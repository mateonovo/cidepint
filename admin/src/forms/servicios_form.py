from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional


class ServiciosForm(FlaskForm):
    nombre = StringField('Nombre del Servicio', validators=[DataRequired()])
    descripcion = StringField('Descripción del Servicio', validators=[DataRequired()])
    keywords = StringField('Palabras Claves', validators=[DataRequired()])
    tipo_servicio = SelectField('Tipo de Servicio', choices=[
        ('Análisis', 'Análisis'),
        ('Consultoría', 'Consultoría'),
        ('Desarrollo', 'Desarrollo')
    ], validators=[DataRequired()])
    habilitado = BooleanField('Habilitado', default=True)


class ActualizarSolicitudesForm(FlaskForm):
    estado = SelectField('Estado de Solicitud', validators=[DataRequired()])
    observacion_cambio_estado = StringField('Observaciones', default='')
    comentario = StringField('Comentario para el cliente', default='')
    submit = SubmitField('Actualizar')

    def set_estado_choices(self, solicitud):
        estados_disponibles = {
            'EN PROCESO': [('ACEPTADA', 'ACEPTADA'), ('RECHAZADA', 'RECHAZADA')],
            'ACEPTADA': [('FINALIZADA', 'FINALIZADA'), ('CANCELADA', 'CANCELADA')],
        }

        self.estado.choices = estados_disponibles.get(solicitud.estado, [])
        if not self.estado.choices:
            self.estado.choices = [('EN PROCESO', 'EN PROCESO')]


class FiltroSolicitudesForm(FlaskForm):
    fecha_inicio = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[Optional()])
    fecha_fin = DateField('Fecha de fin', format='%Y-%m-%d', validators=[Optional()])
    estado = SelectField('Estado', choices=[('', 'Todos'), ('ACEPTADA', 'ACEPTADA'), ('RECHAZADA', 'RECHAZADA'), ('EN PROCESO', 'EN PROCESO'), ('FINALIZADA', 'FINALIZADA'), ('CANCELADA', 'CANCELADA')])
    tipo_servicio = SelectField('Tipo de Servicio', choices=[('', 'Todos'), ('Desarrollo', 'Desarrollo'), ('Análisis', 'Análisis'), ('Consultoría', 'Consultoría')])
    cliente_username = StringField('Username de Cliente', validators=[Optional()])
    submit = SubmitField('Filtrar')
