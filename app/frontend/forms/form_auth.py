from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import ValidationError

class FormEditStatus(FlaskForm):
    state = SubmitField("Aktif")

class FormEditPassword(FlaskForm):
    kataSandi = PasswordField('Password')
    submit = SubmitField('Save Changes')
    
    def validate_kataSandi(self, field):
        if field.data == None:
            raise ValidationError('*Password tidak boleh kosong.')
        elif len(field.data) < 6:
            raise ValidationError('*Password minimal 6 karakter.')