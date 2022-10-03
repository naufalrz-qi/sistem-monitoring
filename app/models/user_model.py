from datetime import datetime
from email.policy import default
from app.extensions import db
import sqlalchemy as sa 
from app.lib.date_time import utc_makassar
from werkzeug.security import check_password_hash

class UserModel(db.Model):
    __tablename__ = 'tb_user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(128), nullable=False)    
    first_name = sa.Column(sa.String(128), nullable=False, default='')
    last_name = sa.Column(sa.String(128), nullable=False, default='')
    password = sa.Column(sa.String(256), nullable=False, default='password123')
    group = sa.Column(sa.String(128), nullable=False) 
    join_date = sa.Column(sa.DateTime, default=utc_makassar())
    update_date = sa.Column(sa.DateTime, onupdate=utc_makassar())
    is_active = sa.Column(sa.String(2), nullable=False)
    user_login_now = sa.Column(sa.DateTime)
    user_logout = sa.Column(sa.DateTime)
    
    def __init__(self, username=None, first_name=None, last_name=None, password=None, group=None) -> None:
        super().__init__()
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.group = group
        self.is_active = 1
    
    
    def __repr__(self) -> str:
        return self.first_name
    
    
    def check_pswd(*args, **kwargs):
        return check_password_hash(*args, **kwargs)
    
class TokenBlockList(db.Model):
    __tablename__ = 'auth_token_block'
    id = sa.Column(sa.Integer, primary_key=True)
    jti = sa.Column(sa.String(36), nullable=False, index=True)
    created_at = sa.Column(sa.DateTime, nullable=False)