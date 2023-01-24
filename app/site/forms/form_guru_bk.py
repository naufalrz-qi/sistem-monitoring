from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import ValidationError


class FormTambahPelanggar(FlaskForm):
    kelas = SelectField(label="Pilih Kelas", choices=[("", "- Pilih -")])
    siswa = SelectField(label="Pilih Siswa", choices=[("", "- Pilih -")])
    jenisPelanggaran = SelectField(
        label="Pilih Jenis Pelanggaran", choices=[("", "- Pilih -")]
    )
    pelapor = StringField(label="Nama Pelapor")
    submit = SubmitField(label="Submit")

    def validate_siswa(self, field):
        if field.data == "":
            raise ValidationError("*Harap Pilih Nama Siswa")

    def validate_jenisPelanggaran(self, field):
        if field.data == "":
            raise ValidationError("*Harap Pilih Jenis Pelanggaran")
