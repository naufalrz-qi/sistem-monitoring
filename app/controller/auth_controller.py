import time
from flask import Blueprint, request, jsonify
from app.extensions import jwt_manager
from sqlalchemy.exc import IntegrityError
from app.lib.base_model import BaseModel
from app.models.user_details_model import GuruModel, SiswaModel
from app.models.user_model import UserModel
from app.extensions import db
from app.lib.status_code import *
from werkzeug.security import generate_password_hash

auth = Blueprint('auth',__name__, url_prefix='/api/v2/auth')

@auth.route('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

@auth.route('/create', methods=['POST','GET'])
def create():
    username = request.json.get('username')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')
    group = request.json.get('group')
    
    hash_pswd = generate_password_hash(password=password)
    
    user = BaseModel(UserModel(username,
                                    first_name,
                                    last_name, 
                                    hash_pswd, 
                                    group,                                     
                                    ))
    if group == 'siswa':
        gender = request.json.get('gender')
        agama = request.json.get('agama')        
         
        usrnm = BaseModel(UserModel) 
        check_username = usrnm.get_one(username=username)
                
        if check_username is not None:
            return jsonify({
                'msg' : 'Username is already exists'
            }), HTTP_409_CONFLICT
        else:            
            user.create()
            siswa = BaseModel(SiswaModel(gender,
                                     agama,
                                     user.model.id))
            siswa.create()         
            return jsonify({
                'msg' : f'Add user {user.model.first_name} succesful.',
                'id' : siswa.model.id
            }), HTTP_201_CREATED
    
    elif group == 'guru':
        gender = request.json.get('gender')
        alamat = request.json.get('alamat')
        agama = request.json.get('agama')
        
        usrnm = BaseModel(UserModel) 
        check_username = usrnm.get_one(username=username)
                
        if check_username is not None:
            return jsonify({
                'msg' : 'Username is already exists'
            }), HTTP_409_CONFLICT
        else:
            user.create()
            guru = BaseModel(GuruModel(gender,
                                       alamat,
                                       agama,
                                       user.model.id))
            guru.create()

            return jsonify({
                'msg' : f'add user {user.model.first_name}'
            })
    

@auth.route('/get')
def get():
    pass 

@auth.route('/edit')
def edit():
    pass 

@auth.route('/delete')
def delete():
    pass