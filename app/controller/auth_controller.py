from flask import Blueprint, url_for, request
from app.extensions import jwt_manager
from sqlalchemy.exc import IntegrityError

auth = Blueprint(__name__, url_prefix='/auth')

@auth.route('/login')
def login():
    pass

@auth.route('/add')
def create():
    username = request.json.get('username')
    password = request.json.get('password')
    group = request.json.get('group')
    
    if group == 'siswa':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        gender = request.json.get('gender')
        agama = request.json.get('agama')
        
        
        
    
    

@auth.route('/get')
def get():
    pass 

@auth.route('/edit')
def edit():
    pass 

@auth.route('/delete')
def delete():
    pass