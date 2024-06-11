from flask import Blueprint, render_template, abort, request
from flask import redirect, url_for, flash
from src.core import auth
from src.core import users
from src.core import instituciones
from src.forms.users_form import CreateUserForm, UpdateUserForm
from src.web.helpers.auth import login_required, has_permissions, user_is_superadmin
from src.core import configuracion

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/")
@login_required
def index():
    if not has_permissions(['user_index']):
        abort(401)

    page = request.args.get('page', type=int, default=1)
    per_page = configuracion.get_per_page()

    email = request.args.get('email', default="")
    estado = request.args.get('estado', default="todos")

    users = get_users(email, estado, page, per_page)

    return render_template("users/index.html", users=users.items, pagination=users)


def get_users(email, estado, page, per_page):
    return auth.filter_users(email, estado, page, per_page)


@users_bp.get("/profile/<int:user_id>")
@login_required
def user_profile(user_id):
    if not has_permissions(['user_show']):
        abort(401)

    user = auth.get_user_by_id(user_id)
    is_superadmin = user_is_superadmin(user=user)

    instituciones_del_usuario = users.get_user_institutions(user)

    # Obtengo las instituciones y roles del usuario
    instituciones_roles = users.get_user_institutions_and_roles(user)

    # Obtengo todas las instituciones a las que el usuario NO pertenece
    otras_instituciones = [inst for inst in instituciones.list_instituciones()
                           if inst not in instituciones_del_usuario]

    return render_template(
        "users/profile.html",
        user=user,
        user_is_superadmin=is_superadmin,
        instituciones_roles=instituciones_roles,
        otras_instituciones=otras_instituciones
    )


@users_bp.route("/update_user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if not has_permissions(['user_update']):
        abort(401)

    user = auth.get_user_by_id(user_id)
    form = UpdateUserForm()

    if form.validate_on_submit():
        if user.email != form.email.data:
            existe = auth.find_user_by_mail(form.email.data)
            if existe:
                flash('Este correo electrónico ya está en uso. Por favor, elige otro.', 'error')
                return redirect(url_for("users.update_user", user_id=user.id))

        auth.update_name_surname_email(user, form.nombre.data, form.apellido.data, form.email.data)
        flash("Usuario actualizado con éxito!", "success")
        return redirect(url_for("users.user_profile", user_id=user.id))

    elif request.method == "GET":
        form.nombre.data = user.nombre
        form.apellido.data = user.apellido
        form.email.data = user.email

    return render_template("users/update_user.html", user_id=user.id, form=form)


@users_bp.post("/update_state/<int:user_id>")
@login_required
def update_state(user_id):
    if not has_permissions(['user_update']):
        abort(401)

    user = auth.get_user_by_id(user_id)
    auth.update_state(user)

    return redirect(url_for("users.user_profile", user_id=user_id))


@users_bp.post("/destroy_user/<int:user_id>")
@login_required
def destroy_user(user_id):
    if not has_permissions(['user_destroy']):
        abort(401)

    user = auth.get_user_by_id(user_id)
    users.cascade_delete_user(user_id)
    auth.delete_user(user)

    flash("Usuario eliminado con éxito", "success")
    return redirect(url_for("users.index"))


@users_bp.route("/create_user", methods=['GET', 'POST'])
@login_required
def create_user():
    if not has_permissions(['user_new']):
        abort(401)

    if request.method == "GET":
        form = CreateUserForm()
        return render_template("users/create_user.html", form=form)

    form = CreateUserForm()
    if form.validate_on_submit():
        existe = auth.find_user_by_mail(form.email.data)
        if existe:
            flash('Este correo electrónico ya está en uso. Por favor, elige otro.', 'error')
            return redirect(url_for("users.create_user"))

        user = auth.create_User(
            email=form.email.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            password=form.contraseña.data,
            token=None,
            activo=True
        )
        flash("Usuario creado con éxito!", "success")
        return redirect(url_for("users.user_profile", user_id=user.id))

    return render_template("users/create_user.html", form=form)


@users_bp.post("/update_role_institution/<int:institution_id>/<int:user_id>")
@login_required
def update_role_institution(institution_id, user_id):
    """
    Esta función actualiza el rol del usuario en una institución.
    Esta implementación es posible ya que sabemos el id de cada rol
    (definido por nosotros en la BD)
    """
    if not has_permissions(['user_update']):
        abort(401)

    new_role = get_role_requested(request.form.get("new_role"))
    if (new_role != -1):
        users.update_role_for_user_in_institution(user_id, institution_id, new_role)
    else:
        users.delete_role_in_institution_to_user_by_id(institution_id, user_id)
    return redirect(url_for("users.user_profile", user_id=user_id))


@users_bp.post("/assign_role_institution/<int:institution_id>/<int:user_id>")
@login_required
def assign_role_institution(institution_id, user_id):
    if not has_permissions(['user_update']):
        abort(401)

    new_role = get_role_requested(request.form.get("new_role"))
    user = auth.get_user_by_id(user_id)
    institution = instituciones.find_institucion_by_id(institution_id)
    role = users.get_role_by_id(new_role)

    users.assign_role_in_institution_to_user(role, institution, user)
    return redirect(url_for("users.user_profile", user_id=user_id))


def get_role_requested(new_role):
    if (new_role == "owner"):
        return 2
    elif (new_role == "admin"):
        return 3
    elif (new_role == "operator"):
        return 4
    elif (new_role == "none"):
        return -1
