from email.policy import default
from app.extensions import db
import sqlalchemy as sa 
from app.lib.date_time import utc_makassar


class UserModel(db.Model):
    __tablename__ = 'tb_user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(128), nullable=False)    
    password = sa.Column(sa.String(256), nullable=False, default='password123')
    group = sa.Column(sa.String(128), nullable=False) 
    join_date = sa.Column(sa.DateTime, default=utc_makassar())
    update_date = sa.Column(sa.DateTime, onupdate=utc_makassar())
    is_active = sa.Column(sa.String(2), nullable=True)
    user_login_now = sa.Column(sa.DateTime, onupdate=utc_makassar())
    user_logout = sa.Column(sa.DateTime, onupdate=utc_makassar())
    id_siswa = sa.Column(sa.Integer, sa.ForeignKey('tb_siswa_detail.id', ondelete='CASCADE', onupdate='CASCADE'))
    
    def __init__(self, username, password, group, id_siswa) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.group = group
        self.is_active = 1
        self.id_siswa = id_siswa
        
    
    def __repr__(self) -> str:
        return 'Username : {}'.format(self.username)
    