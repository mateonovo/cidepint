from flask import Blueprint, render_template, redirect, url_for, flash, abort
from src.web.helpers.auth import login_required, has_permissions
from src.web.helpers.maintenance import info_contacto as cache_info_contacto
from forms.maintenance_form import MaintenanceForm
from forms.maintenance_form import ContactoForm
from forms.maintenance_form import paginadoForm
from src.core import configuracion
from src.web.config import cache


maintenance_bp = Blueprint("maintenance", __name__, url_prefix="/maintenance")


@maintenance_bp.get('/')
@login_required
def index():
    if not has_permissions(['config_show']):
        abort(401)
    mensaje = configuracion.get_mensaje()  
    return render_template('configuraciones/maintenance_form.html', form=MaintenanceForm(),mensaje=mensaje)


@maintenance_bp.post('/toggle')
@login_required
def toggle_maintenance():
    """
    Está función se ejecuta cuando interactuamos con la configuración de
    mantenimiento dependiendo de si activamos o desactivamos el modo
    mantenimiento. También actualiza el mensaje que se mostrará.
    """
    if not has_permissions(['config_update']):
        abort(401)
    form = MaintenanceForm()
    if form.validate_on_submit():
        if form.activate_maintenance.data:
            configuracion.update_state(True)
            flash("Se activó modo Mantenimiento: ", "info")
        elif form.deactivate_maintenance.data:
            configuracion.update_state(False)
            flash("Se deactivó modo mantenimiento: ", "info")
        if form.mensaje.data:
            configuracion.update_mensaje(form.mensaje.data)
            flash("Nuevo mensaje guardado con exito ", "info")
        return redirect(url_for('maintenance.index'))


@maintenance_bp.get('/info_contacto')
@login_required
def info_contacto():
    """
    Muestra la informacion de contacto actual
    """
    if not has_permissions(['config_show']):
        abort(401)
    info = configuracion.get_info_contacto()
    return render_template('configuraciones/info_contacto.html', info=info)


@maintenance_bp.get('/contacto')
@login_required
def index_contacto():
    """
    Muestra el formulario para actualizar la informacion de contacto
    """
    if not has_permissions(['config_show']):
        abort(401)
    info = configuracion.get_info_contacto()
    form = ContactoForm(obj=info)
    return render_template('configuraciones/update_info.html', form=form)


@maintenance_bp.post('/update_contacto')
@login_required
def update_contacto():
    """
    Actualiza la información de contacto
    """
    if not has_permissions(['config_update']):
        abort(401)
    form = ContactoForm()
    if form.validate_on_submit():
        configuracion.update_info(form.telefono.data, form.email.data, form.direccion.data)
        cache.delete('info_contacto')
        c = cache_info_contacto()

        flash("Se guardaron los cambios correctamente", "info")
        return redirect(url_for('maintenance.info_contacto'))
    return render_template('configuraciones/update_info.html', form=form)


@maintenance_bp.get('/paginado')
@login_required
def index_paginado():
    if not has_permissions(['config_show']):
        abort(401)
    form = paginadoForm()
    per_page = configuracion.get_per_page()
    return render_template('configuraciones/paginado.html', form=form, per_page = per_page)


@maintenance_bp.post('/update_paginado')
@login_required
def update_paginado():
    if not has_permissions(['config_update']):
        abort(401)
    form = paginadoForm()
    if form.validate_on_submit():
        configuracion.update_per_page(form.per_page.data)
        flash("Se guardaron los cambios correctamente", "info")
        return redirect(url_for('maintenance.index_paginado'))
    return render_template('configuraciones/paginado.html')
