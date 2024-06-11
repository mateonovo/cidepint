from flask import Blueprint, render_template
from flask import redirect, url_for, flash, session, abort, request
from flask_oauthlib.client import OAuth
from src.core import auth
from src.core import users
from forms.registro_form import SignUpForm, PasswordForm
from flask_mail import Message
from core.mail import mail
import secrets
from src.web.helpers.auth import has_permissions_mail, user_is_superadmin
from flask import current_app
from src.web.helpers.maintenance import maintenanceActivated
from src.core import configuracion
from flask_jwt_extended import create_access_token, set_access_cookies,unset_jwt_cookies,jwt_required
from flask import jsonify
from src.core import api

auth_bp = Blueprint("auth", __name__, url_prefix="/sesion")


@auth_bp.get("/")
def login():
    return render_template("auth/login.html")


@auth_bp.post("/authenticate")
def authenticate():
    """
    Esta función verifica las credenciales ingresadas.
    - Si el modo mantenimiento está activado y el usuario no cuenta con
    los permisos -> 503
    - Si el usuario está bloqueado -> 403
    - Sino, se crea la sesión con el mail del usuario, sus permisos y si es
    superadmin (solo lo usamos para las vistas).
    """
    params = request.form
    user = auth.check_user(params["email"], params["password"])

    if not user:
        flash("Email o clave incorrecta", "error")
        return redirect(url_for("auth.login"))

    if configuracion.get_state() and not has_permissions_mail(['config_show'], user.email):
        return abort(503)
    elif not user.activo:
        return abort(403)
    else:
        session["user_id"] = user.email
        session["is_superadmin"] = user_is_superadmin(user)
        session["permissions"] = users.list_permissions_by_user(user)
        flash("La sesion se inicio correctamente", "success")

    return redirect(url_for("home.index"))



@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()
        return redirect(url_for('home.index'))
    else:
        flash("No hay usuario logueado. Por favor, inicia sesión antes de cerrar sesión.", "warning")
        return redirect(url_for('auth.login'))


def generate_confirmation_token():
    token = secrets.token_urlsafe(16)
    return token


@auth_bp.get("/register")
@maintenanceActivated
def register():
    form = SignUpForm()
    return render_template("auth/register.html", form=form)


@auth_bp.post("/register_user")
@maintenanceActivated
def register_user():
    """
    Registra a un usuario, verifica la unicidad del correo electrónico,
    crea un token de confirmación y envía un correo para completar el registro.
    """
    form = SignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        existing_user = auth.find_user_by_mail(email)

        if existing_user and existing_user.google_id is None:
            flash('Este correo electrónico ya está en uso. Por favor, elige otro.', 'error')
            return redirect(url_for('auth.register'))

        if existing_user and existing_user.google_id is not None:
            token = generate_confirmation_token()
            auth.add_token(existing_user, token)
            send_confirmation_email(existing_user.email, token)
            flash('Tu cuenta ha sido creada, se envió un correo y se asoció con tu cuenta de Google', 'success')
            return redirect(url_for('home.index'))

        token = generate_confirmation_token()
        auth.create_user_no_pw(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=email,
            token=token
        )
        send_confirmation_email(email, token)
        flash('Tu cuenta ha sido creada, se envió un correo electrónico.', 'success')
        return redirect(url_for('home.index'))

    return render_template("auth/register.html", form=form)


def send_confirmation_email(email, token):
    """
    Este metodo envia un email al usuario registrado para que 
    confirme su registro, y enviará una url distinta si el sitio
    se encuentra corriendo en Producción o Desarrollo
    """
    msg = Message(
        'Confirma tu registro',
        sender='cidepint.proyecto@gmail.com',
        recipients=[email])
    url = current_app.config['URL_REGISTRO']
    confirmation_link = f'{url}/{email}/{token}'
    msg.html = f"""
                Para confirmar tu registro, haz clic en el siguiente enlace:
                <a href="{confirmation_link}">Confirmar Registro</a>'
                """
    mail.send(msg)


@auth_bp.get("/confirmar_registro/<email>/<token>")
def confirm_registration(email, token):
    user = auth.find_user_by_token(token)
    if user:
        form = PasswordForm()
        return render_template(
            'auth/confirmar_registro.html',
            form=form,
            email=email,
            token=token
        )
    else:
        abort(404)


@auth_bp.post("/guardar_contrasenia/<email>/<token>")
def save_password(email, token):
    form = PasswordForm()
    auth.enter_password(form.password.data, email)
    auth.delete_token(email)
    flash('Contraseña seteada con exito', 'success')
    return redirect(url_for('home.index'))


@auth_bp.get("/google")
def google():
    """
    Inicia el flujo de autenticación con Google.

    Retorna una redirección a la página de autorización de Google.
    """
    return current_app.extensions['oauthlib.client'].google.authorize(
        callback=url_for('auth.google_authorized', _external=True)
    )


@auth_bp.get("/google/authorized")
def google_authorized():
    """
    Callback para manejar la respuesta de autorización de Google.

    Si la autorización es exitosa, se crea una sesión para el usuario y se redirige a la página principal.
    Si la autorización falla, se devuelve un error 401.

    :return: Redirección a la página principal o error 401.
    """
    response = current_app.extensions['oauthlib.client'].google.authorized_response()
    if response is None or response.get('access_token') is None:
        abort(401)

    session['google_token'] = (response['access_token'], '')

    google_user = current_app.extensions['oauthlib.client'].google.get('userinfo')
    user_info = google_user.data
    user_email = user_info.get('email')

    google_id = user_info.get('id')
    existe = auth.find_user_by_mail(user_email)

    if existe:
        msg = 'La sesión se inició correctamente.'
        if existe.password is not None and existe.google_id is None:
            auth.add_google_id(existe, google_id)
            msg += ' Tu cuenta de Google se asoció junto con la cuenta que ya tenías.'
        create_session_google(existe, session)
        flash(msg, 'success')
        return redirect(url_for('home.index'))
    else:
        user_name = user_info.get('given_name')
        user_lastname = user_info.get('family_name')
        user = auth.create_user_no_pw(
            nombre=user_name,
            apellido=user_lastname,
            email=user_email,
            google_id=google_id
        )
        create_session_google(user, session)
        flash('Tu cuenta de Google ha sido añadida con éxito!', 'success')
        return redirect(url_for('home.index'))


def create_session_google(user, session):
    """
    Crea una sesión para el usuario después de la autenticación con Google.
    """
    session['user_id'] = user.email
    session['is_superadmin'] = user_is_superadmin(user)
    session['permissions'] = users.list_permissions_by_user(user)
