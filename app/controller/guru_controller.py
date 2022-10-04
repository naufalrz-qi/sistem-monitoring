from flask import Blueprint, jsonify
from app.lib.base_model import BaseModel
from app.lib.status_code import HTTP_200_OK
from app.models.user_details_model import GuruModel
from app.models.user_model import UserModel
from app.extensions import db

guru = Blueprint('guru', __name__, url_prefix='/api/v2/guru')

@guru.route('/get-all')
def get():
    model = db.session.query(UserModel, GuruModel)\
                      .join(GuruModel)\
                      .filter(UserModel.id==GuruModel.user_id).all()   
    data = []
    for user,_ in model:
        data.append({
            'id':user.id,
            'username':user.username,
            'first_name' : user.first_name.capitalize(),
            'last_name' : user.last_name.capitalize(),
            'gender' : _.gender.capitalize(),
            'agama': _.agama.capitalize() if _.agama else '-',
            'alamat': _.alamat.capitalize() if _.alamat else '-',
            'active' : True if user.is_active == '1' else False,
            'join' : user.join_date,
            'login' : user.user_login_now if user.user_login_now else '-',
            "logout" : user.user_logout if user.user_logout else '-'
            
        })        
    return jsonify(data), HTTP_200_OK
    
    