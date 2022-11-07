from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError


class FormMapel(FlaskForm):
    mapel = StringField(label="Mata Pelajaran")
    submit = SubmitField(label="Submit Data")

    def validate_mapel(self, field):
        if len(field.data) == 0:
            raise ValidationError("*Inputan Mapel tidak boleh kosong.")


class FormSemester(FlaskForm):
    semester = SelectField(
        label="Semester :",
        choices=[("", "..:: SELECT ::.."), ("ganjil", "Ganjil"), ("genap", "Genap")],
    )
    status = SelectField(
        label="Status :",
        choices=[("", "..:: SELECT ::.."), ("0", "Tidak Aktif"), ("1", "Aktif")],
    )
    submit = SubmitField('Submit Data')

    def validate_semester(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan tidak boleh kosong.")

    def validate_status(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan tidak boleh kosong.")

class FormEditSemester(FlaskForm):
    
    status = SelectField(
        label="Status :",
        choices=[("", "..:: SELECT ::.."), ("0", "Tidak Aktif"), ("1", "Aktif")],
    )
    submit = SubmitField('Submit Data')

    def validate_status(self, field):
        if field.data == "":
            raise ValidationError("*Pilihan tidak boleh kosong.")
