from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import ValidationError

class FormAddSiswa(FlaskForm):
    username = StringField(label='Username :')
    password = PasswordField(label='Password :')
    tipe = StringField(label='Group :')
    fullname = StringField(label='Nama Lengkap')
    jenisKelamin = SelectField(
        label='Jenis Kelamin',
        choices=[('','..::Select::..'),('laki-laki','Laki-laki'), ('perempuan','Perempuan')])
    agama = SelectField(
        label='Agama',
        choices=[
            ('','..::Select::..'),
            ('islam','Islam'),
            ('kristen','Kristen'),
            ('katolik','Katolik'),
            ('hindu','Hindu'),
            ('budha','Budha'),
            ])
    kelas = SelectField(label='Kelas')
    submit = SubmitField(label='Submit Data')
    
    
    def validate_username(self, field):
        if len(field.data) == 0:
            raise ValidationError('*Username tidak boleh kosong..!')
        
    def validate_password(self, field):
        if len(field.data) == 0:
            raise ValidationError('*Password tidak boleh kosong..!')
        elif len(field.data) < 6:
            raise ValidationError('*Jumlah karakter minimal 6')
    
    def validate_fullname(self, field):
        if len(field.data) == 0:
            raise ValidationError('*Nama tidak boleh kosong..!')
        
    def validate_jenisKelamin(self, field):
        if field.data == '':
            raise ValidationError('*Pilih jenis kelamin..!')
        
    def validate_agama(self, field):
        if field.data == '':
            raise ValidationError('*Pilih agama..!')
   
    def validate_kelas(self, field):
        if field.data == '':
            raise ValidationError('*Pilih kelas..!')
        
class FormStatus(FlaskForm):
    state = SubmitField('Aktif')