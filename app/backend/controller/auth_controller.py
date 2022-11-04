from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    current_user,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    create_access_token,
    create_refresh_token,
)
from app.backend.extensions import jwt
from app.backend.lib.base_model import BaseModel
from app.backend.lib.date_time import format_datetime_id, format_indo, utc_makassar
from app.backend.models.master_model import KelasModel
from app.backend.models.user_details_model import *
from app.backend.models.user_model import TokenBlockList, UserModel
from app.backend.extensions import db
from app.backend.lib.status_code import *
from werkzeug.security import generate_password_hash

auth = Blueprint("auth", __name__, url_prefix="/api/v2/auth")


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlockList.id).filter_by(jti=jti).scalar()
    return token is not None


@auth.route("/login", methods=["POST", "GET", "PUT"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = BaseModel(UserModel)
    sql_user = user.get_one_or_none(username=username)

    if not sql_user:
        return jsonify({"msg": "username not found."}), HTTP_401_UNAUTHORIZED
    else:
        chk_pswd = UserModel.check_pswd(sql_user.password, password)
        if chk_pswd:
            if sql_user.group == "siswa" and sql_user.is_active == "1":
                base_siswa = BaseModel(SiswaModel)
                sql_siswa = base_siswa.get_one_or_none(user_id=sql_user.id)
                base_kelas = BaseModel(KelasModel)
                sql_kelas = base_kelas.get_one(id=sql_siswa.kelas_id)
                user_identity = {
                    "id": sql_user.id,
                    "username": sql_user.username,
                    "first_name": sql_siswa.first_name,
                    "last_name": sql_siswa.last_name,
                    "kelas": sql_kelas.kelas if sql_siswa.kelas_id else "-",
                    "is_active": sql_user.is_active,
                    "group": sql_user.group,
                }

                access_token = create_access_token(identity=user_identity)
                refresh_token = create_refresh_token(identity=user_identity)
                sql_user.user_last_login = utc_makassar()
                user.edit()
                return (
                    jsonify(
                        {
                            "id": sql_user.id,
                            "username": sql_user.username,
                            "first_name": sql_siswa.first_name,
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                        }
                    ),
                    HTTP_200_OK,
                )

            elif sql_user.group == "guru" and sql_user.is_active == "1":
                sql_user.user_last_login = utc_makassar()
                base_guru = BaseModel(GuruModel)
                sql_guru = base_guru.get_one_or_none(user_id=sql_user.id)
                user_identity = {
                    "id": sql_user.id,
                    "username": sql_user.username,
                    "first_name": sql_guru.first_name,
                    "last_name": sql_guru.last_name,
                    "is_active": sql_user.is_active,
                    "group": sql_user.group,
                }
                access_token = create_access_token(identity=user_identity)
                refresh_token = create_refresh_token(identity=user_identity)
                user.edit()
                return (
                    jsonify(
                        {
                            "id": sql_user.id,
                            "username": sql_user.username,
                            "first_name": sql_guru.first_name,
                            "acces_token": access_token,
                            "refresh_token": refresh_token,
                        }
                    ),
                    HTTP_200_OK,
                )
            else:
                return (
                    jsonify({"msg": "Akun smntr tidak dapat di akses"}),
                    HTTP_400_BAD_REQUEST,
                )
        else:
            return jsonify({"msg": "Password not valid."}), HTTP_401_UNAUTHORIZED


@auth.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt()["jti"]
    now = utc_makassar()
    db.session.add(TokenBlockList(jti=jti, created_at=now))
    db.session.commit()

    model = BaseModel(UserModel)
    id = get_jwt_identity()["id"]
    user = model.get_one_or_none(id=id)
    user.user_logout = utc_makassar()
    model.edit()
    return jsonify(msg="JWT revoked")


@auth.route("/refresh", methods=["POST", "GET"])
@jwt_required(refresh=True)
def refresh_toke():
    identity = get_jwt_identity()
    access_token = create_access_token(identity, fresh=False)

    return jsonify(access=access_token), HTTP_200_OK


@auth.route("/create", methods=["POST", "GET"])
def create():
    username = request.json.get("username")
    password = request.json.get("password")
    group = request.json.get("group")

    hash_pswd = generate_password_hash(password=password)
    user = BaseModel(
        UserModel(
            username,
            hash_pswd,
            group,
        )
    )
    if group == "siswa" or group == "SISWA":
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        gender = request.json.get("gender")
        agama = request.json.get("agama")
        kelas = request.json.get("kelas_id")

        usrnm = BaseModel(UserModel)
        check_username = usrnm.get_one(username=username)

        if check_username is not None:
            return jsonify({"msg": "Username is already exists"}), HTTP_409_CONFLICT
        else:
            user.create()
            siswa = BaseModel(
                SiswaModel(first_name, last_name, gender, agama, user.model.id, kelas)
            )
            siswa.create()
            return (
                jsonify(
                    {
                        "msg": f"Add user {user.model.username} succesful.",
                        "id": siswa.model.id,
                    }
                ),
                HTTP_201_CREATED,
            )

    elif group == "guru":
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        gender = request.json.get("gender")
        alamat = request.json.get("alamat")
        agama = request.json.get("agama")
        mapel_id = request.json.get("mapel")
        telp = request.json.get("telp")

        usrnm = BaseModel(UserModel)
        check_username = usrnm.get_one(username=username)

        if check_username is not None:
            return jsonify(msg= "Username is already exists"), HTTP_409_CONFLICT
        else:
            user.create()
            guru = BaseModel(
                GuruModel(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    alamat=alamat,
                    agama=agama,
                    user_id=user.model.id,
                    mapel=mapel_id,
                    telp=telp,
                )
            )
            guru.create()
            return jsonify(msg= f"Data Guru : {guru.model.first_name} telah berhasil di tambahkan."), HTTP_201_CREATED

    elif group == "admin":
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        gender = request.json.get("gender")
        alamat = request.json.get("alamat")

        usrnm = BaseModel(UserModel)
        check_username = usrnm.get_one(username=username)

        if check_username is not None:
            return jsonify({"msg": "Username is already exists"}), HTTP_409_CONFLICT
        else:
            user.create()
            user_detail = BaseModel(
                AdminDetailModel(first_name, last_name, gender, alamat, user.model.id)
            )
            user_detail.create()
            return jsonify(msg= f"Data Admin : {user_detail.model.first_name} telah berhasil di tambahkan."), HTTP_201_CREATED


@auth.route("/get-one")
@jwt_required()
def get_one():
    current_user = get_jwt_identity()
    user_id = current_user.get("id")
    # jjwt = get_jwt()['exp']
    if current_user.get("group") == "siswa":
        model = BaseModel(SiswaModel)
        user = model.get_one_or_none(user_id=user_id)
        json_object = {
            "id": user_id,
            "first_name": current_user.get("first_name"),
            "last_name": current_user.get("last_name"),
            "kelas": current_user.get("kelas"),
            "group": current_user.get("group"),
            "is_active": current_user.get("is_active"),
            "gender": user.gender.title(),
        }
        return jsonify(json_object), HTTP_200_OK
    elif current_user.get("group") == "guru":
        model = BaseModel(GuruModel)
        user = model.get_one_or_none(user_id=user_id)
        return (
            jsonify(
                {
                    "id": user_id,
                    "first_name": current_user.get("first_name"),
                    "last_name": current_user.get("last_name"),
                    "group": current_user.get("group"),
                    "is_active": current_user.get("is_active"),
                    "gender": user.gender.title(),
                }
            ),
            HTTP_200_OK,
        )
    elif current_user.get("group") == "admin":
        model = BaseModel(AdminDetailModel)
        user = model.get_one_or_none(user_id=user_id)
        return (
            jsonify(
                {
                    "id": user_id,
                    "first_name": current_user.get("first_name"),
                    "last_name": current_user.get("last_name"),
                    "group": current_user.get("group"),
                    "is_active": current_user.get("is_active"),
                    "gender": user.gender,
                }
            ),
            HTTP_200_OK,
        )


@auth.route("/get-all")
def get_all():
    model = BaseModel(UserModel)
    data = []
    for user in model.get_all():
        data.append(
            {
                "id": user.id,
                "username": user.username,
                "group": user.group,
                "join": format_indo(user.join_date),
                "last_update": format_datetime_id(user.update_date)
                if user.update_date
                else "-",
                "last_login": format_datetime_id(user.user_last_login)
                if user.user_last_login
                else "-",
                "is_active": user.is_active,
            }
        )
    return jsonify(data), HTTP_200_OK


@auth.route("/edit-status", methods=["PUT"])
def edit_status():
    base = BaseModel(UserModel)
    id = request.args.get("id")
    model = base.get_one_or_none(id=id)

    status = request.json.get("status")
    model.is_active = status

    base.edit()

    return jsonify(msg="Upadated Success."), HTTP_200_OK


@auth.put("/edit-password")
def edit_password():
    base = BaseModel(UserModel)
    id = request.args.get("id")
    model = base.get_one_or_none(id=id)
    password = request.json.get("password")

    if not model:
        return jsonify(msg="User not found."), HTTP_404_NOT_FOUND
    elif len(password) < 6:
        return jsonify(msg="Password minimal 6 karakter"), HTTP_400_BAD_REQUEST
    else:
        hash_pswd = generate_password_hash(password=password)
        model.password = hash_pswd
        base.edit()
        return jsonify(msg="Upadated Password Succsess."), HTTP_200_OK
