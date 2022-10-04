from flask import Blueprint, jsonify
from app.lib.base_model import BaseModel
from app.lib.status_code import HTTP_200_OK
from app.models.user_details_model import SiswaModel
from app.models.user_model import UserModel
from app.extensions import db

siswa = Blueprint('siswa', __name__, url_prefix='/api/v2/student')

@siswa.route('/get-all')
def get():
    model = db.session.query(UserModel, SiswaModel)\
                      .join(SiswaModel)\
                      .filter(UserModel.id==SiswaModel.user_id).all()
    
    data = []
    for user,_ in model:
        data.append({
            'id':user.id,
            'username':user.username,
            'first_name' : user.first_name.capitalize(),
            'last_name' : user.last_name.capitalize(),
            'gender' : _.gender.capitalize(),
            'tempat_lahir': _.tempat_lahir.capitalize() if _.tempat_lahir else '-',
            'tgl_lahir': _.tgl_lahir if _.tgl_lahir else '-',
            'agama': _.agama.capitalize() if _.agama else '-',
            'alamat': _.alamat.capitalize() if _.alamat else '-',
            'active' : True if user.is_active == '1' else False,
            'join' : user.join_date,
            'login' : user.user_login_now if user.user_login_now else '-',
            "logout" : user.user_logout if user.user_logout else '-'
            
        })        
    return jsonify(data), HTTP_200_OK
    
    