from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email


class MaintenanceForm(FlaskForm):
    activate_maintenance = SubmitField('Activar Mantenimiento')
    deactivate_maintenance = SubmitField('Desactivar Mantenimiento')
    mensaje = StringField('Mensaje de mantenimiento')
    guardar = SubmitField('Guardar Mensaje')


class ContactoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Telefono', validators=[DataRequired(message="Este campo es obligatorio")])
    direccion = StringField('Direccion', validators=[DataRequired(message="Este campo es obligatorio")])
    guardar = SubmitField('Guardar')


class paginadoForm(FlaskForm):
    per_page = IntegerField('Cantidad de elementos por pagina',
                            validators=[DataRequired(message="Este campo es obligatorio")])
    guardar = SubmitField('Guardar')
