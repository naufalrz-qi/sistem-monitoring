from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField


class FormAddGuru(FlaskForm):
    username = StringField(label="Username :")
    password = PasswordField(label="Password :")
    tipe = StringField(label="Group :")
    fullname = StringField(label="Nama Lengkap :")
    jenisKelamin = SelectField(
        label="Jenis Kelamin :",
        choices=[
            ("", "..::Select::.."),
            ("laki-laki", "Laki-laki"),
            ("perempuan", "Perempuan"),
        ],
    )
    agama = SelectField(
        label="Agama :",
        choices=[
            ("", "..::Select::.."),
            ("islam", "Islam"),
            ("kristen", "Kristen"),
            ("katolik", "Katolik"),
            ("hindu", "Hindu"),
            ("budha", "Budha"),
        ],
    )
    mapel = SelectField(label="Mata Pelajaran :", choices=[('','..:: SELECT ::..')])
    alamat = StringField(label='Alamat :')
    telp = StringField(label='No. Telp :')
    submit = SubmitField(label="Submit Data")


class FormEditGuru(FlaskForm):
    nip = StringField("NIP :")
    fullname = StringField("Nama Lengkap :")
    mapel = SelectField("Mata Pelajaran", choices=[("", "..:: SELECT ::..")])
    jenisKelamin = SelectField(
        "Jenis Kelamin :",
        choices=[
            ("_","..:: SELECT ::.."),
            ("laki-laki", "Laki-Laki"),
            ("perempuan", "Perempuan"),
        ],
    )
    agama = SelectField(
        label="Agama :",
        choices=[
            ("", "..::Select::.."),
            ("islam", "Islam"),
            ("kristen", "Kristen"),
            ("katolik", "Katolik"),
            ("hindu", "Hindu"),
            ("budha", "Budha"),
        ],
    )
    alamat = StringField('Alamat :')
    telp = StringField('Telp :')
    submit = SubmitField('Save Changes')
