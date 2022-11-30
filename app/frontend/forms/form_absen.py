from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, HiddenField, DateField, SubmitField


class AbsensiForm(FlaskForm):
    name = StringField("Nama")
    id = HiddenField("User ID")
    pertemuan = HiddenField("Pertemuan")
    today = DateField("Tanggal")
    ket = BooleanField("")
    submit = SubmitField("Selesai")
