from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class InstitucionForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    informacion = StringField('Informacion', validators=[DataRequired(), Length(max=255)])
    calle = StringField('Calle', validators=[Length(max=15)])
    numero = StringField('Numero', validators=[Length(max=15)])
    localizacion = StringField('Localizacion', validators=[Length(max=100)])
    palabras_claves = StringField('Palabras Claves', validators=[DataRequired(), Length(max=50)])
    horarios = StringField('Horarios', validators=[Length(max=50)])
    web = StringField('Web', validators=[Length(max=50)])
    contacto = StringField('Contacto', validators=[DataRequired(), Length(max=50)])
