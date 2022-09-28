from app.admin.admin_model import SiswaView, UserView
from app.extensions import db
from app.models.siswa_model import SiswaModel
from app.models.user_model import UserModel
from app.extensions import admin

 
user = admin.add_view(UserView(UserModel, db.session, name='User', endpoint='users'))
siswa = admin.add_view(SiswaView(SiswaModel, db.session, name='Siswa', endpoint='students'))