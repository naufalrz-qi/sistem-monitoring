from flask import Blueprint, jsonify, request
from app.backend.lib.base_model import BaseModel
from app.backend.lib.date_time import format_datetime_id, format_indo
from app.backend.lib.status_code import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from app.backend.models.master_model import KelasModel, WaliKelasModel
from app.backend.models.user_details_model import GuruModel
from app.backend.models.user_model import UserModel
from app.backend.extensions import db

guru = Blueprint('guru', __name__, url_prefix='/api/v2/guru')

@guru.route('/get-all')
def get():
    base_model = BaseModel(GuruModel)      
    data = []
    for user in base_model.get_all():    
        data.append({
            'id':user.users.id,
            'username':user.users.username.title(),
            'first_name' : user.first_name.title(),
            'last_name' : user.last_name.title(),
            'gender' : user.gender.title(),
            'agama': user.agama.title() if user.agama else '-',
            'alamat': user.alamat.title() if user.alamat else '-',
            'mapel' : user.mapel.mapel if user.mapel_id else '-', 
            'active' : True if user.users.is_active == '1' else False,
            'join' : format_indo(user.users.join_date),
            'login' : format_datetime_id(user.users.user_last_login) if user.users.user_last_login else '-',
        })        
    return jsonify(data), HTTP_200_OK

@guru.route('single/<int:id>', methods=['GET','PUT','DELETE'])
def get_single_object(id):
    model_user = BaseModel(UserModel)
    user = model_user.get_one(id=id)
    
    model_guru = BaseModel(GuruModel)
    guru = model_guru.get_one(user_id=id)
    
    if request.method == 'GET':    
        if not model_guru:
            return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
        else:
            return jsonify(
                id=user.id,
                nip=user.username,
                first_name= guru.first_name.title(),
                last_name= guru.last_name.title(),
                
            ), HTTP_200_OK

@guru.route('/wali-kelas')
def get_wali_kelas():
    model = BaseModel(WaliKelasModel)
    wali_kelas = model.get_all()
    
    data = []
    for _ in wali_kelas:
        data.append({
            'first_name' : _.guru.first_name,
            'last_name' : _.guru.last_name,
            'kelas' : _.kelas.kelas
        })
    
    return jsonify(data=data), HTTP_200_OK