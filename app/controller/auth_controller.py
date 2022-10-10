from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user, get_jwt, get_jwt_identity, jwt_required, create_access_token, create_refresh_token
from app.extensions import jwt
from app.lib.base_model import BaseModel
from app.lib.date_time import format_datetime_id, format_indo, utc_makassar
from app.models.user_details_model import *
from app.models.user_model import TokenBlockList, UserModel
from app.extensions import db
from app.lib.status_code import *
from werkzeug.security import generate_password_hash

auth = Blueprint('auth',__name__, url_prefix='/api/v2/auth')

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload['jti']
    token = db.session.query(TokenBlockList.id).filter_by(jti=jti).scalar()
    return token is not None

@auth.route('/login', methods=['POST','GET', 'PUT'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = BaseModel(UserModel)
    sql_user = user.get_one_or_none(username=username)
    
    if not sql_user:
        return jsonify({
            'msg' : 'username not found.'
        }), HTTP_401_UNAUTHORIZED    
    else:
        chk_pswd = UserModel.check_pswd(sql_user.password, password)
        if chk_pswd:
            if sql_user.group == 'siswa' and sql_user.is_active == '1':
                user_identity = {
                    'id' : sql_user.id,
                    'username' : sql_user.username,
                    'first_name' :sql_user.first_name,
                    'last_name' : sql_user.last_name,
                    'is_active' : sql_user.is_active,
                    'group' : sql_user.group
                 }
                
                access_token = create_access_token(identity=user_identity)
                refresh_token = create_refresh_token(identity=user_identity)
                sql_user.user_last_login = utc_makassar()
                user.edit()      
                return jsonify({
                    'id' : sql_user.id,
                    'access_token' : access_token,
                    'refresh_token' : refresh_token,
                }), HTTP_200_OK
                
            elif sql_user.group == 'guru' and sql_user.is_active == '1':
                sql_user.user_last_login = utc_makassar()
                user_identity = {
                    'id' : sql_user.id,
                    'username' : sql_user.username,
                    'first_name' :sql_user.first_name,
                    'last_name' : sql_user.last_name,
                    'is_active' : sql_user.is_active,
                    'group' : sql_user.group
                }
                access_token = create_access_token(identity=user_identity)
                refresh_token  = create_refresh_token(identity=user_identity)
                user.edit()
                return jsonify({
                    'id' : sql_user.id,
                    'first_name' : sql_user.first_name,
                    'acces_token' : access_token,
                    'refresh_token' : refresh_token,
                }), HTTP_200_OK
            else:
                return jsonify({
                    'msg' : 'Akun smntr tidak dapat di akses'
                }), HTTP_400_BAD_REQUEST
        else:
            return jsonify({
                'msg' : 'Password not valid.'
            }), HTTP_401_UNAUTHORIZED

@auth.route('/logout', methods=['DELETE'])
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt()["jti"]
    now = utc_makassar()
    db.session.add(TokenBlockList(jti=jti, created_at=now))
    db.session.commit()
    
    model = BaseModel(UserModel)
    id = get_jwt_identity()['id']
    user = model.get_one_or_none(id=id)
    user.user_logout = utc_makassar()
    model.edit()    
    return jsonify(msg="JWT revoked")

@auth.route('/refresh', methods=['POST','GET'])
@jwt_required(refresh=True)
def refresh_toke():
    identity = get_jwt_identity()
    access_token = create_access_token(identity, fresh=False)
    
    return jsonify(access=access_token), HTTP_200_OK
    
    
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
            }), HTTP_201_CREATED
            
    elif group == 'admin':
        gender = request.json.get('gender')
        alamat = request.json.get('alamat')
        
        usrnm = BaseModel(UserModel) 
        check_username = usrnm.get_one(username=username)
                
        if check_username is not None:
            return jsonify({
                'msg' : 'Username is already exists'
            }), HTTP_409_CONFLICT
        else:
            user.create()
            user_detail = BaseModel(AdminDetailModel(gender,
                                       alamat,
                                       user.model.id))
            user_detail.create()
            return jsonify({
                'msg' : f'add user {user.model.first_name}'
            }), HTTP_201_CREATED
    

@auth.route('/get-one')
@jwt_required()
def get_one():
    current_user = get_jwt_identity()
    user_id = current_user.get('id') 
    # jjwt = get_jwt()['exp']
    if current_user.get('group') == 'siswa':
        model = BaseModel(SiswaModel)
        user = model.get_one_or_none(user_id=user_id) 
        json_object = {
            'id' : user_id,
            'first_name' : current_user.get('first_name'),
            'last_name' : current_user.get('last_name'),
            'group' : current_user.get('group'),
            'is_active': current_user.get('is_active'),
            'gender' : user.gender,
            }       
        return jsonify(
            json_object
            ), HTTP_200_OK
    elif current_user.get('group') == 'guru':
        model = BaseModel(GuruModel)
        user = model.get_one_or_none(user_id=user_id)        
        return jsonify({
            'id' : user_id,
            'first_name' : current_user.get('first_name'),
            'last_name' : current_user.get('last_name'),
            'group' : current_user.get('group'),
            'is_active': current_user.get('is_active'),
            'gender' : user.gender,
            }), HTTP_200_OK
    elif current_user.get('group') == 'admin':
        model = BaseModel(AdminDetailModel)
        user = model.get_one_or_none(user_id=user_id)        
        return jsonify({
            'id' : user_id,
            'first_name' : current_user.get('first_name'),
            'last_name' : current_user.get('last_name'),
            'group' : current_user.get('group'),
            'is_active': current_user.get('is_active'),
            'gender' : user.gender,
            }), HTTP_200_OK

@auth.route('/get-all')
def get_all():
    model = BaseModel(UserModel)
    data = []
    for user in model.get_all():
        data.append(
           {
               'id': user.id,
               'username' : user.username,
               'first_name' : user.first_name,
               'last_name' : user.last_name,
               'group' : user.group,
               'join' : format_indo(user.join_date),
               'last_login' : format_datetime_id(user.user_last_login) if user.user_last_login else '-'               
           }
        ) 
   
    return jsonify(data), HTTP_200_OK
@auth.route('/edit')
def edit():
    pass 

@auth.route('/delete')
def delete():
    pass