from fileinput import filename
import hashlib
import qrcode, os
from sqlalchemy import func
from werkzeug.utils import secure_filename
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import HorizontalBarsDrawer
from flask import Blueprint, jsonify, request, send_from_directory, url_for
from flask_jwt_extended import jwt_required
from app.backend.lib.base_model import BaseModel
from app.backend.lib.date_time import format_datetime_id, format_indo, string_format, utc_makassar
from app.backend.lib.status_code import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from app.backend.models.master_model import KelasModel
from app.backend.models.user_details_model import SiswaModel
from app.backend.models.user_model import UserModel
from app.backend.extensions import db
from app.backend.lib.uploader import uploads
from datetime import datetime
import app

siswa = Blueprint('siswa', __name__, url_prefix='/api/v2/student')
qc_folder = os.getcwd() + '/app/backend/static/img/siswa/qr_code/'


# NOTE : MANUAL STATIC FOLDER
@siswa.route('backend/<path:filename>')
def static(filename):
    dir = send_from_directory('backend/static', filename)
    return dir


@siswa.route('/get-all')
def get():
    # model = db.session.query(UserModel, SiswaModel)\
    #                   .join(SiswaModel).all()
    base = BaseModel(SiswaModel)
    model = base.get_all()
    data = []
    for user in model:
        data.append({
            'id':user.user.id,
            'nisn':user.user.username,
            'first_name' : user.first_name.title(),
            'last_name' : user.last_name.title(),
            'gender' : user.gender.title(),
            'kelas' : user.kelas.kelas if user.kelas_id else '-',
            'tempat_lahir': user.tempat_lahir.title() if user.tempat_lahir else '-',
            # 'tgl_lahir': user.tgl_lahir if user.tgl_lahir else '-',
            'tgl_lahir': format_indo(user.tgl_lahir) if user.tgl_lahir else '-',
            'agama': user.agama.title() if user.agama else '-',
            'alamat': user.alamat.title() if user.alamat else '-',
            'nama_ortu': user.nama_ortu_or_wali if user.nama_ortu_or_wali else '-',
            'picture': url_for('.static', filename='img/siswa/foto/'+ user.pic) if user.pic else None,
            'pic_name': user.pic if user.pic else '-',
            'telp': user.no_telp if user.no_telp else '-',
            'qr_code': url_for('.static', filename='img/siswa/qr_code/' + user.qr_code) if user.qr_code else None,
            'active' : 'Aktif' if user.user.is_active == '1' else 'Non-Aktif',
            'join' : format_datetime_id(user.user.join_date) if user.user.join_date else '-',
            'type': user.user.group.upper(),
            'last_update': format_indo(user.user.update_date) if user.user.update_date else '-',
            'last_login' : format_datetime_id(user.user.user_last_login) if user.user.user_last_login else '-',
            "logout" : user.user.user_logout if user.user.user_logout else '-'
        })           
    return jsonify(data=data), HTTP_200_OK

@siswa.route('/single/<int:id>', methods=['GET','PUT','DELETE'])
def get_single(id):
    # base_user = BaseModel(UserModel)
    # user = base_user.get_one_or_none(id=id)
    base = BaseModel(SiswaModel)
    model = base.get_one_or_none(user_id=id)
       
    if request.method == 'GET':
        if not model:
            return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
        print(model.tgl_lahir)
        return jsonify(id= model.user.id,
                       nisn=model.user.username,
                       first_name= model.first_name.title(),
                       last_name=model.last_name.title(),
                       kelas = model.kelas.kelas if model.kelas.kelas else None,
                       kelas_id = model.kelas_id if model.kelas_id else None,
                       gender=model.gender.title() if model.gender else None  ,
                       tempat_lahir= model.tempat_lahir.title() if model.tempat_lahir else None,
                       tgl_lahir=str(model.tgl_lahir) if model.tgl_lahir else None,
                       agama=model.agama.title() if model.agama else None,
                       alamat=model.alamat.title() if model.alamat else None,
                       nama_ortu=model.nama_ortu_or_wali.title() if  model.nama_ortu_or_wali else None,
                       telp = model.no_telp if model.no_telp else None
                       ), HTTP_200_OK
        
    elif request.method == 'PUT':
        if not model:
            return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
        else:
            nisn = request.json.get('nisn')       
            first_name = request.json.get('first_name')
            last_name = request.json.get('last_name')
            gender = request.json.get('gender')
            tmpt_lahir = request.json.get('tempat')
            tgl_lahir = request.json.get('tgl')
            alamat = request.json.get('alamat')
            agama = request.json.get('agama')
            telp = request.json.get('telp')
            kelas = request.json.get('kelas')
            nama_ortu = request.json.get('nama_ortu')
            # active = request.json.get('active')                  
            
            model.user.username = nisn
            model.firs_name = first_name
            model.last_name = last_name
            model.gender = gender
            model.tempat_lahir = tmpt_lahir
            model.tgl_lahir = tgl_lahir
            # model.tgl_lahir = string_format(tgl_lahir)
            model.alamat = alamat
            model.agama = agama
            model.no_telp = telp
            model.kelas_id = kelas
            model.nama_ortu_or_wali  = nama_ortu
            model.user.update_date = utc_makassar()
            # model.user.is_active = active
        
            base.edit()   
            
            baseKelas = BaseModel(KelasModel)
            kelasModel = baseKelas.get_one(id=kelas) 
            countSiswaGender = db.session.query(func.count(SiswaModel.kelas_id)).filter(SiswaModel.kelas_id==kelas).filter(SiswaModel.gender==gender).scalar()
            countSiswaAll = db.session.query(func.count(SiswaModel.kelas_id)).filter(SiswaModel.kelas_id==kelas).scalar()
            
            if gender == 'laki-laki':
                kelasModel.jml_laki = countSiswaGender
            elif gender == 'perempuan':
                kelasModel.jml_perempuan = countSiswaGender
            
            kelasModel.jml_seluruh = countSiswaAll
            baseKelas.edit()
                
            return jsonify(msg=f'Update data {model.first_name} successfull.'), HTTP_200_OK
    
    elif request.method == 'DELETE':        
        if not model:
            return jsonify(msg='Data Not Found.'), HTTP_404_NOT_FOUND
        else:
            # base.delete(model)
            # # base_user.delete(user)
            '''
            Check file before delete user and file
            '''
            dir_file = os.getcwd()+'/app/backend/static/img/siswa/foto/'
            # file = dir_file + model.pic
            
            if model.pic:
                file = os.path.join(dir_file, model.pic)
                os.unlink(file)
            
                base_user = BaseModel(UserModel)
                model_user = base_user.get_one(id=id)
                base.delete(model_user)       
                return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
            else:
                base_user = BaseModel(UserModel)
                model_user = base_user.get_one(id=id)
                base.delete(model_user)       
                return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
                
        
# generate qr code
@siswa.route('/generate-qc', methods=['GET','PUT'])
def generate_qc():
    base = BaseModel(SiswaModel)
    id = request.args.get('id')
    model = base.get_one(user_id=id)
    
    if not model:
        return jsonify(msg='User not found.'), HTTP_404_NOT_FOUND
    else:
        qc= qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qc.add_data(model.user.username)
        qc_img = qc.make_image(image_factory=StyledPilImage, module_drawer=HorizontalBarsDrawer(), fit=True)
        enc_file_name = hashlib.md5(secure_filename(model.user.username).encode('utf-8')).hexdigest()
        path_file = qc_folder +  model.first_name + '_' + enc_file_name + '.png'
        qc_img.save(path_file)
        
        model.qr_code = model.first_name + '_' + enc_file_name + '.png'
        
        base.edit()
        
        return jsonify(msg='generate qr code success'),HTTP_200_OK

# upload photos
@siswa.put('upload-photo')
@siswa.post('upload-photo')
def upload_photo():
    base = BaseModel(SiswaModel)
    id = request.args.get('id')
    model = base.get_one(user_id=id)
    if not model:
        return jsonify(msg='Data not found'), HTTP_404_NOT_FOUND
    else:
        f = request.files['images']
        first_name = model.first_name if len(model.first_name) != 2 else model.last_name
        user_first_name = first_name.replace(" ", "_").lower()
        
        upload_file = uploads(f, user_first_name)
        if upload_file['status'] == 'ok':
            model.pic = upload_file['photo_name']            
            base.edit()            
            return jsonify(msg='upload photo success'), HTTP_200_OK
        

# GET SISWA BY Class
@siswa.get('get-siswa')
def getSiswa():
    pass