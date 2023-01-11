from flask import Blueprint, jsonify, request
from app.api.lib.base_model import BaseModel
from app.api.lib.date_time import format_datetime_id, format_indo
from app.api.lib.status_code import *
from app.models.master_model import KelasModel, WaliKelasModel
from app.models.user_details_model import GuruModel
from app.models.user_model import UserModel
from app.extensions import db

guru = Blueprint("guru", __name__, url_prefix="/api/v2/guru")


@guru.route("/get-all")
def get():
    base_model = BaseModel(GuruModel)
    data = []
    for user in base_model.get_all():
        data.append(
            {
                "id": user.user_id,
                "nip": user.user.username,
                "first_name": user.first_name.title(),
                "last_name": user.last_name.title(),
                "gender": user.gender.title(),
                "agama": user.agama.title() if user.agama else "-",
                "alamat": user.alamat.title() if user.alamat else "-",
                "telp": user.telp if user.telp else "-",
                "active": True if user.user.is_active == "1" else False,
                "join": format_indo(user.user.join_date),
                "last_update": format_indo(user.user.update_date)
                if user.user.update_date
                else "-",
                "last_login": format_datetime_id(user.user.user_last_login)
                if user.user.user_last_login
                else "-",
                "type": user.user.group.upper(),
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
                    id=guru.user.id,
                    nip=guru.user.username,
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

            guru.user.username = username
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
