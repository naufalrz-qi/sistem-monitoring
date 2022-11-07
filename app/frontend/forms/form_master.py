from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError

class FormMapel(FlaskForm):
    mapel = StringField(label='Mata Pelajaran')
    submit = SubmitField(label='Submit Data')
    
    def validate_mapel(self, field):
        if len(field.data) == 0:
            raise ValidationError('*Inputan Mapel tidak boleh kosong.!')