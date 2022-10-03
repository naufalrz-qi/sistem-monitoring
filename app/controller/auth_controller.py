from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user, get_jwt, get_jwt_identity, jwt_required, create_access_token, create_refresh_token
from app.extensions import jwt
from sqlalchemy.exc import IntegrityError
from app.lib.base_model import BaseModel
from app.lib.date_time import utc_makassar
from app.models.user_details_model import GuruModel, SiswaModel
from app.models.user_model import TokenBlockList, UserModel
from app.extensions import db
from app.lib.status_code import *
from werkzeug.security import generate_password_hash, check_password_hash

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
                sql_user.user_login_now = utc_makassar()
                user.edit()      
                return jsonify({
                    'id' : sql_user.id,
                    'access_token' : access_token,
                    'refresh_token' : refresh_token,
                }), HTTP_200_OK
                
            elif sql_user.group == 'guru' and sql_user.is_active == '1':
                sql_user.user_login_now = utc_makassar()
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
    
 
# @auth.route('/test')
# @jwt_required()
# def test_user():
#     current_user = get_jwt_identity()
    
#     model = BaseModel(GuruModel)
#     guru = model.get_one_or_none(user_id=current_user.get('id'))
#     print(guru.gender)
    
#     return jsonify(
#         # current_user,
#         current_user,
       
#     ),HTTP_200_OK
    
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
    

@auth.route('/get-one')
@jwt_required()
def get():
    current_user = get_jwt_identity()
    user_id = current_user.get('id')
    
    jjwt = get_jwt()['exp']
    print(jjwt)
    if current_user.get('group') == 'siswa':
        model = BaseModel(SiswaModel)
        user = model.get_one_or_none(user_id=user_id)        
        return jsonify({
            'id' : user_id,
            'first_name' : current_user.get('first_name'),
            'last_name' : current_user.get('last_name'),
            'group' : current_user.get('group'),
            'is_active': current_user.get('is_active'),
            'gender' : user.gender,
            }), HTTP_200_OK
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


@auth.route('/edit')
def edit():
    pass 

@auth.route('/delete')
def delete():
    pass