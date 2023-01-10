from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import ValidationError


class FormSelectKelas(FlaskForm):
    kelas = SelectField(label="Pilih Kelas", choices=[("", "- Pilih -")])

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kelas")


class FormSelectKehadiranSiswa(FlaskForm):
    kelas = SelectField("Pilih Kelas", choices=[("", "- Pilih -")])
    bulan = SelectField("Pilih Bulan", choices=[("", "- Pilih -")])
    tahun = SelectField("Pilih Tahun", choices=[("", "- Pilih -")])

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kelas")

    def validate_bulan(self, field):
        if field.data == "":
            raise ValidationError("*Harap Pilih Bulan")

    def validate_tahun(self, field):
        if field.data == "":
            raise ValidationError("*Harap Pilih Tahun")
