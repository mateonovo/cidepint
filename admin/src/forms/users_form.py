from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class CreateUserForm(FlaskForm):
    class Meta:
        locales = ['es_ES']

    nombre = StringField('Nombre',
                         validators=[DataRequired(message="Este campo es obligatorio"),
                                     Length(max=64)])
    apellido = StringField('Apellido',
                           validators=[DataRequired(message="Este campo es obligatorio"),
                                       Length(max=64)])
    email = StringField('Email',
                        validators=[DataRequired(message="Este campo es obligatorio"),
                                    Email(message="El mail ingresado no es válido.")])
    contraseña = PasswordField('Contraseña',
                               validators=[DataRequired(message="Este campo es obligatorio")])
    confirmar_contraseña = PasswordField('Confirmar contraseña',
                                         validators=[DataRequired(message="Este campo es obligatorio"),
                                                     EqualTo('contraseña', message="Las contraseñas no coinciden")])
    enviar = SubmitField('Crear usuario')


class UpdateUserForm(FlaskForm):
    class Meta:
        locales = ['es_ES']

    nombre = StringField('Nombre',
                         validators=[DataRequired(message="Este campo es obligatorio"),
                                     Length(max=64)])
    apellido = StringField('Apellido',
                           validators=[DataRequired(message="Este campo es obligatorio"),
                                       Length(max=64)])
    email = StringField('Email',
                        validators=[DataRequired(message="Este campo es obligatorio"),
                                    Email(message="El mail ingresado no es válido.")])

    enviar = SubmitField('Editar')
