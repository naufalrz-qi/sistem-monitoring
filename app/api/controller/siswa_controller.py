import time
from flask import Blueprint, jsonify, request
from app.lib.base_model import BaseModel
from app.lib.date_time import format_datetime_id, format_indo, string_format
from app.lib.status_code import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from app.models.user_details_model import SiswaModel
from app.models.user_model import UserModel
from app.extensions import db

siswa = Blueprint('siswa', __name__, url_prefix='/api/v2/student')

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
            'tempat_lahir': user.tempat_lahir.title() if user.tempat_lahir else '-',
            'tgl_lahir': user.tgl_lahir if user.tgl_lahir else '-',
            'agama': user.agama.title() if user.agama else '-',
            'alamat': user.alamat.title() if user.alamat else '-',
            'active' : True if user.user.is_active == '1' else False,
            'join' : user.user.join_date,
            'last_login' : format_datetime_id(user.user.user_last_login) if user.user.user_last_login else '-',
            "logout" : user.user.user_logout if user.user.user_logout else '-'
        })   
    return jsonify(data), HTTP_200_OK

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
        
            base.edit()        
            return jsonify(msg=f'Update data {model.user.first_name} successfull.'), HTTP_200_OK
    
    elif request.method == 'DELETE':        
        if not model:
            return jsonify(msg='Data Not Found.'), HTTP_404_NOT_FOUND
        else:
            base.delete(model)
            base_user.delete(user)
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT