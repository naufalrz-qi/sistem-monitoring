import json
import time
from flask import (
    Blueprint,
    Response,
    abort,
    request,
    redirect,
    send_from_directory,
    url_for,
    render_template,
    flash,
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from calendar import monthrange
from app.backend.lib.status_code import HTTP_413_REQUEST_ENTITY_TOO_LARGE
from app.backend.models.user_model import *
from app.backend.models.master_model import *
from app.backend.models.user_details_model import *
from app.backend.lib.base_model import BaseModel
from app.frontend.forms.form_absen import FormSelectAbsensi, FormSelectKehadiranSemester
from app.frontend.forms.form_auth import FormEditStatus
from app.frontend.forms.form_jadwal import FormJadwalMengajar
from app.frontend.forms.form_letter_report import FormSelectKelas
from app.frontend.forms.form_master import *
from app.frontend.forms.form_siswa import FormAddSiswa, FormEditSiswa
from ..forms.form_auth import *
from ..forms.form_guru import *
from ..lib.base_url import base_url
from ..models.user_login_model import *
from ...backend.models.data_model import *
from sqlalchemy import func
import os
import requests as req
import io
import xlwt

admin2 = Blueprint(
    "admin2", __name__, template_folder="../templates/", url_prefix="/admin"
)

file = os.getcwd() + "/data.json"


@admin2.route("/admin/<path:filename>")
def static(filename):
    dir = send_from_directory("frontend/static", filename)
    return dir


sql = lambda x: x


@admin2.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.group == "admin":
            jml_siswa = sql(
                x=db.session.query(UserModel).filter(UserModel.group == "siswa").count()
            )
            jml_guru = sql(
                x=db.session.query(UserModel).filter(UserModel.group == "guru").count()
            )
            jml_admin = sql(
                x=db.session.query(UserModel).filter(UserModel.group == "admin").count()
            )

            jml_mapel = sql(x=db.session.query(MapelModel).count())

            jml_kelas = sql(x=db.session.query(KelasModel).count())

            return render_template(
                "admin/index_admin.html",
                jml_siswa=jml_siswa,
                jml_guru=jml_guru,
                jml_admin=jml_admin,
                jml_mapel=jml_mapel,
                jml_kelas=jml_kelas,
            )
        else:
            abort(404)


class PenggunaSiswa:
    @admin2.route("get-siswa")
    @login_required
    def getSiswa():
        if current_user.is_authenticated:
            if current_user.group == "admin":
                urlKelas = base_url + "api/v2/master/kelas/get-all"
                respKelas = req.get(urlKelas)
                jsonRespKelas = respKelas.json()

                urlSiswa = base_url + url_for("siswa.get")
                respSiswa = req.get(urlSiswa)
                jsonRespSiswa = respSiswa.json()
                return render_template(
                    "admin/siswa/get_siswa.html",
                    kelas=jsonRespKelas,
                    siswa=jsonRespSiswa,
                )
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    @admin2.route("/data-siswa")
    @login_required
    def get_siswa():
        if current_user.is_authenticated:
            if current_user.group == "admin":
                url = base_url + url_for("siswa.get")
                r = req.get(url)
                data = r.json()
                # NOTE: GET KELAS
                base_kelas = request.url_root
                url_kelas = base_kelas + url_for("master.kelas_all")
                resp_kelas = req.get(url_kelas)
                json_kelas = resp_kelas.json()
                return render_template(
                    "admin/siswa/data_siswa.html",
                    model=data,
                    jsonKelas=json_kelas,
                )
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    @admin2.route("/generate-qc", methods=["GET", "PUT"])
    @login_required
    def generate_qc():
        if current_user.is_authenticated:
            if current_user.group == "admin":
                id = request.args.get("id")
                url = base_url + url_for("siswa.generate_qc", id=id)
                headers = {"Content-Type": "application/json"}
                r = req.put(url, headers=headers)
                if r.status_code == 200:
                    flash(
                        message=f"Generate QR kode berhasil. Status : {r.status_code}",
                        category="success",
                    )
                    return redirect(url_for("admin2.getSiswa"))
                    # return redirect(url_for("admin2.get_siswa"))
                else:
                    flash(
                        message=f"Maaf terjadi kesalahan dalam generate QR CODE. Status : {r.status_code}",
                        category="error",
                    )
                    return redirect(url_for("admin2.getSiswa"))
                    # return redirect(url_for("admin2.get_siswa"))
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    # NOTE:  UPLOAD FOTO
    @admin2.post("/upload-photo")
    # @admin2.route('/upload-photo', methods=['GET','PUT','POST'])
    @login_required
    def upload_foto():
        if current_user.is_authenticated:
            if current_user.group == "admin":
                id = request.args.get("id")
                url = base_url + url_for("siswa.upload_photo", id=id)
                file = request.files["file"]
                file_name = secure_filename(file.filename)
                upload_folder = os.getcwd() + "/temp/"
                path = upload_folder + file_name
                file.save(path)

                files = {"images": open(path, "rb+")}
                response = req.post(url, files=files)

                if response.status_code == 200:
                    files.get("images").close()
                    temp_file = upload_folder + file_name
                    os.remove(f"{temp_file}")
                    flash(
                        f"File foto siswa telah berhasil di upload. Status : {response.status_code}",
                        "success",
                    )
                    return redirect(url_for("admin2.getSiswa"))
                    # return redirect(url_for("admin2.get_siswa"))
                else:
                    return f"<p>error : {response.status_code}</p>"
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    @admin2.errorhandler(413)
    def request_entity_too_large(error):
        return "File Upload Maks 2MB", HTTP_413_REQUEST_ENTITY_TOO_LARGE

    # NOTE:  TAMBAH DATA SISWA
    @admin2.route("/add-siswa", methods=["GET", "POST"])
    @login_required
    def add_siswa():
        # get kelas
        if current_user.is_authenticated:
            if current_user.group == "admin":
                url_kelas = base_url + f"/api/v2/master/kelas/get-all"
                get_kelas = req.get(url_kelas)
                data = get_kelas.json()
                kelas = [("", "..::Select::..")]
                for _ in data["data"]:
                    kelas.append((_["id"], _["kelas"]))

                url = base_url + f"/api/v2/auth/create"
                form = FormAddSiswa(request.form)
                form.kelas.choices = kelas
                if request.method == "POST" and form.validate_on_submit():
                    username = form.username.data
                    password = form.password.data
                    group = form.tipe.data if form.tipe.data else "siswa"
                    fullname = form.fullname.data
                    first_name = ""
                    last_name = ""
                    first_name, *last_name = fullname.split()
                    if len(last_name) == 0:
                        last_name = first_name
                    elif len(last_name) != 0:
                        last_name = " ".join(last_name)
                    gender = form.jenisKelamin.data
                    agama = form.agama.data
                    kelas = form.kelas.data
                    telp = request.form.get("telp")

                    payload = json.dumps(
                        {
                            "username": username,
                            "password": password,
                            "group": group,
                            "first_name": first_name,
                            "last_name": last_name,
                            "gender": gender,
                            "agama": agama,
                            "kelas_id": kelas,
                            "telp": telp,
                        }
                    )
                    headers = {"Content-Type": "application/json"}
                    response = req.post(url=url, headers=headers, data=payload)
                    msg = response.json()
                    if response.status_code == 201:
                        flash(
                            message=f"{msg['msg']}. Status : {response.status_code}",
                            category="success",
                        )
                        return redirect(url_for("admin2.getSiswa"))
                        # return redirect(url_for("admin2.get_siswa"))
                    elif response.status_code == 409:
                        flash(
                            message="NISN sudah yang di input, telah terdaftar",
                            category="error",
                        )
                    else:
                        return render_template(
                            "admin/siswa/tambah_siswa.html", form=form
                        )
                return render_template("admin/siswa/tambah_siswa.html", form=form)
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    # NOTE:  UPDATE DATA SISWA
    @admin2.route("/update-siswa/<int:id>", methods=["GET", "POST", "PUT"])
    @login_required
    def update_siswa(id):
        if current_user.is_authenticated:
            if current_user.group == "admin":
                form = FormEditSiswa()
                # GET KELAS
                url_kelas = base_url + f"/api/v2/master/kelas/get-all"
                get_kelas = req.get(url_kelas)
                list_kelas = get_kelas.json()["data"]
                choices = [("", "- Pilih -")]
                for _ in list_kelas:
                    # form.kelas.choices.append((_["id"], _["kelas"]))
                    choices.append((_["id"], _["kelas"]))
                form.kelas.choices = choices

                url_obj = base_url + f"api/v2/student/single/{id}"

                resp_obj = req.get(url=url_obj)
                json_resp = resp_obj.json()
                kelasId = json_resp["kelas_id"]
                form.nisn.default = json_resp["nisn"]
                form.fullname.default = (
                    json_resp["first_name"] + " " + json_resp["last_name"]
                )
                form.kelas.default = next(
                    obj["id"]
                    for obj in list_kelas
                    if json_resp["kelas"] in obj["kelas"]
                )
                form.jenisKelamin.default = json_resp["gender"].lower()
                form.tempatLahir.default = json_resp["tempat_lahir"]
                """
                NOTE: Convert str to datetime.date
                buat logika jika string tgl ada maka convert ke datetime.strptime(str_date, format).date
                jika tidak maka tetapkan string tgl default '2000-10-10' agar tidak terjadi error
                """
                from_date = (
                    json_resp["tgl_lahir"] if json_resp["tgl_lahir"] else "2000-10-10"
                )
                to_date = datetime.strptime(from_date, "%Y-%m-%d").date()
                """"""
                form.tanggalLahir.default = to_date if json_resp["tgl_lahir"] else None
                form.agama.default = json_resp["agama"].lower()
                form.alamat.default = json_resp["alamat"]
                form.namaOrtu.default = json_resp["nama_ortu"]
                form.telp.default = json_resp["telp"]
                form.process()
                """
                Cara for and if dari umum sampai tracky
                ## cara umum
                # nilai = None
                # for item in list_kelas:
                #     if json_resp['kelas'] in item['kelas']:
                #         nilai = item['id']
                ## cara 1
                # item = next((item['id'] for item in list_kelas if json_resp['kelas'] in item['kelas']), None)
                ## cara 2
                # item = next(item['id'] for item in list_kelas if json_resp['kelas'] in item['kelas'])    
                """
                if request.method == "POST":
                    nisn = request.form.get("nisn")
                    fullname = request.form.get("fullname")
                    first_name = ""
                    last_name = ""
                    first_name, *last_name = fullname.split() if fullname else "None"
                    if len(last_name) == 0:
                        last_name = first_name
                    elif len(last_name) != 0:
                        last_name = " ".join(last_name)
                    kelas = request.form.get("kelas")
                    gender = request.form.get("jenisKelamin")
                    tempat_lahir = request.form.get("tempatLahir")
                    tgl_lahir = request.form.get("tanggalLahir")
                    agama = request.form.get("agama")
                    alamat = request.form.get("alamat")
                    nama_ortu = request.form.get("namaOrtu")
                    telp = request.form.get("telp")
                    headers = {"Content-Type": "application/json"}
                    payload = json.dumps(
                        {
                            "nisn": nisn,
                            "first_name": first_name,
                            "last_name": last_name,
                            "kelas": kelas,
                            "gender": gender,
                            "tempat": tempat_lahir,
                            "tgl": tgl_lahir,
                            "agama": agama,
                            "alamat": alamat,
                            "nama_ortu": nama_ortu,
                            "telp": telp,
                        }
                    )
                    response_update = req.put(url_obj, headers=headers, data=payload)
                    if response_update.status_code == 200:
                        baseKelasAfter = (
                            base_url + f"api/v2/master/kelas/update-jumlah/{kelas}"
                        )
                        updateJumlahSiswaAfter = req.put(
                            url=baseKelasAfter, headers=headers
                        )
                        baseKelasBefore = (
                            base_url + f"api/v2/master/kelas/update-jumlah/{kelasId}"
                        )
                        updateJumlahSiswaAfter = req.put(
                            url=baseKelasBefore, headers=headers
                        )
                        flash(
                            f"Data dari {first_name} telah berhasil diperbaharui.",
                            "info",
                        )
                        return redirect(url_for("admin2.getSiswa"))
                        # return redirect(url_for("admin2.get_siswa"))
                    else:
                        flash(
                            f"Terjadi kesalahan dalam memuat data. statu : {response_update.status_code}",
                            "error",
                        )
                        return render_template(
                            "admin/siswa/edit_siswa.html",
                            form=form,
                            obj=json_resp,
                        )

                return render_template(
                    "admin/siswa/edit_siswa.html", form=form, obj=json_resp
                )
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    # NOTE:  DELETE DATA SISWA
    @admin2.route("/delete-siswa/<int:id>", methods=["GET", "POST", "DELETE"])
    @login_required
    def delete_siswa(id):
        if current_user.group == "admin":
            url = base_url + f"/api/v2/student/single/{id}"
            respGetSiswa = req.get(url)
            jsonResp = respGetSiswa.json()
            kelasId = jsonResp["kelas_id"]

            baseKelas = base_url + f"api/v2/master/kelas/update-jumlah/{kelasId}"
            headers = {"Content-Type": "application/json"}

            response = req.delete(url)
            if response.status_code == 204:
                respkelas = req.put(url=baseKelas, headers=headers)
                flash(
                    message=f"Data siswa telah berhasil di hapus. {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.getSiswa"))
                # return redirect(url_for("admin2.get_siswa"))
            else:
                flash(
                    f"Ada tejadi kesalahan dalam menghapus data. Status : {response.status_code}",
                    "error",
                )
                return redirect(url_for("admin2.getSiswa"))
                # return redirect(url_for("admin2.get_siswa"))

    # eksport data
    @admin2.route("/export-siswa")
    def export_siswa():
        url = request.url_root + url_for("siswa.get")
        req_url = req.get(url)
        data = req_url.json()
        # output in bytes
        output = io.BytesIO()
        # create workbook object
        workbook = xlwt.Workbook()
        # style header
        # style = xlwt.easyxf('font: name Times New Roman, color-index black, bold on; \
        #                     align: wrap on, vert center, horiz center;')
        style = xlwt.XFStyle()
        # background
        bg_color = xlwt.Pattern()
        bg_color.pattern = xlwt.Pattern.SOLID_PATTERN
        bg_color.pattern_fore_colour = xlwt.Style.colour_map["ocean_blue"]
        style.pattern = bg_color

        # border
        boder = xlwt.Borders()
        boder.bottom = xlwt.Borders.THIN
        style.borders = boder

        # font
        font = xlwt.Font()
        font.bold = True
        font.name = "Times New Roman"
        font.height = 220
        style.font = font

        # font aligment
        align = xlwt.Alignment()
        align.wrap = xlwt.Alignment.NOT_WRAP_AT_RIGHT
        align.horz = xlwt.Alignment.HORZ_CENTER
        align.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = align

        # add a sheet
        sh = workbook.add_sheet("Data Siswa")
        # add headers
        sh.write(0, 0, "NO", style)
        sh.write(0, 1, "ID", style)
        sh.write(0, 2, "Nama", style)

        no = 0
        urut = 0

        for row in data["data"]:
            sh.write(no + 1, 0, urut + 1)
            sh.write(no + 1, 1, row["id"])
            no += 1
            urut += 1

        workbook.save(output)
        output.seek(0)

        return Response(
            output,
            mimetype="application/ms-excel",
            headers={"Content-Disposition": "attachment; filename=data_siswa.xls"},
        )


# """NOTE: DATA GURU"""
class PenggunaGuru:
    @admin2.route("data-guru")
    @login_required
    def get_guru():
        if current_user.is_authenticated:
            if current_user.group == "admin":
                url = base_url + "api/v2/guru/get-all"
                response = req.get(url)
                json_resp = response.json()
                return render_template("admin/guru/data_guru.html", model=json_resp)
            else:
                abort(404)

    @admin2.route("tambah-data", methods=["GET", "POST"])
    @login_required
    def add_guru():
        if current_user.is_authenticated:
            if current_user.group == "admin":
                form = FormAddGuru(request.form)
                base = request.root_url

                if request.method == "POST" and form.validate_on_submit():
                    username = form.username.data
                    password = form.password.data
                    group = form.tipe.data if form.tipe.data else "guru"
                    fullname = form.fullname.data
                    first_name = ""
                    last_name = ""
                    first_name, *last_name = fullname.split() if fullname else "None"
                    if len(last_name) == 0:
                        last_name = first_name
                    elif len(last_name) != 0:
                        last_name = " ".join(last_name)
                    gender = form.jenisKelamin.data
                    agama = form.agama.data
                    alamat = form.alamat.data
                    telp = form.telp.data

                    url_create = base + "api/v2/auth/create"
                    payload = json.dumps(
                        {
                            "username": username,
                            "password": password,
                            "group": group,
                            "first_name": first_name,
                            "last_name": last_name,
                            "gender": gender,
                            "alamat": alamat,
                            "agama": agama,
                            "telp": telp,
                        }
                    )
                    headers = {"Content-Type": "application/json"}
                    response = req.post(url=url_create, data=payload, headers=headers)
                    msg = response.json().get("msg")

                    if response.status_code == 201:
                        flash(f"{msg} Status : {response.status_code}", "success")
                        return redirect(url_for("admin2.get_guru"))
                    else:
                        flash(f"{msg}. Status : {response.status_code}", "error")
                        # return redirect(url_for('admin2.get_guru'))
                        return render_template("admin/guru/tambah_guru.html", form=form)
                return render_template("admin/guru/tambah_guru.html", form=form)
            else:
                abort(404)

    @admin2.route("update-guru/<int:id>", methods=["POST", "GET"])
    @login_required
    def update_guru(id):
        if current_user.group == "admin":
            form = FormEditGuru(request.form)
            # NOTE: GET SINGLE OBJECT
            url_obj = base_url + f"api/v2/guru/single/{id}"
            resp_obj = req.get(url=url_obj)
            jsonObj = resp_obj.json()

            # FORM DEFAULT VALUE
            form.nip.default = jsonObj["nip"]
            form.fullname.default = jsonObj["first_name"] + " " + jsonObj["last_name"]
            form.jenisKelamin.default = jsonObj["gender"].lower()
            form.agama.default = jsonObj["agama"].lower()
            form.alamat.default = jsonObj["alamat"]
            form.telp.default = jsonObj["telp"]
            form.process()

            # NOTE: REQUEST FORM TO SAVE CHANGES
            if request.method == "POST":
                nip = request.form.get("nip")
                fullname = request.form.get("fullname")
                # NOTE : SPLIT FULLNAME TO FIRST_NAME and LAST_NAME
                first_name = ""
                last_name = ""
                first_name, *last_name = fullname.split() if fullname else "None"
                if len(last_name) == 0:
                    last_name = first_name
                elif len(last_name) != 0:
                    last_name = " ".join(last_name)
                # END
                gender = request.form.get("jenisKelamin")
                agama = request.form.get("agama")
                alamat = request.form.get("alamat")
                telp = request.form.get("telp")

                # HEADERS, DATA TO RESPONSE
                payload = json.dumps(
                    {
                        "nip": nip,
                        "first_name": first_name,
                        "last_name": last_name,
                        "gender": gender,
                        "agama": agama,
                        "alamat": alamat,
                        "telp": telp,
                    }
                )
                headers = {"Content-Type": "application/json"}

                resp_obj = req.put(url=url_obj, data=payload, headers=headers)
                msg = resp_obj.json()
                if resp_obj.status_code == 200:
                    flash(f"{msg['msg']} Status : {resp_obj.status_code}", "success")
                    return redirect(url_for("admin2.get_guru"))
                else:
                    flash(f"{msg['msg']}. Status : {resp_obj.status_code}", "error")
                return render_template("admin/guru/edit_guru.html", form=form)
            return render_template("admin/guru/edit_guru.html", form=form)
        else:
            abort(404)

    @admin2.route("delete-guru/<id>", methods=["GET", "DELETE", "POST"])
    @login_required
    def delete_guru(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/guru/single/{id}"
            response = req.delete(url=url)

            if response.status_code == 204:
                flash(
                    message=f"Data guru telah berhasil di hapus. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_guru"))
            else:
                flash(
                    message=f"Terjadi kesalahan dalama memuat data. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_guru"))
        else:
            abort(404)


class PenggunaUser:
    @admin2.route("/data-user")
    @login_required
    def get_user():
        if current_user.group == "admin":
            url = base_url + f"api/v2/auth/get-all"
            response = req.get(url)
            json_resp = response.json()
            form = FormEditStatus()
            formUpdatePassword = FormEditPassword()
            return render_template(
                "admin/pengguna/data_user.html",
                user=json_resp,
                form=form,
                formPassword=formUpdatePassword,
            )
        else:
            abort(404)

    @admin2.post("/edit-status/<int:id>")
    @login_required
    def update_status(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/auth/edit-status?id={id}"

            status_form = request.form.get("status")

            status = ""
            if request.method == "POST":
                if status_form == "Aktif":
                    status = "0"
                elif status_form == "Non-Aktif":
                    status = "1"

                payload = json.dumps({"status": status})
                headers = {"Content-Type": "application/json"}
                response = req.put(url, headers=headers, data=payload)

                if response.status_code == 200:
                    return redirect(url_for("admin2.get_user"))
                else:
                    return redirect(url_for("admin2.get_user"))
        else:
            abort(400)

    @admin2.post("edit-pswd/<int:id>")
    @login_required
    def update_password(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/auth/edit-password?id={id}"
            if request.method == "POST":
                password = request.form.get("kataSandi")

                headers = {"Content-Type": "application/json"}
                payload = json.dumps({"password": password})

                response = req.put(url=url, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 200:
                    flash(
                        message=f'{msg["msg"]}, status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_user"))
                elif response.status_code == 400:
                    flash(
                        f'Error: {msg["msg"]}, status : {response.status_code}', "error"
                    )
                    return redirect(url_for("admin2.get_user"))
                else:
                    flash(
                        f"Error: Terjadi kesalahan dalam memuat data, status : {response.status_code}",
                        "error",
                    )
                    return redirect(url_for("admin2.get_user"))
        else:
            abort(404)


# NOTE: MASTER DATA
class MasterData:
    # NOTE: ================== MASTER DATA MAPEL =====================================
    @admin2.get("data-mapel")
    @login_required
    def get_mapel():
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/mapel/get-all"
            response = req.get(url)
            jsonRespon = response.json()
            return render_template(
                "admin/master/mapel/data_mapel.html", model=jsonRespon
            )
        else:
            abort(404)

    @admin2.route("add-mapel", methods=["POST", "GET"])
    @login_required
    def add_mapel():
        if current_user.group == "admin":
            form = FormMapel(request.form)
            URL = base_url + f"api/v2/master/mapel/create"
            if request.method == "POST" and form.validate_on_submit():
                mapel = form.mapel.data
                payload = json.dumps({"mapel": mapel})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 201:
                    flash(
                        message=f"{msg['msg']}. Status : {response.status_code}",
                        category="success",
                    )
                    return redirect(url_for("admin2.get_mapel"))
                else:
                    flash(
                        message=f"{msg['msg']}. Status : {response.status_code}",
                        category="error",
                    )
                    return render_template(
                        "admin/master/mapel/tambah_mapel.html", form=form
                    )
            return render_template("admin/master/mapel/tambah_mapel.html", form=form)
        else:
            abort(404)

    @admin2.route("edit-mapel/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_mapel(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/mapel/get-one/{id}"

            # NOTE: GET ONE DATA BY ID
            responGetMapel = req.get(url=URL)
            jsonResponse = responGetMapel.json()

            form = FormMapel(request.form)
            form.mapel.data = jsonResponse["mapel"]
            if request.method == "POST" and form.validate_on_submit():
                mapel = request.form.get("mapel")
                payload = json.dumps({"mapel": mapel})
                headers = {"Content-Type": "application/json"}
                response = req.put(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 200:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="info",
                    )
                    return redirect(url_for("admin2.get_mapel"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/mapel/edit_mapel.html", form=form
                    )
            return render_template("admin/master/mapel/edit_mapel.html", form=form)
        else:
            abort(404)

    @admin2.route("delete-mapel/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_mapel(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/mapel/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    message=f"Data mapel telah di hapus dari database. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_mapel"))
            elif response.status_code == 404:
                msg = response.json()
                flash(
                    message=f"{msg['msg']} : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_mapel"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA SESMESTER =====================================
    @admin2.get("data-semester")
    @login_required
    def get_semester():
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/semester/get-all"
            response = req.get(URL)
            jsonResp = response.json()
            return render_template(
                "admin/master/semester/data_semester.html", model=jsonResp
            )
        else:
            abort(404)

    @admin2.route("add-semester", methods=["GET", "POST"])
    @login_required
    def add_semester():
        if current_user.group == "admin":
            form = FormSemester(request.form)
            URL = base_url + f"api/v2/master/semester/create"
            if request.method == "POST" and form.validate_on_submit():
                semester = form.semester.data
                status = form.status.data

                payload = json.dumps({"semester": semester, "status": status})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status: {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_semester"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status: {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/semester/tambah_semester.html", form=form
                    )

            return render_template(
                "admin/master/semester/tambah_semester.html", form=form
            )
        else:
            abort(404)

    @admin2.route("edit-semester/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_semester(id):
        if current_user.group == "admin":
            form = FormEditSemester(request.form)
            URL = base_url + f"api/v2/master/semester/get-one/{id}"
            responseGet = req.get(url=URL)
            jsonResp = responseGet.json()
            form.status.data = "1" if jsonResp["status"] == True else "0"

            if request.method == "POST" and form.validate_on_submit():
                status = request.form.get("status")
                payload = json.dumps({"status": status})
                headers = {"Content-Type": "application/json"}
                response = req.put(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 200:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="info",
                    )
                    return redirect(url_for("admin2.get_semester"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/semester/edit_semester.html", form=form
                    )
            return render_template(
                "admin/master/semester/edit_semester.html", form=form
            )
        else:
            abort(404)

    @admin2.route("delete-semester/<int:id>", methods=["DELETE", "GET"])
    @login_required
    def delete_semester(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/semester/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    message=f"Data semester telah di hapus dari database. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_semester"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA TAHUN AJARAN =====================================
    @admin2.route("data-tahun-ajaran")
    @login_required
    def get_ajaran():
        if current_user.group == "admin":
            URL = base_url + "api/v2/master/ajaran/get-all"
            response = req.get(URL)
            jsonResp = response.json()
            return render_template(
                "admin/master/tahun_ajaran/data_tahun_ajaran.html", model=jsonResp
            )
        else:
            abort(404)

    @admin2.route("add-tahun-ajaran", methods=["GET", "POST"])
    @login_required
    def add_ajaran():
        if current_user.group == "admin":
            form = FormTahunAJaran(request.form)
            URL = base_url + "api/v2/master/ajaran/create"

            if request.method == "POST" and form.validate_on_submit():
                ajaran = form.tahunAjaran.data
                status = form.status.data

                payload = json.dumps({"ajaran": ajaran, "status": status})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_ajaran"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/tahun_ajaran/tambah_tahun_ajaran.html", form=form
                    )
            return render_template(
                "admin/master/tahun_ajaran/tambah_tahun_ajaran.html", form=form
            )
        else:
            abort(404)

    @admin2.route("edit-tahun-ajaran/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_ajaran(id):
        if current_user.group == "admin":
            form = FormTahunAJaran(request.form)
            URL = base_url + f"api/v2/master/ajaran/get-one/{id}"
            response = req.get(URL)
            jsonResp = response.json()
            form.tahunAjaran.data = jsonResp["ajaran"]
            form.status.data = "1" if jsonResp["status"] == True else "0"

            if request.method == "POST" and form.validate_on_submit():
                ajaran = request.form.get("tahunAjaran")
                status = request.form.get("status")
                payload = json.dumps({"ajaran": ajaran, "status": status})
                headers = {"Content-Type": "application/json"}
                response = req.put(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 200:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="info",
                    )
                    return redirect(url_for("admin2.get_ajaran"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/tahun_ajaran/edit_tahun_ajaran.html", form=form
                    )

            return render_template(
                "admin/master/tahun_ajaran/edit_tahun_ajaran.html", form=form
            )
        else:
            abort(404)

    @admin2.route("delete-tahun-ajaran/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_ajaran(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/ajaran/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    message=f"Data Tahun Ajaran telah dihapus dari database. Status : {response.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_ajaran"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA KELAS =====================================
    @admin2.route("data-kelas")
    @login_required
    def get_kelas():
        if current_user.group == "admin":
            URL = base_url + "api/v2/master/kelas/get-all"
            response = req.get(URL)
            jsonResp = response.json()
            return render_template("admin/master/kelas/data_kelas.html", model=jsonResp)
        else:
            abort(404)

    @admin2.route("add-kelas", methods=["GET", "POST"])
    @login_required
    def add_kelas():
        if current_user.group == "admin":
            form = FormKelas(request.form)
            URL = base_url + "api/v2/master/kelas/create"

            if request.method == "POST" and form.validate_on_submit():
                kelas = form.kelas.data

                payload = json.dumps({"kelas": kelas})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_kelas"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/kelas/tambah_kelas.html", form=form
                    )
            return render_template("admin/master/kelas/tambah_kelas.html", form=form)
        else:
            abort(404)

    @admin2.route("edit-kelas/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_kelas(id):
        if current_user.group == "admin":
            form = FormEditKelas(request.form)
            URL = base_url + f"api/v2/master/kelas/get-one/{id}"

            response = req.get(URL)
            jsonResp = response.json()
            form.kelas.data = jsonResp["kelas"]
            form.jumlahLaki.data = jsonResp["laki"]
            form.jumlahPerempuan.data = jsonResp["perempuan"]
            form.jumlahSiswa.data = jsonResp["seluruh"]

            if request.method == "POST":
                kelas = request.form.get("kelas")
                laki = request.form.get("jumlahLaki")
                perempuan = request.form.get("jumlahPerempuan")
                seluruh = request.form.get("jumlahSiswa")

                payload = json.dumps(
                    {
                        "kelas": kelas,
                        "laki": laki,
                        "perempuan": perempuan,
                        "seluruh": seluruh,
                    }
                )
                headers = {"Content-Type": "application/json"}

                response = req.put(url=URL, data=payload, headers=headers)
                msg = response.json()

                if response.status_code == 200:
                    flash(f'{msg["msg"]} Status : {response.status_code}', "info")
                    return redirect(url_for("admin2.get_kelas"))
                else:
                    flash(f'{msg["msg"]} Status : {response.status_code}', "error")
                    return render_template(
                        "admin/master/kelas/edit_kelas.html", form=form
                    )
            return render_template("admin/master/kelas/edit_kelas.html", form=form)
        else:
            abort(404)

    @admin2.route("delete-kelas/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_kelas(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/kelas/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    f"Data kelas telah dihpus dari database. Status : {response.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_kelas"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA HARI =====================================
    @admin2.route("data-hari")
    @login_required
    def get_hari():
        if current_user.group == "admin":
            URL = base_url + "api/v2/master/hari/get-all"
            response = req.get(URL)
            jsonResp = response.json()
            return render_template("admin/master/hari/data_hari.html", model=jsonResp)
        else:
            abort(404)

    @admin2.route("add-hari", methods=["GET", "POST"])
    @login_required
    def add_hari():
        if current_user.group == "admin":
            URL = base_url + "api/v2/master/hari/create"
            form = FormHari(request.form)
            if request.method == "POST" and form.validate_on_submit():
                hari = form.hari.data

                payload = json.dumps({"hari": hari})
                headers = {"Content-Type": "application/json"}
                response = req.post(url=URL, data=payload, headers=headers)
                msg = response.json()
                if response.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_hari"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {response.status_code}',
                        category="error",
                    )
                    return render_template(
                        "admin/master/hari/tambah_hari.html", form=form
                    )

            return render_template("admin/master/hari/tambah_hari.html", form=form)
        else:
            abort(404)

    @admin2.route("edit-hari/<int:id>", methods=["GET", "POST"])
    def edit_hari(id):
        pass

    @admin2.route("delete-hari/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_hari(id):
        if current_user.group == "admin":
            URL = base_url + f"api/v2/master/hari/get-one/{id}"
            response = req.delete(URL)
            if response.status_code == 204:
                flash(
                    f"Data hari telah di hapus dari database. Status : {response.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_hari"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA JAM =====================================
    @admin2.route("data-jam")
    @login_required
    def get_jam():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/jam/get-all"
            resp = req.get(url)
            jsonResp = resp.json()
            form = FormJam(request.form)

            return render_template(
                "admin/master/jam/data_jam.html", model=jsonResp, form=form
            )
        else:
            abort(404)

    @admin2.route("tambah-jam", methods=["GET", "POST"])
    @login_required
    def add_jam():
        if current_user.group == "admin":
            form = FormJam(request.form)
            url = base_url + "api/v2/master/jam/create"
            if request.method == "POST":
                jam = form.jam.data
                payload = json.dumps({"jam": jam})
                headers = {"Content-Type": "application/json"}
                resp = req.post(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_jam"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="error",
                    )
                    return redirect(url_for("admin2.get_jam"))
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    @admin2.route("edit-jam/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_jam(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/jam/get-one/{id}"
            if request.method == "POST":
                jam = request.form.get("jam")
                payload = json.dumps({"jam": jam})
                headers = {"Content-Type": "application/json"}
                resp = req.put(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 200:
                    flash(
                        message=f'{msg["msg"]} Status: {resp.status_code}',
                        category="info",
                    )
                    return redirect(url_for("admin2.get_jam"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status: {resp.status_code}',
                        category="error",
                    )
                    return redirect(url_for("admin2.get_jam"))
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    @admin2.route("delete-jam/<int:id>", methods=["GET", "POST"])
    @login_required
    def delete_jam(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/jam/get-one/{id}"
            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    message=f"Data Jam telah dihapus dari database Status: {resp.status_code}",
                    category="info",
                )
                return redirect(url_for("admin2.get_jam"))
            else:
                msg = resp.json()
                flash(
                    message=f'{msg["msg"]} Status: {resp.status_code}', category="error"
                )
                return redirect(url_for("admin2.get_jam"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA WALI KELAS =====================================
    @admin2.route("data-wali-kelas")
    @login_required
    def get_wali():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/wali-kelas/get-all"
            resp = req.get(url)
            jsonResp = resp.json()

            form = FormWaliKelas(request.form)
            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + "" + i["last_name"])
                )

            urlKelas = base_url + "api/v2/master/kelas/get-all"
            respKelas = req.get(urlKelas)
            jsonRespKelas = respKelas.json()
            for i in jsonRespKelas["data"]:
                form.kelas.choices.append((i["id"], i["kelas"]))

            return render_template(
                "admin/master/wali_kelas/data_wali.html",
                model=jsonResp,
                form=form,
                jsonGuru=jsonRespGuru,
                jsonKelas=jsonRespKelas["data"],
            )
        else:
            abort(404)

    @admin2.route("tambah-wali", methods=["GET", "POST"])
    @login_required
    def add_wali():
        if current_user.group == "admin":
            form = FormWaliKelas(request.form)
            url = base_url + "api/v2/master/wali-kelas/create"
            if request.method == "POST":
                guru = form.namaGuru.data
                kelas = form.kelas.data
                payload = json.dumps({"guru_id": guru, "kelas_id": kelas})
                headers = {"Content-Type": "application/json"}
                resp = req.post(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 201:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="success",
                    )
                    return redirect(url_for("admin2.get_wali"))
                else:
                    flash(
                        message=f'{msg["msg"]} Status : {resp.status_code}',
                        category="error",
                    )
                    return redirect(url_for("admin2.get_wali"))
            else:
                flash(
                    f"Hak akses anda telah dicabut/berakhir. Silahkan login kembali",
                    "error",
                )
                abort(404)

    @admin2.route("update-wali/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_wali(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/wali-kelas/get-one/{id}"
            if request.method == "POST":
                guru_id = request.form.get("namaGuru")
                kelas_id = request.form.get("namaKelas")
                paylaod = json.dumps({"guru_id": guru_id, "kelas_id": kelas_id})
                headers = {"Content-Type": "application/json"}
                resp = req.put(url=url, data=paylaod, headers=headers)
                msg = resp.json()
                if resp.status_code == 200:
                    flash(f'{msg["msg"]} Status : {resp.status_code}', "info")
                    return redirect(url_for("admin2.get_wali"))
                else:
                    flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                    return redirect(url_for("admin2.get_wali"))
        else:
            abort(404)

    @admin2.route("delete-wali/<int:id>", methods=["GET", "POST"])
    @login_required
    def delete_wali(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/wali-kelas/get-one/{id}"

            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    f"Data wali kelas telah dihapus dari database. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_wali"))
            else:
                flash(
                    f"Terjadi kesalahan dalam memuat data. Status : {resp.status_code}",
                    "error",
                )
                return redirect(url_for("admin2.get_wali"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA GURU BK=====================================
    @admin2.route("data-guru-bk", methods=["GET"])
    @login_required
    def get_bk():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/guru-bk/get-all"
            resp = req.get(url)
            jsonResp = resp.json()
            form = FormGuruBK(request.form)
            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + "" + i["last_name"])
                )
            return render_template(
                "admin/master/guru_bk/data_guru_bk.html",
                model=jsonResp,
                form=form,
                jsonGuru=jsonRespGuru,
            )
        else:
            abort(404)

    @admin2.route("add-guru-bk", methods=["GET", "POST"])
    @login_required
    def add_bk():
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/guru-bk/create"
            guru_id = request.form.get("namaGuru")
            payload = json.dumps({"guru_id": guru_id})
            headers = {"Content-Type": "application/json"}
            resp = req.post(url=url, data=payload, headers=headers)

            msg = resp.json()
            if resp.status_code == 201:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "success")
                return redirect(url_for("admin2.get_bk"))
            else:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                return redirect(url_for("admin2.get_bk"))
        else:
            abort(404)

    @admin2.route("edit-guru-bk/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_bk(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/guru-bk/get-one/{id}"
            guru_id = request.form.get("namaGuru")
            payload = json.dumps({"guru_id": guru_id})
            headers = {"Content-Type": "application/json"}

            resp = req.put(url=url, data=payload, headers=headers)
            msg = resp.json()
            if resp.status_code == 200:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "info")
                return redirect(url_for("admin2.get_bk"))
            else:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                return redirect(url_for("admin2.get_bk"))
        else:
            abort(404)

    @admin2.route("delete-guru-bk/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_bk(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/guru-bk/get-one/{id}"

            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    f"Data Guru BK telah dihapus dari database. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_bk"))
            else:
                flash(f"Gagal memuat data. Status : {resp.status_code}", "error")
                return redirect(url_for("admin2.get_bk"))
        else:
            abort(404)

    # NOTE: ================== MASTER DATA KEPALA SEKOLAH =====================================
    @admin2.route("data-kepsek", methods=["GET"])
    @login_required
    def get_kepsek():
        if current_user.group == "admin":
            url = base_url + "api/v2/master/kepsek/get-all"
            resp = req.get(url)
            jsonResp = resp.json()
            form = FormKepsek(request.form)
            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + "" + i["last_name"])
                )

            # status = [{'0':'Tidak Aktif','1':'AKtif'}]
            status = [
                {"id": "0", "status": "tidak aktif"},
                {"id": "1", "status": "aktif"},
            ]

            return render_template(
                "admin/master/kepsek/data_kepsek.html",
                model=jsonResp,
                form=form,
                jsonGuru=jsonRespGuru,
                status=status,
            )
        else:
            abort(404)

    @admin2.route("add-kepsek", methods=["GET", "POST"])
    @login_required
    def add_kepsek():
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/kepsek/create"
            guru_id = request.form.get("namaGuru")
            payload = json.dumps({"guru_id": guru_id})
            headers = {"Content-Type": "application/json"}
            resp = req.post(url=url, data=payload, headers=headers)

            msg = resp.json()
            if resp.status_code == 201:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "success")
                return redirect(url_for("admin2.get_kepsek"))
            else:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                return redirect(url_for("admin2.get_kepsek"))
        else:
            abort(404)

    @admin2.route("edit-kepsek/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_kepsek(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/kepsek/get-one/{id}"
            guru_id = request.form.get("namaGuru")
            status = request.form.get("status")

            payload = json.dumps({"guru_id": guru_id, "status": status})
            headers = {"Content-Type": "application/json"}

            resp = req.put(url=url, data=payload, headers=headers)
            msg = resp.json()
            if resp.status_code == 200:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "info")
                return redirect(url_for("admin2.get_kepsek"))
            else:
                flash(f'{msg["msg"]} Status : {resp.status_code}', "error")
                return redirect(url_for("admin2.get_kepsek"))
        else:
            abort(404)

    @admin2.route("delete-kepsek/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_kepsek(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/kepsek/get-one/{id}"

            resp = req.delete(url=url)
            if resp.status_code == 204:
                flash(
                    f"Data Kepala Sekolah telah dihapus dari database. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_kepsek"))
            else:
                flash(f"Gagal memuat data. Status : {resp.status_code}", "error")
                return redirect(url_for("admin2.get_kepsek"))
        else:
            abort(404)


class JadwalMengajara:
    # NOTE: ================== DATA JADWAL MENGAAJAR =====================================
    @admin2.route("data-jawdwal-mengajar")
    @login_required
    def get_jadwal():
        if current_user.is_authenticated:
            if current_user.group == "admin":
                url = base_url + "api/v2/master/jadwal-mengajar/get-all"
                resp = req.get(url)
                jsonResp = resp.json()
                return render_template(
                    "admin/jadwal_mengajar/data_jadwal.html", model=jsonResp
                )
            else:
                abort(404)

    @admin2.route("tambah-jadwal-mengajar", methods=["GET", "POST"])
    @login_required
    def add_jadwal():
        if current_user.group == "admin" and current_user.is_authenticated:
            form = FormJadwalMengajar(request.form)
            kodeMengajar = "MPL-" + str(time.time()).rsplit(".", 1)[1]
            urlSemester = base_url + "api/v2/master/semester/get-all"
            respSemester = req.get(urlSemester)
            for i in respSemester.json()["data"]:
                if i["status"] == True:
                    sms = i["semester"]
                    sms_id = i["id"]

            urlTahunAjaran = base_url + "api/v2/master/ajaran/get-all"
            respTahunAjaran = req.get(urlTahunAjaran)
            for i in respTahunAjaran.json()["data"]:
                if i["status"] == True:
                    ta = i["th_ajaran"]
                    ta_id = i["id"]

            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + " " + i["last_name"])
                )

            urlMapel = base_url + "api/v2/master/mapel/get-all"
            respMapel = req.get(urlMapel)
            for i in respMapel.json()["data"]:
                form.namaMapel.choices.append((i["id"], i["mapel"].title()))

            urlHari = base_url + "api/v2/master/hari/get-all"
            respHari = req.get(urlHari)
            for i in respHari.json()["data"]:
                form.hari.choices.append((i["id"], i["hari"].title()))

            urlKelas = base_url + "api/v2/master/kelas/get-all"
            respKelas = req.get(urlKelas)
            for i in respKelas.json()["data"]:
                form.kelas.choices.append((i["id"], i["kelas"]))

            # urlJam = base_url + "api/v2/master/jam/get-all"
            # respJam = req.get(urlJam)
            # for i in respJam.json()["data"]:
            #     form.waktuMulai.choices.append((i["jam"], i["jam"]))
            #     form.waktuSelesai.choices.append((i["jam"], i["jam"]))

            form.kode.data = kodeMengajar
            form.semester.data = sms.title()
            form.ta.data = ta_id
            form.sms.data = sms_id
            form.tahunAjaran.data = ta

            if request.method == "POST" and form.validate_on_submit():
                kode_mengajar = request.form.get("kode")
                tahun_ajaran_id = request.form.get("ta")
                semeter_id = request.form.get("sms")
                guru_id = request.form.get("namaGuru")
                mapel_id = request.form.get("namaMapel")
                hari_id = request.form.get("hari")
                kelas_id = request.form.get("kelas")
                # jam_mulai = request.form.get("waktuMulai")
                # jam_selesai = request.form.get("waktuSelesai")
                jam_mulai2 = request.form.get("waktuMulai2")
                jam_selesai2 = request.form.get("waktuSelesai2")
                jam_ke = request.form.get("jamKe")

                url = base_url + "api/v2/master/jadwal-mengajar/create"
                payload = json.dumps(
                    {
                        "kode_mengajar": kode_mengajar,
                        "tahun_ajaran_id": tahun_ajaran_id,
                        "semeter_id": semeter_id,
                        "guru_id": guru_id,
                        "mapel_id": mapel_id,
                        "hari_id": hari_id,
                        "kelas_id": kelas_id,
                        "jam_mulai": jam_mulai2,
                        "jam_selesai": jam_selesai2,
                        "jam_ke": jam_ke,
                    }
                )
                headers = {"Content-Type": "application/json"}

                resp = req.post(url=url, data=payload, headers=headers)
                msg = resp.json()
                if resp.status_code == 201:
                    flash(f'{msg["msg"]} Status : {resp.status_code}', "success")
                    return redirect(url_for("admin2.get_jadwal"))
                else:
                    flash(f'{msg["msg"]} Status : {resp.status_code}')
                    return redirect(url_for("admin2.get_jadwal", "error"))

            return render_template(
                "admin/jadwal_mengajar/tambah_jadwal.html", form=form
            )
        else:
            abort(404)

    @admin2.route("edit-jadwal/<int:id>", methods=["GET", "POST"])
    def edit_jadwal(id):
        if current_user.group == "admin":
            form = FormJadwalMengajar(request.form)
            url = base_url + f"api/v2/master/jadwal-mengajar/get-one/{id}"
            respGet = req.get(url)
            jsonResp = respGet.json()

            urlGuru = base_url + "api/v2/guru/get-all"
            respGuru = req.get(urlGuru)
            jsonRespGuru = respGuru.json()
            for i in jsonRespGuru:
                form.namaGuru.choices.append(
                    (i["id"], i["first_name"] + " " + i["last_name"])
                )

            urlMapel = base_url + "api/v2/master/mapel/get-all"
            respMapel = req.get(urlMapel)
            for i in respMapel.json()["data"]:
                form.namaMapel.choices.append((i["id"], i["mapel"].title()))

            urlHari = base_url + "api/v2/master/hari/get-all"
            respHari = req.get(urlHari)
            for i in respHari.json()["data"]:
                form.hari.choices.append((i["id"], i["hari"].title()))

            urlKelas = base_url + "api/v2/master/kelas/get-all"
            respKelas = req.get(urlKelas)
            for i in respKelas.json()["data"]:
                form.kelas.choices.append((i["id"], i["kelas"]))

            # urlJam = base_url + "api/v2/master/jam/get-all"
            # respJam = req.get(urlJam)
            # for i in respJam.json()["data"]:
            #     form.waktuMulai.choices.append((i["jam"], i["jam"]))
            #     form.waktuSelesai.choices.append((i["jam"], i["jam"]))

            form.kode.default = jsonResp["kode_mengajar"]
            form.tahunAjaran.default = jsonResp["tahun_ajaran"]
            form.namaGuru.default = jsonResp["guru_id"]
            form.semester.default = jsonResp["semester"].upper()
            form.namaMapel.default = jsonResp["mapel_id"]
            form.hari.default = jsonResp["hari_id"]
            form.kelas.default = jsonResp["kelas_id"]
            form.waktuMulai2.default = jsonResp["jam_mulai"]
            form.waktuSelesai2.default = jsonResp["jam_selesai"]
            form.jamKe.default = jsonResp["jam_ke"]
            form.process()

            if request.method == "POST":
                guru_id = request.form.get("namaGuru")
                mapel_id = request.form.get("namaMapel")
                hari_id = request.form.get("hari")
                jam_mulai = request.form.get("waktuMulai2")
                jam_selesai = request.form.get("waktuSelesai2")
                kelas_id = request.form.get("kelas")
                jam_ke = request.form.get("jamKe")

                payload = json.dumps(
                    {
                        "guru_id": guru_id,
                        "hari_id": hari_id,
                        "mapel_id": mapel_id,
                        "jam_mulai": jam_mulai,
                        "jam_selesai": jam_selesai,
                        "kelas_id": kelas_id,
                        "jam_ke": jam_ke,
                    }
                )

                headers = {"Content-Type": "application/json"}

                resp = req.put(url=url, data=payload, headers=headers)

                jsonRespPut = resp.json()

                if resp.status_code == 200:
                    flash(f'{jsonRespPut["msg"]} Status : {resp.status_code}', "info")
                    return redirect(url_for("admin2.get_jadwal"))
                else:
                    flash(
                        f"Terjadi kesalahan dalam perbaharui data. Status : {resp.status_code}"
                    )

            return render_template(
                "admin/jadwal_mengajar/edit_jadwal.html", model=jsonResp, form=form
            )

    @admin2.route("delete-jadwal/<int:id>", methods=["GET", "DELETE"])
    @login_required
    def delete_jadwal(id):
        if current_user.group == "admin":
            url = base_url + f"api/v2/master/jadwal-mengajar/get-one/{id}"
            resp = req.delete(url)

            if resp.status_code == 204:
                flash(
                    f"Data Jadwal Pelajaran telah dibatalkan. Status : {resp.status_code}",
                    "info",
                )
                return redirect(url_for("admin2.get_jadwal"))
            else:
                flash(
                    f"Gala memuat Data Jadwal Pelajaran. Status : {resp.status_code}",
                    "error",
                )
                return redirect(url_for("admin2.get_jadwal"))
        else:
            abort(404)


"""
NOTE : DATABASE DIRECT NO API
"""


@admin2.route("/data-kehadiran/bulan", methods=["GET", "POST"])
@login_required
def data_kehadiran_bulan():
    if current_user.group == "admin":
        base_kelas = BaseModel(KelasModel)
        kelas = base_kelas.get_all()
        base_bulan = BaseModel(NamaBulanModel)
        bulan = base_bulan.get_all()
        sql_absen = AbsensiModel.query.group_by(AbsensiModel.tgl_absen).all()

        form = FormSelectAbsensi()
        # data kelas
        for i in kelas:
            form.kelas.choices.append((i.id, i.kelas))
        # data bulan
        for i in bulan:
            form.bulan.choices.append((i.id, i.nama_bulan.title()))

        for i in sql_absen:
            form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))

        if request.method == "POST" and form.validate_on_submit():
            kelas_id = request.form.get("kelas")
            bulan_id = request.form.get("bulan")
            tahun = request.form.get("tahun")

            sql_kehadiran = (
                db.session.query(AbsensiModel)
                .join(SiswaModel)
                .join(MengajarModel)
                .filter(AbsensiModel.siswa_id == SiswaModel.user_id)
                .filter(func.month(AbsensiModel.tgl_absen) == bulan_id)
                .filter(func.year(AbsensiModel.tgl_absen) == tahun)
                .filter(SiswaModel.kelas_id == kelas_id)
                .group_by(AbsensiModel.siswa_id)
                .order_by(AbsensiModel.siswa_id.asc())
                .all()
            )
            sql_keterangan = db.session.query(AbsensiModel)

            data = {}
            data["bulan"] = base_bulan.get_one(id=bulan_id).nama_bulan
            for i in sql_kehadiran:
                data["kelas"] = i.siswa.kelas.kelas
                data["tahun_ajaran"] = i.mengajar.tahun_ajaran.th_ajaran
                data["semester"] = i.mengajar.semester.semester

            this_year = datetime.date(datetime.today())
            data["tahun"] = this_year.year
            date_in_month = monthrange(
                int(
                    this_year.year,
                ),
                int(bulan_id),
            )
            data["month_range"] = date_in_month[1]

            return render_template(
                "admin/absensi/result_daftar_hadir.html",
                sql_kehadiran=sql_kehadiran,
                data=data,
                sql_ket=sql_keterangan,
                func=func,
                AbsensiModel=AbsensiModel,
            )

        return render_template(
            "admin/absensi/daftar_hadir_siswa.html",
            kelas=kelas,
            bulan=bulan,
            form=form,
        )
    else:
        return abort(404)


@admin2.route("data-kehadiran/semester")
@login_required
def data_kehadiran_semester():
    if current_user.group == "admin":
        form = FormSelectKehadiranSemester()
        sql_kelas = BaseModel(KelasModel).get_all()
        sql_semester = BaseModel(SemesterModel).get_all()

        for i in sql_kelas:
            form.kelas.choices.append((i.id, i.kelas))

        for i in sql_semester:
            form.semester.choices.append((i.id, i.semester.upper()))
        return render_template("admin/absensi/daftar_hadir_semester.html", form=form)
    else:
        return abort(404)


@admin2.route("surat-pernyataan/pilih-kelas", methods=["GET", "POST"])
@login_required
def select_siswa():
    if current_user.group == "admin":
        base_kelas = BaseModel(KelasModel)
        sql_kelas = base_kelas.get_all()
        form = FormSelectKelas()
        for i in sql_kelas:
            form.kelas.choices.append((i.id, i.kelas))

        data = {}

        if form.validate_on_submit():
            kelas = request.form.get("kelas")
            base_siswa = BaseModel(SiswaModel)
            sql_siswa = base_siswa.get_all_filter_by(kelas_id=kelas)
            for i in sql_siswa:
                data["kelas"] = i.kelas.kelas

            return render_template(
                "admin/siswa/get_siswa_by_kelas.html", model=sql_siswa, data=data
            )

        return render_template("admin/letter_report/select_kelas.html", form=form)
    else:
        return abort(404)


@admin2.route("surat-pernyataan", methods=["GET", "POST"])
@login_required
def surat_pernyataan():
    try:
        if current_user.group == "admin":
            base_siswa = BaseModel(SiswaModel)
            id = request.args.get(key="siswa_id", type=int)
            sql_siswa = base_siswa.get_one(id=id)
            today = datetime.date(datetime.today())
            sql_wali = BaseModel(WaliKelasModel).get_one(kelas_id=sql_siswa.kelas_id)
            print(sql_wali)
            return render_template(
                "arsip/surat_pernyataan.html",
                sql_siswa=sql_siswa,
                today=today,
                sql_wali=sql_wali,
            )
        else:
            return abort(404)
    except Exception as e:
        return e
