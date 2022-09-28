from flask import Blueprint, request, jsonify
from app.extensions import jwt_manager
from sqlalchemy.exc import IntegrityError
from app.lib.base_model import BaseModel
from app.models.siswa_model import SiswaModel
from app.models.user_model import UserModel
from app.extensions import db
from app.lib.status_code import *
from werkzeug.security import generate_password_hash

auth = Blueprint('auth',__name__, url_prefix='/auth')

@auth.route('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

@auth.route('/create', methods=['POST','GET'])
def create():
    username = request.json.get('username')
    password = request.json.get('password')
    group = request.json.get('group')
    
    hash_pswd = generate_password_hash(password=password)
    
    if group == 'siswa':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        gender = request.json.get('gender')
        agama = request.json.get('agama')
        
        siswa = BaseModel(SiswaModel(first_name,
                                     last_name,
                                     gender,
                                     agama)) 
        usrnm = BaseModel(UserModel) 
        check_username = usrnm.get_one(username=username)
                
        if check_username is not None:
            return jsonify({
                'msg' : 'Username is already exists'
            }), HTTP_409_CONFLICT
        else:            
            siswa.create()
            user = BaseModel(UserModel(username, 
                                       hash_pswd, 
                                       group, 
                                       siswa.model.id))
            user.create()
            
            return jsonify({
                'msg' : f'Add user {siswa.model.first_name} succesful.',
                'id' : siswa.model.id
            }), HTTP_201_CREATED
    
    elif group == 'guru':
        pass    
        
    

@auth.route('/get')
def get():
    pass 

@auth.route('/edit')
def edit():
    pass 

@auth.route('/delete')
def delete():
    pass