from flask import Blueprint, render_template, request, session
from flask import redirect, url_for, flash
from src.core import auth
from src.core import users
from src.core import admin_instituciones
from src.web.helpers.auth import login_required, has_permissions
from flask import current_app as app
from flask import abort
from src.web.helpers.auth import user_is_superadmin
from src.core import configuracion

admin_users_bp = Blueprint("admin", __name__, url_prefix="/administracion")



def institutions_of_owner():
    owner = auth.find_user_by_mail(session["user_id"])
    return users.get_user_institutions_by_role(owner.id, 2)


@admin_users_bp.get("/")
@login_required
def buscar_usuario():
    if not has_permissions(['owner_index']):
        abort(401)
    inst = institutions_of_owner()
    return render_template("admin_usuarios/buscar.html", inst=inst)


@admin_users_bp.post("/")
@login_required
def buscar():
    """
    Esta función toma una institución de las que el usuario es
    dueño y un usuario. Si el usuario existe, lo redirige para darle
    o quitarle un rol. Si el usuario no existe o es el superadmin, le indica
    que no se encuentra registrado.
    """
    email = request.form['email']
    institucion_id = request.form['institucion_id']
    user = auth.find_user_by_mail(email)
    if user and not user_is_superadmin(user):
        return redirect(url_for('admin.asignar_rol', institucion_id=institucion_id, email=email))
    else:
        flash("Ese usuario no se encuentra registrado")
        return redirect(url_for('admin.buscar'))


@admin_users_bp.get("/asignar_rol/<int:institucion_id>/<string:email>")
@login_required
def asignar_rol(institucion_id, email):
    """
    Esta función analiza si el usuario selecciona posee un rol en la institucíon,
    para mostrar en el template la opcion de asignar el rol por primera vez, 
    actualizarlo o quitarlo
    """
    if not has_permissions(['owner_update', 'owner_new', 'owner_destroy']):
        abort(401)
       
    rolActual = ''
    user_id = auth.find_user_by_mail(email).id
    rol_actual_id = users.get_role_in_institution(user_id, institucion_id)
    if rol_actual_id is not None:
        rolActual = users.get_role_by_id(rol_actual_id.role_id).nombre
      
    return render_template("admin_usuarios/asignar.html", 
                           user_id=user_id,
                           institucion_id=institucion_id,
                           rolActual=rolActual)


@admin_users_bp.post("/asignar_rol_post/<int:institucion_id>/<int:user_id>")
@login_required
def asignar(institucion_id, user_id):
    """
    Se le crea un rol al usuario en la institucion si no posee uno , 
    En caso de tenerlo se lo actualiza o elimina
    """
  
    rol = int(request.form['rol']) 
    if users.get_role_in_institution(user_id, institucion_id) is None: 
        users.assign_role_in_institution_to_user_by_id(rol, institucion_id, user_id)
        flash("Se asigno el rol correctamente")
    elif (rol == 5):
        users.delete_role_in_institution_to_user_by_id(institucion_id, user_id)
        flash("Se ha quitado el rol correctamente")   
    else:
        users.update_role_for_user_in_institution(user_id, institucion_id, rol)    
        flash("Se actualizo el rol correctamente")      
    create_historial(user_id, institucion_id, rol)
    return redirect(url_for('admin.buscar_usuario'))


def create_historial(user_id, inti_id, rol_id):
    email = auth.find_user_email_by_id(user_id)
    historial = admin_instituciones.create_historial(
        user_id=user_id,
        institucion_id=inti_id, 
        rol_id=rol_id,
        email=email)
    return historial


@admin_users_bp.get("/ver_historial/<int:institucion_id>")
@login_required
def ver_historial(institucion_id):
    if not has_permissions(['owner_index']):
        abort(401)
    page = request.args.get('page', type=int, default=1)
    per_page = configuracion.get_per_page()
    asigns = admin_instituciones.paginate_historial(page, per_page, institucion_id)
    roles = {
        2: "dueño",
        3: "Administrador",
        4: "operador",
        5: "se quito rol"
    }
    return render_template("admin_usuarios/historial.html", asigns=asigns, roles=roles)


@admin_users_bp.post("/historial")
@login_required
def historial():
    institucion_id = request.form['institucion_id']
    return redirect(url_for('admin.ver_historial', institucion_id=institucion_id))


@admin_users_bp.get("/select")
@login_required
def select():
    if not has_permissions(['owner_index']):
        abort(401)
    inst = institutions_of_owner()
    return render_template("admin_usuarios/select.html", list_instituciones=inst)
