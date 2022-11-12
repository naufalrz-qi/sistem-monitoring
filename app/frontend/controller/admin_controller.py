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
from app.frontend.forms.form_master import *
from app.frontend.forms.form_siswa import FormAddSiswa, FormEditSiswa
from ..forms.form_auth import *
from ..forms.form_guru import *
from ..lib.base_url import base_url
import os
import requests as req
import io
import xlwt

admin2 = Blueprint("admin2", __name__, template_folder="../templates/", url_prefix="/")


@admin2.route("/admin/<path:filename>")
def static(filename):
    dir = send_from_directory("frontend/static", filename)
    return dir


@admin2.route("/")
def index():
    return render_template("admin/index_admin.html")


class PenggunaSiswa:
    @admin2.route('get-siswa')
    def getSiswa():
        urlKelas = base_url + 'api/v2/master/kelas/get-all'
        respKelas = req.get(urlKelas)
        jsonRespKelas = respKelas.json()
        
        urlSiswa = base_url + url_for('siswa.get')
        respSiswa = req.get(urlSiswa)
        jsonRespSiswa = respSiswa.json()
        return render_template('admin/siswa/get_siswa.html', kelas=jsonRespKelas, siswa=jsonRespSiswa)
    
    @admin2.route("/data-siswa")
    def get_siswa():
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

    @admin2.route("/generate-qc", methods=["GET", "PUT"])
    def generate_qc():
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

    # NOTE:  UPLOAD FOTO
    @admin2.post("/upload-photo")
    # @admin2.route('/upload-photo', methods=['GET','PUT','POST'])
    def upload_foto():
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
            return redirect(url_for("admin2.getSiswa"))
            # return redirect(url_for("admin2.get_siswa"))
        else:
            return f"<p>error : {response.status_code}</p>"

    @admin2.errorhandler(413)
    def request_entity_too_large(error):
        return "File Upload Maks 2MB", HTTP_413_REQUEST_ENTITY_TOO_LARGE

    # NOTE:  TAMBAH DATA SISWA
    @admin2.route("/add-siswa", methods=["GET", "POST"])
    def add_siswa():
        
        # get kelas
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
            telp = request.form.get('telp')

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
                    "telp": telp
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

    # NOTE:  UPDATE DATA SISWA
    @admin2.route("/update-siswa/<int:id>", methods=["GET", "POST", "PUT"])
    def update_siswa(id):
        form = FormEditSiswa()
        
        # GET KELAS
        url_kelas = base_url + f"/api/v2/master/kelas/get-all"
        get_kelas = req.get(url_kelas)
        list_kelas = get_kelas.json()["data"]
        choices = [("", "..:: SELECT ::..")]
        for _ in list_kelas:
            # form.kelas.choices.append((_["id"], _["kelas"]))
            choices.append((_["id"], _["kelas"]))
        form.kelas.choices = choices
        # baseModel = BaseModel(SiswaModel)
        # getOne = baseModel.get_one_or_none(user_id=id)
        # GET SINGLE DATA
        url_obj = base_url + f"api/v2/student/single/{id}"
        
        resp_obj = req.get(url=url_obj)
        json_resp = resp_obj.json()
        kelasId = json_resp['kelas_id']
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
            response_update = req.put(url_obj, headers=headers, data=payload)
            if response_update.status_code == 200:
                baseKelasAfter = base_url + f'api/v2/master/kelas/update-jumlah/{kelas}'
                updateJumlahSiswaAfter = req.put(url=baseKelasAfter, headers=headers)
                baseKelasBefore = base_url + f'api/v2/master/kelas/update-jumlah/{kelasId}'
                updateJumlahSiswaAfter = req.put(url=baseKelasBefore, headers=headers)
                flash(f"Data dari {first_name} telah berhasil diperbaharui.", "info")
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

    # NOTE:  DELETE DATA SISWA
    @admin2.route("/delete-siswa/<int:id>", methods=["GET", "POST", "DELETE"])
    def delete_siswa(id):
        url = base_url + f"/api/v2/student/single/{id}"
        respGetSiswa = req.get(url)
        jsonResp = respGetSiswa.json()
        kelasId = jsonResp['kelas_id']
        
        baseKelas = base_url + f'api/v2/master/kelas/update-jumlah/{kelasId}'
        headers = {"Content-Type": "application/json"}
        

        response = req.delete(url)
        if response.status_code == 204:
            respkelas = req.put(url=baseKelas, headers=headers)
            print(respkelas.text)
            flash(message="Data siswa telah berhasil di hapus.", category="info")
            return redirect(url_for("admin2.getSiswa"))
            # return redirect(url_for("admin2.get_siswa"))
        else:
            flash("Ada tejadi kesalahan dalam menghapus data.", "error")
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
    def get_guru():
        url = base_url + "api/v2/guru/get-all"
        response = req.get(url)
        json_resp = response.json()

        return render_template(
            "admin/guru/data_guru.html", model=json_resp
        )

    @admin2.route("tambah-data", methods=["GET", "POST"])
    def add_guru():
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
                return render_template(
                    "admin/guru/tambah_guru.html", form=form
                )
        return render_template("admin/guru/tambah_guru.html", form=form)

    @admin2.route("update-guru/<int:id>", methods=["POST", "GET"])
    def update_guru(id):
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

    @admin2.route("delete-guru/<id>", methods=["GET", "DELETE", "POST"])
    def delete_guru(id):
        
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


class PenggunaUser:
    @admin2.route("/data-user")
    def get_user():
        
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

    @admin2.post("/edit-status/<int:id>")
    def update_status(id):
        
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

    @admin2.post("edit-pswd/<int:id>")
    def update_password(id):
        
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
                flash(f'Error: {msg["msg"]}, status : {response.status_code}', "error")
                return redirect(url_for("admin2.get_user"))
            else:
                flash(
                    f"Error: Terjadi kesalahan dalam memuat data, status : {response.status_code}",
                    "error",
                )
                return redirect(url_for("admin2.get_user"))


  

# NOTE: MASTER DATA 
class MasterData:
    # NOTE: ================== MASTER DATA MAPEL =====================================
    @admin2.get("data-mapel")
    def get_mapel():
        url = base_url + f"api/v2/master/mapel/get-all"
        response = req.get(url)
        jsonRespon = response.json()
        return render_template("admin/master/mapel/data_mapel.html", model=jsonRespon)

    @admin2.route("add-mapel", methods=["POST", "GET"])
    def add_mapel():
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

    @admin2.route("edit-mapel/<int:id>", methods=["GET", "POST"])
    def edit_mapel(id):
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
                return render_template("admin/master/mapel/edit_mapel.html", form=form)
        return render_template("admin/master/mapel/edit_mapel.html", form=form)

    @admin2.route("delete-mapel/<int:id>", methods=["GET", "DELETE"])
    def delete_mapel(id):
        URL = base_url + f"api/v2/master/mapel/get-one/{id}"
        response = req.delete(URL)
        if response.status_code == 204:
            flash(
                message=f"Data mapel telah di hapus dari database. Status : {response.status_code}",
                category="info",
            )
            return redirect(url_for('admin2.get_mapel'))
        elif response.status_code == 404:
            msg = response.json()
            flash(
                message=f"{msg['msg']} : {response.status_code}",
                category="info",
            )        
            return redirect(url_for('admin2.get_mapel'))
        
            
    # NOTE: ================== MASTER DATA SESMESTER =====================================
    @admin2.get('data-semester')
    def get_semester():
        URL = base_url + f'api/v2/master/semester/get-all'
        response = req.get(URL)
        jsonResp = response.json()
        return render_template('admin/master/semester/data_semester.html', model=jsonResp)
    
    @admin2.route('add-semester', methods=['GET', 'POST'])
    def add_semester():
        form = FormSemester(request.form)
        URL = base_url + f'api/v2/master/semester/create'
        if request.method == 'POST' and form.validate_on_submit():
            semester = form.semester.data
            status = form.status.data
            
            payload = json.dumps({
                'semester': semester,
                'status': status
            })
            headers = {'Content-Type': 'application/json'}
            response = req.post(url=URL, data=payload, headers=headers)
            msg = response.json()
            
            if response.status_code == 201:
                flash(message=f'{msg["msg"]} Status: {response.status_code}', category='success')
                return redirect(url_for('admin2.get_semester'))
            else:
                flash(message=f'{msg["msg"]} Status: {response.status_code}', category='error')
                return render_template('admin/master/semester/tambah_semester.html', form=form)
            
        return render_template('admin/master/semester/tambah_semester.html', form=form)
    
    @admin2.route('edit-semester/<int:id>', methods=['GET','POST'])
    def edit_semester(id):
        form = FormEditSemester(request.form)
        URL = base_url + f'api/v2/master/semester/get-one/{id}'
        responseGet = req.get(url=URL)
        jsonResp = responseGet.json()
        form.status.data = '1' if jsonResp['status'] == True else '0'
        
        if request.method == 'POST' and form.validate_on_submit():
            status = request.form.get('status')
            payload = json.dumps({
                'status': status
            })
            headers = {'Content-Type': 'application/json'}
            response = req.put(url=URL, data=payload, headers=headers)
            msg = response.json()
            
            if response.status_code == 200:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='info')
                return redirect(url_for('admin2.get_semester'))
            else:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='error')
                return render_template('admin/master/semester/edit_semester.html', form=form)
        return render_template('admin/master/semester/edit_semester.html', form=form)

    @admin2.route('delete-semester/<int:id>', methods=['DELETE','GET'])
    def delete_semester(id):
        URL = base_url + f'api/v2/master/semester/get-one/{id}'
        response = req.delete(URL)
        if response.status_code == 204:
            flash(
                message=f"Data semester telah di hapus dari database. Status : {response.status_code}",
                category="info",
            )
            return redirect(url_for('admin2.get_semester'))
        
        
    # NOTE: ================== MASTER DATA TAHUN AJARAN =====================================
    @admin2.route('data-tahun-ajaran')
    def get_ajaran():
        URL = base_url + 'api/v2/master/ajaran/get-all'
        response = req.get(URL)
        jsonResp = response.json()
        return render_template('admin/master/tahun_ajaran/data_tahun_ajaran.html', model=jsonResp)
    
    @admin2.route('add-tahun-ajaran', methods=['GET','POST'])
    def add_ajaran():
        form = FormTahunAJaran(request.form)
        URL = base_url + 'api/v2/master/ajaran/create'
        
        if request.method == 'POST' and form.validate_on_submit():
            ajaran = form.tahunAjaran.data
            status = form.status.data
            
            payload = json.dumps({
                'ajaran': ajaran,
                'status': status
            })
            headers = {'Content-Type': 'application/json'}
            response = req.post(url=URL, data=payload, headers=headers)
            msg=response.json()
            
            if response.status_code == 201:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='success')
                return redirect(url_for('admin2.get_ajaran'))
            else:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='error')
                return render_template('admin/master/tahun_ajaran/tambah_tahun_ajaran.html', form=form)
        return render_template('admin/master/tahun_ajaran/tambah_tahun_ajaran.html', form=form)

    @admin2.route('edit-tahun-ajaran/<int:id>', methods=['GET','POST'])
    def edit_ajaran(id):
        form = FormTahunAJaran(request.form)
        URL = base_url + f'api/v2/master/ajaran/get-one/{id}'
        response = req.get(URL)
        jsonResp = response.json()
        form.tahunAjaran.data = jsonResp['ajaran']
        form.status.data = '1' if jsonResp['status'] == True else '0'
        
        if request.method == 'POST' and form.validate_on_submit():
            ajaran = request.form.get('tahunAjaran')
            status = request.form.get('status')
            payload = json.dumps({
                'ajaran' : ajaran,
                'status' : status
            })
            headers = {'Content-Type': 'application/json'}
            response = req.put(url=URL, data=payload, headers=headers)
            msg = response.json()
            if response.status_code == 200:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='info')
                return redirect(url_for('admin2.get_ajaran'))
            else:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='error')
                return render_template('admin/master/tahun_ajaran/edit_tahun_ajaran.html', form=form)
                
        return render_template('admin/master/tahun_ajaran/edit_tahun_ajaran.html', form=form)
    
    @admin2.route('delete-tahun-ajaran/<int:id>', methods=['GET','DELETE'])
    def delete_ajaran(id):
        URL = base_url + f'api/v2/master/ajaran/get-one/{id}'
        response = req.delete(URL)
        if response.status_code == 204:
            flash(message=f'Data Tahun Ajaran telah dihapus dari database. Status : {response.status_code}', category='info')
            return redirect(url_for('admin2.get_ajaran'))
    
    
    # NOTE: ================== MASTER DATA KELAS =====================================
    @admin2.route('data-kelas')
    def get_kelas():
        URL = base_url + 'api/v2/master/kelas/get-all'
        response = req.get(URL)
        jsonResp = response.json()
        return render_template('admin/master/kelas/data_kelas.html', model=jsonResp)
    
    @admin2.route('add-kelas', methods=['GET','POST'])
    def add_kelas():
        form = FormKelas(request.form)
        URL = base_url + 'api/v2/master/kelas/create'
        
        if request.method == 'POST' and form.validate_on_submit():
            kelas = form.kelas.data 
            
            payload = json.dumps({
                'kelas': kelas
            })
            headers = {'Content-Type': 'application/json'}
            response = req.post(url=URL, data=payload, headers=headers)
            msg = response.json()
            if response.status_code == 201:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='success')
                return redirect(url_for('admin2.get_kelas'))
            else:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='error')
                return render_template('admin/master/kelas/tambah_kelas.html', form=form)
        return render_template('admin/master/kelas/tambah_kelas.html', form=form)
    
    @admin2.route('edit-kelas/<int:id>', methods=['GET', 'POST'])
    def edit_kelas(id):
        form = FormEditKelas(request.form)
        URL = base_url + f'api/v2/master/kelas/get-one/{id}'
        
        response = req.get(URL)
        jsonResp = response.json()
        form.kelas.data = jsonResp['kelas']
        form.jumlahLaki.data = jsonResp['laki']
        form.jumlahPerempuan.data = jsonResp['perempuan']
        form.jumlahSiswa.data = jsonResp['seluruh']
        
        if request.method == 'POST':
            kelas = request.form.get('kelas')
            laki = request.form.get('jumlahLaki')
            perempuan = request.form.get('jumlahPerempuan')
            seluruh = request.form.get('jumlahSiswa')
            
            payload = json.dumps({
                'kelas': kelas,
                'laki': laki,
                'perempuan': perempuan,
                'seluruh': seluruh
            })
            headers = {'Content-Type': 'application/json'}
            
            response = req.put(url=URL, data=payload, headers=headers)
            msg = response.json()
            
            if response.status_code == 200:
                flash(f'{msg["msg"]} Status : {response.status_code}', 'info')
                return redirect(url_for('admin2.get_kelas'))
            else:
                flash(f'{msg["msg"]} Status : {response.status_code}', 'error')
                return render_template('admin/master/kelas/edit_kelas.html', form=form)
        return render_template('admin/master/kelas/edit_kelas.html', form=form)
    
    @admin2.route('delete-kelas/<int:id>', methods=['GET','DELETE'])
    def delete_kelas(id):
        URL = base_url + f'api/v2/master/kelas/get-one/{id}'
        response = req.delete(URL)
        if response.status_code == 204:
            flash(f'Data kelas telah dihpus dari database. Status : {response.status_code}', 'info')
            return redirect(url_for('admin2.get_kelas'))
    
    # NOTE: ================== MASTER DATA HARI =====================================
    @admin2.route('data-hari')
    def get_hari():
        URL = base_url + 'api/v2/master/hari/get-all'
        response = req.get(URL)
        jsonResp = response.json()        
        return render_template('admin/master/hari/data_hari.html', model=jsonResp)
    
    @admin2.route('add-hari', methods=['GET','POST'])
    def add_hari():
        URL = base_url + 'api/v2/master/hari/create'
        form = FormHari(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            hari = form.hari.data
            
            payload = json.dumps({
                'hari': hari
            })
            headers = {'Content-Type': 'application/json'}
            response = req.post(url=URL, data=payload, headers=headers)
            msg = response.json()
            if response.status_code == 201:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='success')
                return redirect(url_for('admin2.get_hari'))
            else:
                flash(message=f'{msg["msg"]} Status : {response.status_code}', category='error')
                return render_template('admin/master/hari/tambah_hari.html', form=form)
                
        return render_template('admin/master/hari/tambah_hari.html', form=form)
    
    @admin2.route('edit-hari/<int:id>', methods=['GET','POST'])
    def edit_hari(id):
        pass 
    
    @admin2.route('delete-hari/<int:id>', methods=['GET','DELETE'])
    def delete_hari(id):
        URL = base_url + f'api/v2/master/hari/get-one/{id}'
        response = req.delete(URL)
        if response.status_code == 204:
            flash(f'Data hari telah di hapus dari database. Status : {response.status_code}', 'info')
            return redirect(url_for('admin2.get_hari'))

    @admin2.route('data-jam')
    def get_jam():
        url = base_url + 'api/v2/master/jam/get-all'
        resp = req.get(url)
        jsonResp = resp.json()
        form = FormJam(request.form)
 
        return render_template('admin/master/jam/data_jam.html', model=jsonResp, form=form)
    
    @admin2.route('tambah-jam', methods=['GET','POST'])
    def add_jam():
        form = FormJam(request.form)
        url = base_url + 'api/v2/master/jam/create'
        if  request.method == 'POST' and form.validate_on_submit():
            jam = form.jam.data
            payload = json.dumps({
                'jam': jam
            })
            headers = {'Content-Type':'application/json'}
            resp = req.post(url=url, data=payload, headers=headers)
            msg = resp.json()
            if resp.status_code == 201:
                flash(message=f'{msg["msg"]} Status : {resp.status_code}', category='success')
                return redirect(url_for('admin2.get_jam'))
            else:
                flash(message=f'{msg["msg"]} Status : {resp.status_code}', category='error')
                return redirect(url_for('admin2.get_jam'))
    
    @admin2.route('edit-jam/<int:id>', methods=['GET','POST'])
    def edit_jam(id):
        url = base_url + f'api/v2/master/jam/get-one/{id}'
        if request.method == 'POST':
            jam = request.form.get('jam')
            payload = json.dumps({
                'jam': jam
            })
            headers = {'Content-Type':'application/json'}
            resp = req.put(url=url, data=payload, headers=headers)
            msg = resp.json()
            if resp.status_code == 200:
                flash(message=f'{msg["msg"]} Status: {resp.status_code}', category='info')
                return redirect(url_for('admin2.get_jam'))
            else:
                flash(message=f'{msg["msg"]} Status: {resp.status_code}', category='error')
                return redirect(url_for('admin2.get_jam'))
    
    @admin2.route('delete-jam/<int:id>', methods=['GET','POST'])
    def delete_jam(id):
        url = base_url + f'api/v2/master/jam/get-one/{id}'
        resp = req.delete(url=url)
        if resp.status_code == 204:
            flash(message=f'Data Jam telah dihapus dari database Status: {resp.status_code}', category='info')
            return redirect(url_for('admin2.get_jam'))
        else:
            msg = resp.json()
            flash(message=f'{msg["msg"]} Status: {resp.status_code}', category='error')
            return redirect(url_for('admin2.get_jam'))
                
class TestPage:
    @admin2.get("test-page")
    def test_page():
        
        return render_template("test_page.html" )