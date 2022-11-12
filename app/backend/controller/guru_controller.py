from flask import Blueprint, jsonify, request
from app.backend.lib.base_model import BaseModel
from app.backend.lib.date_time import format_datetime_id, format_indo
from app.backend.lib.status_code import *
from app.backend.models.master_model import KelasModel, WaliKelasModel
from app.backend.models.user_details_model import GuruModel
from app.backend.models.user_model import UserModel
from app.backend.extensions import db

guru = Blueprint("guru", __name__, url_prefix="/api/v2/guru")


@guru.route("/get-all")
def get():
    base_model = BaseModel(GuruModel)
    data = []
    for user in base_model.get_all():
        data.append(
            {
                "id": user.users.id,
                "nip": user.users.username,
                "first_name": user.first_name.title(),
                "last_name": user.last_name.title(),
                "gender": user.gender.title(),
                "agama": user.agama.title() if user.agama else "-",
                "alamat": user.alamat.title() if user.alamat else "-",
                "telp": user.telp if user.telp else "-",
                "active": True if user.users.is_active == "1" else False,
                "join": format_indo(user.users.join_date),
                "last_update": format_indo(user.users.update_date)
                if user.users.update_date
                else "-",
                "last_login": format_datetime_id(user.users.user_last_login)
                if user.users.user_last_login
                else "-",
                "type": user.users.group.upper(),
            }
        )
    return jsonify(data), HTTP_200_OK


@guru.route("single/<int:id>", methods=["GET", "PUT", "DELETE"])
def get_single_object(id):
    base = BaseModel(GuruModel)
    guru = base.get_one_or_none(user_id=id)

    if request.method == "GET":
        if not guru:
            return jsonify(msg="Data not found."), HTTP_404_NOT_FOUND
        else:
            return (
                jsonify(
                    id=guru.users.id,
                    nip=guru.users.username,
                    first_name=guru.first_name.title(),
                    last_name=guru.last_name.title(),
                    gender=guru.gender.title(),
                    agama=guru.agama.title(),
                    alamat=guru.alamat.title(),
                    telp=guru.telp,
                ),
                HTTP_200_OK,
            )

    elif request.method == "PUT":
        # NOTE : Check user before request
        if not guru:
            return jsonify(msg="Data is not found."), HTTP_404_NOT_FOUND
        else:
            # NOTE : REQUEST JSON TO SAVE CHANGES
            username = request.json.get("nip")
            first_name = request.json.get("first_name")
            last_name = request.json.get("last_name")
            gender = request.json.get("gender")
            agama = request.json.get("agama")
            alamat = request.json.get("alamat")
            telp = request.json.get("telp")

            guru.users.username = username
            guru.first_name = first_name
            guru.last_name = last_name
            guru.gender = gender
            guru.agama = agama
            guru.alamat = alamat
            guru.telp = telp

            base.edit()
            return (
                jsonify(msg=f"Data Guru: {guru.first_name} berhasil di perbaharui."),
                HTTP_200_OK,
            )

    elif request.method == "DELETE":
        # NOTE : CHECK USER BEFORE REQUEST
        if not guru:
            return jsonify(msg="Data is not found."), HTTP_404_NOT_FOUND
        else:
            base = BaseModel(UserModel)
            user = base.get_one_or_none(id=id)
            base.delete(user)
            return jsonify(msg="Data has been deleted."), HTTP_204_NO_CONTENT


@guru.route("/wali-kelas")
def get_wali_kelas():
    model = BaseModel(WaliKelasModel)
    wali_kelas = model.get_all()

    data = []
    for _ in wali_kelas:
        data.append(
            {
                "first_name": _.guru.first_name,
                "last_name": _.guru.last_name,
                "kelas": _.kelas.kelas,
            }
        )

    return jsonify(data=data), HTTP_200_OK
