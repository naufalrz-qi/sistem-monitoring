import json
from msvcrt import getwch
from flask import (
    Blueprint,
    Response,
    request,
    redirect,
    send_from_directory,
    url_for,
    render_template,
    flash,
)
from app.backend.lib.status_code import HTTP_413_REQUEST_ENTITY_TOO_LARGE
from app.backend.models.user_model import *
from app.backend.models.user_details_model import *
from app.backend.lib.base_model import BaseModel
from werkzeug.utils import secure_filename
from app.frontend.forms.form_auth import FormEditStatus
from app.frontend.forms.form_siswa import FormAddSiswa, FormEditSiswa
from ..forms.form_auth import *
from ..forms.form_guru import *
import os
import requests as req
import io
import xlwt

staff = Blueprint("staff", __name__, template_folder="../templates/", url_prefix="/")


@staff.route("/staff/<path:filename>")
def static(filename):
    dir = send_from_directory("frontend/static", filename)
    return dir


@staff.route("/")
def index():
    return render_template("staff/index_staff.html")


class Siswa:
    @staff.route("/data-siswa")
    def get_siswa():
        base_url = request.url_root
        url = base_url + url_for("siswa.get")
        r = req.get(url)
        data = r.json()
        # NOTE: GET KELAS
        base_kelas = request.url_root
        url_kelas = base_kelas + url_for("master.kelas_all")
        resp_kelas = req.get(url_kelas)
        json_kelas = resp_kelas.json()
        return render_template(
            "staff/data_pengguna/siswa/data_siswa.html",
            model=data,
            jsonKelas=json_kelas,
        )

    @staff.route("/generate-qc", methods=["GET", "PUT"])
    def generate_qc():
        base_url = request.url_root
        id = request.args.get("id")
        url = base_url + url_for("siswa.generate_qc", id=id)
        headers = {"Content-Type": "application/json"}
        r = req.put(url, headers=headers)
        if r.status_code == 200:
            flash(
                message=f"Generate QR kode berhasil. Status : {r.status_code}",
                category="success",
            )
            return redirect(url_for("staff.get_siswa"))
        else:
            flash(
                message=f"Maaf terjadi kesalahan dalam generate QR CODE. Status : {r.status_code}",
                category="error",
            )
            return redirect(url_for("staff.get_siswa"))

    # NOTE:  UPLOAD FOTO
    @staff.post("/upload-photo")
    # @staff.route('/upload-photo', methods=['GET','PUT','POST'])
    def upload_foto():
        base_url = request.url_root
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
            return redirect(url_for("staff.get_siswa"))
        else:
            return f"<p>error : {response.status_code}</p>"

    @staff.errorhandler(413)
    def request_entity_too_large(error):
        return "File Upload Maks 2MB", HTTP_413_REQUEST_ENTITY_TOO_LARGE

    # NOTE:  TAMBAH DATA SISWA
    @staff.route("/add-siswa", methods=["GET", "POST"])
    def add_siswa():
        base = request.url_root
        # get kelas
        url_kelas = base + f"/api/v2/master/kelas/get-all"
        get_kelas = req.get(url_kelas)
        data = get_kelas.json()
        kelas = [("", "..::Select::..")]
        for _ in data["data"]:
            kelas.append((_["id"], _["kelas"]))

        url = base + f"/api/v2/auth/create"
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
                }
            )
            headers = {"Content-Type": "application/json"}
            response = req.post(url=url, headers=headers, data=payload)
            if response.status_code == 201:
                flash(message="Berhasil...", category="success")
                return redirect(url_for("staff.get_siswa"))
            elif response.status_code == 409:
                flash(
                    message="NISN sudah yang di input, telah terdaftar",
                    category="error",
                )
            else:
                return render_template(
                    "staff/data_pengguna/siswa/tambah_siswa.html", form=form
                )
        return render_template("staff/data_pengguna/siswa/tambah_siswa.html", form=form)

    # NOTE:  UPDATE DATA SISWA
    @staff.route("/update-siswa/<int:id>", methods=["GET", "POST", "PUT"])
    def update_siswa(id):
        form = FormEditSiswa()
        base = request.url_root
        # GET KELAS
        url_kelas = base + f"/api/v2/master/kelas/get-all"
        get_kelas = req.get(url_kelas)
        list_kelas = get_kelas.json()["data"]
        choices = [("", "..:: SELECT ::..")]
        for _ in list_kelas:
            # form.kelas.choices.append((_["id"], _["kelas"]))
            choices.append((_["id"], _["kelas"]))
        form.kelas.choices = choices
        baseModel = BaseModel(SiswaModel)
        getOne = baseModel.get_one_or_none(user_id=id)
        # GET SINGLE DATA
        url_obj = base + f"api/v2/student/single/{id}"
        resp_obj = req.get(url=url_obj)
        json_resp = resp_obj.json()
        form.nisn.default = json_resp["nisn"]
        form.fullname.default = json_resp["first_name"] + " " + json_resp["last_name"]
        form.kelas.default = next(
            obj["id"] for obj in list_kelas if json_resp["kelas"] in obj["kelas"]
        )
        form.jenisKelamin.default = json_resp["gender"].lower()
        form.tempatLahir.default = json_resp["tempat_lahir"]
        """
        NOTE: Convert str to datetime.date
        buat logika jika string tgl ada maka convert ke datetime.strptime(str_date, format).date
        jika tidak maka tetapkan string tgl default '2000-10-10' agar tidak terjadi error
        """
        from_date = json_resp["tgl_lahir"] if json_resp["tgl_lahir"] else "2000-10-10"
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
            print(f"payload = {payload}")
            response_update = req.put(url_obj, headers=headers, data=payload)

            if response_update.status_code == 200:
                flash(f"Data dari {first_name} telah berhasil diperbaharui.", "success")
                return redirect(url_for("staff.get_siswa"))
            else:
                flash(
                    f"Terjadi kesalahan dalam memuat data. statu : {response_update.status_code}",
                    "error",
                )
                return render_template(
                    "staff/data_pengguna/siswa/edit_siswa.html",
                    form=form,
                    obj=json_resp,
                )
        return render_template(
            "staff/data_pengguna/siswa/edit_siswa.html", form=form, obj=json_resp
        )

    # NOTE:  DELETE DATA SISWA
    @staff.route("/delete-siswa/<int:id>", methods=["GET", "POST", "DELETE"])
    def delete_siswa(id):
        base = request.url_root
        url = base + f"/api/v2/student/single/{id}"

        response = req.delete(url)
        if response.status_code == 204:
            flash(message="Data siswa telah berhasil di hapus.", category="success")
            return redirect(url_for("staff.get_siswa"))
        else:
            flash("Ada tejadi kesalahan dalam menghapus data.", "error")
            return redirect(url_for("staff.get_siswa"))

    # eksport data
    @staff.route("/export-siswa")
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
class Guru:
    @staff.route("data-guru")
    def get_guru():
        base = request.url_root
        url = base + "api/v2/guru/get-all"
        response = req.get(url)
        json_resp = response.json()

        return render_template(
            "staff/data_pengguna/guru/data_guru.html", model=json_resp
        )
    
    @staff.route('update-guru/<int:id>', methods=['POST','GET'])
    def update_guru(id):
        form = FormEditGuru(request.form)
        base = request.url_root
        # NOTE: GET SINGLE OBJECT
        url_obj = base + f'api/v2/guru/single/{id}'
        resp_obj = req.get(url=url_obj)
        jsonObj = resp_obj.json()
        
        # NOTE : GET ALL MAPEL
        url_mapel = base + f'api/v2/master/mapel/get-all'
        resp_mapel = req.get(url=url_mapel)
        jsonMapel = resp_mapel.json()['data']
        # FORM SET CHOICES
        for _ in jsonMapel:
            form.mapel.choices.append((_['id'], _['mapel']))
        # FORM DEFAULT VALUE
        form.nip.default = jsonObj['nip']
        form.fullname.default = jsonObj['first_name'] + ' ' + jsonObj['last_name']
        form.mapel.default = jsonObj['mapel_id']
        form.jenisKelamin.default = jsonObj['gender'].lower()
        form.agama.default = jsonObj['agama'].lower()
        form.alamat.default = jsonObj['alamat']
        form.telp.default = jsonObj['telp']
        form.process()
        
        # NOTE: REQUEST FORM TO SAVE CHANGES
        if request.method == 'POST':
            nip = request.form.get('nip')
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
            mapel = request.form.get('mapel')
            gender = request.form.get('jenisKelamin')
            agama = request.form.get('agama')
            alamat = request.form.get('alamat')
            telp = request.form.get('telp')
            
            # HEADERS, DATA TO RESPONSE
            payload = json.dumps(
                {
                    'nip': nip,
                    'first_name': first_name,
                    'last_name': last_name,
                    'mapel': mapel,
                    'gender': gender,
                    'agama': agama,
                    'alamat': alamat,
                    'telp': telp
                }
            )
            headers = {"Content-Type": "application/json"}
            
            resp_obj = req.put(url=url_obj, data=payload, headers=headers)
            msg = resp_obj.json()
            if resp_obj.status_code == 200:
                flash(f'{msg}, status : {resp_obj.status_code}', 'success')
                return redirect(url_for('staff.get_guru'))
            else:
                flash(f'{msg}. Status : {resp_obj.status_code}', 'error')
            return render_template('staff/data_pengguna/guru/edit_guru.html', form=form)
        return render_template('staff/data_pengguna/guru/edit_guru.html', form=form)
    
    @staff.route('delete-guru/<id>', methods=['GET','DELETE','POST'])
    def delete_guru(id):
        base = request.url_root
        url = base + f'api/v2/guru/single/{id}'
        response = req.delete(url=url)

        if response.status_code == 204:
            flash(message=f'Data guru telah berhasil di hapus. Status : {response.status_code}', category='info')
            return redirect(url_for('staff.get_guru'))
        else:
            flash(message=f'Terjadi kesalahan dalama memuat data. Status : {response.status_code}', category='info')
            return redirect(url_for('staff.get_guru'))
            
        


class User:
    @staff.route("/data-user")
    def get_user():
        base = request.url_root
        url = base + f'api/v2/auth/get-all'
        response = req.get(url)
        json_resp = response.json()
        form = FormEditStatus()
        formUpdatePassword = FormEditPassword()
        return render_template(
            "staff/data_pengguna/data_user.html",
            user=json_resp,
            form=form,
            formPassword=formUpdatePassword,
        )

    @staff.post("/edit-status/<int:id>")
    def update_status(id):
        base = request.url_root
        url = base + f"api/v2/auth/edit-status?id={id}"

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
                return redirect(url_for("staff.get_user"))
            else:
                return redirect(url_for("staff.get_user"))

    @staff.post("edit-pswd/<int:id>")
    def update_password(id):
        base = request.url_root
        url = base + f"api/v2/auth/edit-password?id={id}"

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
                return redirect(url_for("staff.get_user"))
            elif response.status_code == 400:
                flash(f'Error: {msg["msg"]}, status : {response.status_code}', "error")
                return redirect(url_for("staff.get_user"))
            else:
                flash(
                    f"Error: Terjadi kesalahan dalam memuat data, status : {response.status_code}",
                    "error",
                )
                return redirect(url_for("staff.get_user"))


class TestPage:
    @staff.get("test-page")
    def test_page():
        return render_template("test_page.html")
