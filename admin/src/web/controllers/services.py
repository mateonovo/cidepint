from datetime import datetime
from flask import Blueprint, render_template, abort
from flask import flash, redirect, url_for, request
from src.forms.servicios_form import ServiciosForm
from src.forms.servicios_form import ActualizarSolicitudesForm
from src.forms.servicios_form import FiltroSolicitudesForm
from src.web.helpers.auth import login_required, has_permissions
from src.web.helpers.institutions import user_in_institution
from src.core import services, instituciones, api
from src.core import configuracion
from src.core import auth


services_bp = Blueprint("services", __name__, url_prefix="/services")


@services_bp.get("/<int:institucion_id>")
@login_required
@user_in_institution
def index(institucion_id):
    """
     Este método se encarga de mostrar los servicios de manera páginada 
     segun el valor que se encuentre en el archivo de configuración.
    """
    if not has_permissions(['services_index']):
        abort(401)
    page = request.args.get('page', type=int, default=1)
    per_page = configuracion.get_per_page()
    paginated_services = services.paginate_services(page, per_page, institucion_id)
    nombre_institucion = instituciones.find_institucion_by_id(institucion_id).nombre
    return render_template("services/index.html",
                           services=paginated_services,
                           institucion_id=institucion_id,
                           nombre=nombre_institucion)


@services_bp.get("/agregar/<int:institucion_id>")
@login_required
@user_in_institution
def agregar(institucion_id):
    if not has_permissions(['services_new']):
        abort(401)
    form = ServiciosForm()
    return render_template("services/agregar_servicio.html",
                           form=form,
                           institucion_id=institucion_id)


@services_bp.post("/agregar_servicio/<int:institucion_id>")
@login_required
@user_in_institution
def agregar_servicio(institucion_id):
    """
    Este método se encarga de de agregar un
    servicio a una institución específica segun su ID
    """
    form = ServiciosForm()
    if form.validate_on_submit():
        services.create_service(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            keywords=form.keywords.data,
            tipo_servicio=form.tipo_servicio.data,
            habilitado=form.habilitado.data,
            institucion=instituciones.find_institucion_by_id(institucion_id)
        )
        flash('Servicio creado con exito', 'success')
        return redirect(url_for('services.index',
                                institucion_id=institucion_id))
    return render_template("services/agregar_servicio.html",
                           form=form,
                           institucion_id=institucion_id)


@services_bp.get("/editar/<int:servicio_id>/<int:institucion_id>")
@login_required
@user_in_institution
def editar(servicio_id, institucion_id):
    if not has_permissions(['services_update']):
        abort(401)
    servicio = services.get_service(servicio_id)
    form = ServiciosForm(obj=servicio)
    return render_template('services/editar_servicio.html',
                           form=form,
                           servicio=servicio,
                           institucion_id=institucion_id)


@services_bp.post("/editar_servicio/<int:servicio_id>/<int:institucion_id>")
@login_required
@user_in_institution
def editar_servicio(servicio_id, institucion_id):
    """
    Este método se encarga de mostrar un formulario para editar un
    servicio con los nuevos datos ingresados por el usuario
    """
    servicio = services.get_service(servicio_id)
    form = ServiciosForm()
    if form.validate_on_submit():
        services.update_service(form, servicio)
        flash('Servicio actualizado correctamente', 'success')
        return redirect(url_for("services.index",
                                institucion_id=institucion_id))
    return render_template('services/editar_servicio.html',
                           form=form,
                           institucion_id=institucion_id)


@services_bp.post("/eliminar/<int:servicio_id>/<int:institucion_id>")
@login_required
@user_in_institution
def eliminar(servicio_id, institucion_id):
    if not has_permissions(['services_destroy']):
        abort(401)
    services.delete_service(servicio_id)
    flash('Servicio eliminado correctamente', 'success')
    return redirect(url_for("services.index", institucion_id=institucion_id))


#------------------------------------------------


@services_bp.route("/index_solicitudes/<int:institucion_id>", methods=['POST', 'GET'])
@login_required
@user_in_institution
def index_solicitudes(institucion_id):
    """
    Este método lista todas las solicitudes y permite filtrarlas
    por un rango de fechas, username del cliente que la realizó
    estado de la solicitud o tipo de servicio de la misma
    """
    if not has_permissions(['solicitudes_index']):
        abort(401)
    form = FiltroSolicitudesForm()  # Asume que tienes un formulario para el filtrado
    page = request.args.get('page', type=int, default=1)
    per_page = configuracion.get_per_page()

    if form.validate_on_submit():
        inicio = None
        fin = None
        estado = None
        tipo = None
        username = None
        if form.fecha_inicio.data:
            inicio = form.fecha_inicio.data

        if form.fecha_fin.data:
            fin = form.fecha_fin.data

        if form.estado.data:
            estado = form.estado.data

        if form.tipo_servicio.data:
            tipo = form.tipo_servicio.data

        if form.cliente_username.data:
            username = form.cliente_username.data
        
        solicitudes = services.paginate_solicitudes_filtradas(page, per_page, inicio, fin, estado, tipo, username, institucion_id)
    else:
        solicitudes = services.paginate_solicitudes(page, per_page, institucion_id)

    return render_template("services/index_solicitudes.html", solicitudes=solicitudes, form=form, institucion_id=institucion_id)


@services_bp.route("/show_solicitud/<int:id>", methods=['POST', 'GET'])
@login_required
def show_solicitud(id):
    if not has_permissions(['solicitudes_show']):
        abort(401)
    solicitud = services.show_solicitud(id)
    cliente = auth.get_user_by_id(solicitud.cliente_id)
    servicio = services.get_service(solicitud.servicio_id)
    return render_template("services/solicitud.html", solicitud=solicitud, cliente=cliente, servicio=servicio)


@services_bp.post("/update_solicitud/<int:id>")
@login_required
def update_solicitud(id):
    """
    Este método permite cambiar el estado de una solicitud.
    Si está 'En proceso' puede ser 'Aceptada' o 'Rechazada',
    y si es 'Aceptada' puede pasar a 'Finalizada' o 'Cancelada'
    Ademas puede realizar una observacion con respecto a 
    dicho cambio y escribir un comentario general en la misma.
    """

    if not has_permissions(['solicitudes_update']):
        abort(401)
    solicitud = services.show_solicitud(id)
    form = ActualizarSolicitudesForm(obj=solicitud)
    form.set_estado_choices(solicitud)

    if form.validate_on_submit():
        if (form.estado.data == solicitud.estado and form.comentario.data != ''):
            services.update_solicitud(solicitud, comentario=form.comentario.data)
        elif (form.comentario.data == ''):
            services.update_solicitud(
                solicitud,
                estado=form.estado.data,
                observacion_cambio_estado=form.observacion_cambio_estado.data,
                fecha_cambio_estado=datetime.utcnow(),
            )
        else:
            services.update_solicitud(
                solicitud,
                estado=form.estado.data,
                observacion_cambio_estado=form.observacion_cambio_estado.data,
                fecha_cambio_estado=datetime.utcnow(),
                comentario=form.comentario.data
            )

        flash('Solicitud actualizada exitosamente', 'success')

        return redirect(url_for('services.show_solicitud', id=solicitud.id))

    return render_template("services/update_solicitud.html", solicitud=solicitud, form=form)


@services_bp.route("/destroy_solicitud/<int:id>", methods=['POST', 'DELETE'])
@login_required
def destroy_solicitud(id):
    if not has_permissions(['solicitudes_destroy']):
        abort(401)
    services.delete_solicitud(id)
    flash('Solicitud eliminada exitosamente', 'success')
    return redirect(url_for('services.index_solicitudes'))
