from flask_admin.contrib.sqla import ModelView
from app.models.siswa_model import SiswaModel
from app.models.user_model import UserModel
from wtforms import fields

class UserView(ModelView):
    column_exclude_list = ['id','user_login_now','user_logout', 'tb_siswa_detail', 'password']
    form_excluded_columns = ['join_date','update_date','user_login_now','user_logout']
    form_choices = {'is_active': [
                    ('0', 'False'),
                    ('1', 'True')],
                    'group' : [
                        ('admin', 'Admin'),
                        ('siswa', 'Siswa'),
                        ('guru', 'Guru'),
                    ]
                    }
    can_create = False
    can_view_details = True
    can_edit = True
    column_display_pk = True
    form_extra_fields = {
        'password' : fields.PasswordField('Password'),
        'tb_siswa_detail' : fields.StringField('ID Siswa')
    }
    
    
    
class SiswaView(ModelView):
    column_exclude_list = []
    can_view_details = True
    inline_models = [(UserModel, dict(
        form_columns=[
            UserModel.username,
            'password',
            UserModel.group,
            UserModel.is_active,
            UserModel.id,
            ],
        form_extra_fields = {
                'password' : fields.PasswordField('Password'),
            }
        ))]
   