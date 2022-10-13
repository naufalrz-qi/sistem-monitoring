from  flask import Blueprint, request, redirect, url_for, render_template
from app.models.user_model import *
from app.models.user_details_model import *
from app.lib.base_model import BaseModel

staff = Blueprint('staff', __name__, template_folder='../templates/', url_prefix='/admin')

@staff.route('/')
def index():
    
    return render_template('staff/index_staff.html')

class  Siswa:
    @staff.route('/pengguna-siswa')
    def pengguna_siswa():
        base = BaseModel(SiswaModel)
        model = base.get_all()    
        return render_template('staff/data_pengguna/data_siswa.html', model=model)