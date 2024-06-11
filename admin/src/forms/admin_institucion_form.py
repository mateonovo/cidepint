from flask_wtf import FlaskForm
from wtforms import SubmitField


class adminInstitucionForm(FlaskForm):
    administrador = SubmitField('Asignar Administrador')
    operador = SubmitField('Asignar Operador')
    dueño = SubmitField('Asignar Dueño')