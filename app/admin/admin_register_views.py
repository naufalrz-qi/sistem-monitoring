from app.admin.admin_model import *
from app.extensions import db
from app.models.user_details_model import *
from app.models.user_model import UserModel
from app.extensions import admin

 
admin_detail = admin.add_view(AdminDetailView(AdminDetailModel, db.session, name='Admin'))
user = admin.add_view(UserView(UserModel, db.session, name='Users'))
siswa_detail = admin.add_view(SiswaView(SiswaModel, db.session, name='Siswa'))
guru = admin.add_view(GuruDetailView(GuruModel, db.session, name='Guru'))