from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class FormAddGuru(FlaskForm):
    pass


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
