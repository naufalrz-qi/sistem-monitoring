from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import ValidationError


class FormSelectKelas(FlaskForm):
    kelas = SelectField(label="Pilih Kelas", choices=[("", "- Pilih -")])

    def validate_kelas(self, field):
        if field.data == "":
            raise ValidationError("*Harap pilih kelas")
