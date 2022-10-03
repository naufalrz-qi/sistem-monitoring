from app.admin.admin_model import GuruDetailView, SiswaView, UserView
from app.extensions import db
from app.models.user_details_model import *
from app.models.user_model import UserModel
from app.extensions import admin

 
user = admin.add_view(UserView(UserModel, db.session, name='User'))
siswa = admin.add_view(SiswaView(SiswaModel, db.session, name='Siswa', endpoint='students'))
guru = admin.add_view(GuruDetailView(GuruModel, db.session, name='Guru', endpoint='teachers'))