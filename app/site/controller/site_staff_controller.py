import os
from flask import Blueprint, Response, request, redirect, url_for, render_template, stream_template
from app.lib.status_code import HTTP_413_REQUEST_ENTITY_TOO_LARGE
from app.models.user_model import *
from app.models.user_details_model import *
from app.lib.base_model import BaseModel
import requests as req
import io
import xlwt
from werkzeug.utils import secure_filename

staff = Blueprint('staff', __name__, template_folder='../templates/', url_prefix='/admin')

@staff.route('/')
def index():    
    return render_template('staff/index_staff.html')

class Siswa:
    base_siswa = BaseModel(SiswaModel)    
    # def __init__(self):
    #     self.base = SiswaModel
    
    @staff.route('/data-siswa')
    def get_siswa():
        base_url = request.url_root
        url = base_url + url_for('siswa.get')
        r = req.get(url)
        data = r.json()       
        return render_template('staff/data_pengguna/siswa/data_siswa.html', model=data)
    
    @staff.route('/generate-qc', methods=['GET','PUT'])
    def generate_qc():
        base_url = request.url_root
        id = request.args.get('id')
        url = base_url + url_for('siswa.generate_qc', id=id)
        headers = {
            'Content-Type': 'application/json'
        }
        r = req.put(url, headers=headers)
        if r.status_code == 200:
            return redirect(url_for('staff.get_siswa'))
        
    @staff.post('/upload-photo')
    # @staff.route('/upload-photo', methods=['GET','PUT','POST'])
    def upload_foto():
        base_url = request.url_root
        id = request.args.get('id')
        url = base_url + url_for('siswa.upload_photo', id=id)
   
        file = request.files['file']
        file_name = secure_filename(file.filename)
        upload_folder = os.getcwd() + '/temp/'
        path = upload_folder + file_name
        file.save(path)
        
        files = {'images': open(path, 'rb+')}
        response = req.post(url, files=files)  
        
        if response.status_code == 200:
            files.get('images').close()
            temp_file = upload_folder + file_name
            os.remove(f'{temp_file}')
            return redirect(url_for('staff.get_siswa'))
        else:
            return f'<p>error : {response.status_code}</p>'
            
    @staff.errorhandler(413)
    def request_entity_too_large(error):
        return 'File Upload Maks 2MB', HTTP_413_REQUEST_ENTITY_TOO_LARGE    
        
               
    @staff.route('/export-siswa')
    def export_siswa():
        url = request.url_root + url_for('siswa.get')
        req_url = req.get(url)
        data = req_url.json()
        # output in bytes
        output = io.BytesIO()
        # create workbook object
        workbook = xlwt.Workbook()
        # style header
        # style = xlwt.easyxf('font: name Times New Roman, color-index black, bold on; \
        #                     align: wrap on, vert center, horiz center;')
        style = xlwt.XFStyle()
        # background
        bg_color = xlwt.Pattern()
        bg_color.pattern = xlwt.Pattern.SOLID_PATTERN
        bg_color.pattern_fore_colour = xlwt.Style.colour_map['ocean_blue']
        style.pattern = bg_color
        
        # border
        boder = xlwt.Borders()
        boder.bottom = xlwt.Borders.THIN
        style.borders = boder
        
        # font
        font = xlwt.Font()
        font.bold = True
        font.name = 'Times New Roman'
        font.height = 220
        style.font = font
        
        # font aligment
        align = xlwt.Alignment()
        align.wrap = xlwt.Alignment.NOT_WRAP_AT_RIGHT
        align.horz = xlwt.Alignment.HORZ_CENTER
        align.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = align
                
        # add a sheet
        sh = workbook.add_sheet('Data Siswa')
        # add headers
        sh.write(0,0, 'NO', style)
        sh.write(0,1, 'ID', style)
        sh.write(0,2, 'Nama', style)
        
        no = 0
        urut = 0
        
        for row in data['data']:
            sh.write(no+1, 0, urut+1)
            sh.write(no+1, 1, row['id'])
            no +=1
            urut +=1
            
        workbook.save(output)
        output.seek(0)
        
        return Response(output, mimetype='application/ms-excel', headers={'Content-Disposition': 'attachment; filename=data_siswa.xls'})
    
    # @staff.route('/tambah-pengguna-siswa', methods=['POST', 'GET'])
    # def post_siswa():
    #     username = request.form.get('username')
    #     passwaord = request.form.get('password')
    #     group = 'siswa'
    #     model = Siswa.base
    #     model.model = SiswaModel()    
    #     fullname = request.form.get('fullname')
        
    #     first_name = ''
    #     last_name = ''
    #     if fullname is not None:
    #         first_name, *last_name = fullname.split(' ')
            
    #     print(first_name)
    #     print(' '.join(last_name))
        
    #     return render_template('staff/data_pengguna/siswa/tambah_siswa.html')

class  User:
    base_user = BaseModel(UserModel)
    base_staff = BaseModel(AdminDetailModel)
    base_guru = BaseModel(GuruModel)
    base_siswa = BaseModel(SiswaModel)
    
    @staff.route('/data-user')
    def get():
        model = db.session.query(UserModel).all()
            
        for user in model:
            print(user.id)      
        print(model)
        model_user = User.base_user.get_all()
        return render_template('staff/data_pengguna/data_user.html', user=model_user)
        
        
        
    