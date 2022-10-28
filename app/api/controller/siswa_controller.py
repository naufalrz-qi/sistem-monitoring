from fileinput import filename
import hashlib
import qrcode, os
from werkzeug.utils import secure_filename
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import HorizontalBarsDrawer
from flask import Blueprint, jsonify, request, url_for
from flask_jwt_extended import jwt_required
from app.lib.base_model import BaseModel
from app.lib.date_time import format_datetime_id, format_indo, string_format, utc_makassar
from app.lib.status_code import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from app.models.user_details_model import SiswaModel
from app.models.user_model import UserModel
from app.extensions import db
from app.lib.uploader import uploads
import app

siswa = Blueprint('siswa', __name__, url_prefix='/api/v2/student')
qc_folder = os.getcwd() + '/app/static/img/siswa/qr_code/'


@siswa.route('/get-all')
def get():
    # model = db.session.query(UserModel, SiswaModel)\
    #                   .join(SiswaModel).all()
    base = BaseModel(SiswaModel)
    model = base.get_all()
    data = []
    for user in model:
        data.append({
            'id':user.id,
            'nisn':user.user.username,
            'first_name' : user.first_name.title(),
            'last_name' : user.last_name.title(),
            'gender' : user.gender.title(),
            'kelas' : user.kelas.kelas if user.kelas_id else '-',
            'tempat_lahir': user.tempat_lahir.title() if user.tempat_lahir else '-',
            'tgl_lahir': format_indo(user.tgl_lahir) if user.tgl_lahir else '-',
            'agama': user.agama.title() if user.agama else '-',
            'alamat': user.alamat.title() if user.alamat else '-',
            'nama_ortu': user.nama_ortu_or_wali if user.nama_ortu_or_wali else '-',
            'picture': url_for('static', filename='img/siswa/photos/'+ user.pic) if user.pic else '-',
            'qr_code': url_for('static', filename='img/siswa/qr_code/' + user.qr_code) if user.qr_code else '-',
            'active' : 'Aktif' if user.user.is_active == '1' else 'Non-Aktif',
            'join' : user.user.join_date,
            'last_login' : format_datetime_id(user.user.user_last_login) if user.user.user_last_login else '-',
            "logout" : user.user.user_logout if user.user.user_logout else '-'
        })           
    return jsonify(data=data), HTTP_200_OK

@siswa.route('/single/<int:id>', methods=['GET','PUT','DELETE'])
def get_single(id):
    base_user = BaseModel(UserModel)
    user = base_user.get_one_or_none(id=id)
    base = BaseModel(SiswaModel)
    model = base.get_one_or_none(user_id=id)
       
    if request.method == 'GET':
        if not model:
            return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
        
        return jsonify(id= user.id,
                       nisn=model.user.username,
                       first_name= model.first_name.title(),
                       last_name=model.last_name.title(),
                       gender=model.gender.title() if model.gender else '-'  ,
                       tempat_l= model.tempat_lahir.title() if model.tempat_lahir else '-',
                       tgl_l= format_indo(model.tgl_lahir) if model.tgl_lahir else '-',
                       agama=model.agama.title() if model.agama else '-',
                       alamat=model.alamat.title() if model.alamat else '-',
                       active=True if model.user.is_active == "1" else False,
                       ), HTTP_200_OK
        
    elif request.method == 'PUT':
        if not model:
            return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
        else:        
            first_name = request.json.get('first_name')
            last_name = request.json.get('last_name')
            gender = request.json.get('gender')
            tmpt_lahir = request.json.get('tempat')
            tgl_lahir = request.json.get('tgl')
            alamat = request.json.get('alamat')
            agama = request.json.get('agama')
            active = request.json.get('active')      
            
            model.firs_name = first_name
            model.last_name = last_name
            model.gender = gender
            model.tgl_lahir = tmpt_lahir
            model.tgl_lahir = string_format(tgl_lahir)
            model.alamat = alamat
            model.agama = agama
            model.user.is_active = active
            model.update_date = utc_makassar()
        
            base.edit()        
            return jsonify(msg=f'Update data {model.user.first_name} successfull.'), HTTP_200_OK
    
    elif request.method == 'DELETE':        
        if not model:
            return jsonify(msg='Data Not Found.'), HTTP_404_NOT_FOUND
        else:
            base.delete(model)
            base_user.delete(user)
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
# generate qr code
@siswa.route('/generate-qc', methods=['GET','PUT'])
def generate_qc():
    base = BaseModel(SiswaModel)
    id = request.args.get('id')
    model = base.get_one(id=id)
    
    if not model:
        return jsonify(msg='User not found.'), HTTP_404_NOT_FOUND
    else:
        qc= qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qc.add_data(model.user.username)
        qc_img = qc.make_image(image_factory=StyledPilImage, module_drawer=HorizontalBarsDrawer())
        
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
    model = base.get_one(id=id)
    

    if not model:
        return jsonify(msg='Data not found'), HTTP_404_NOT_FOUND
    else:
        f = request.files['images']
        print(f)
        
        first_name = model.first_name
        user_first_name = first_name.replace(" ", "_").lower()
        
        upload_file = uploads(f, user_first_name)
        if upload_file['status'] == 'ok':
            model.pic = upload_file['photo_name']            
            base.edit()            
            return jsonify(msg='upload photo success'), HTTP_200_OK
        
        