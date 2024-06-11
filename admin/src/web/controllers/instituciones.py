from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from src.core import instituciones
from src.web.helpers.auth import login_required, has_permissions
from forms.institucion_form import InstitucionForm
from flask import current_app as app
from src.core import configuracion


instituciones_bp = Blueprint("instituciones", __name__, url_prefix="/instituciones")


@instituciones_bp.route('/', methods=['GET'])
@login_required
def list_instituciones():

    """
    Este método se encarga de traer las instituciones,
    paginadas según las configuraciones aplicadas. 
    """

    if not has_permissions(['institution_index']):
        abort(401)

    page = request.args.get('page', type=int, default=1)
    per_page = configuracion.get_per_page()
    paginated_instits = instituciones.paginate_instituciones(page, per_page)
    return render_template("instituciones/list_instituciones.html", instits=paginated_instits)


@instituciones_bp.route('/<int:id>', methods=['GET'])
@login_required
def show(id):
    if not has_permissions(['institution_show']):
        abort(401)
    instit = instituciones.find_institucion_by_id(id)
    return render_template("instituciones/institucion.html", instit=instit)


@instituciones_bp.route('/habilitar_institucion/<int:id>', methods=['POST'])
@login_required
def habilitar_institucion(id):
    """
    Este método cambia el flag de Habilitado de una institucion.
    Si está habilitada, la deshabilita y viceversa
    """
    if not has_permissions(['institution_update']):
        abort(401)
    instit = instituciones.find_institucion_by_id(id)

    instituciones.habilitar_institucion(instit, not instit.habilitado)

    return render_template("instituciones/institucion.html", instit=instit)

@instituciones_bp.get("/create")
@login_required
def create():
    if not has_permissions(['institution_new']):
        abort(401)
    form = InstitucionForm()
    return render_template("instituciones/create_institucion.html", form=form)


@instituciones_bp.post("/create_institucion")
@login_required
def create_institucion():
    if not has_permissions(['institution_new']):
        abort(401)
    form = InstitucionForm()
    if form.validate_on_submit():
        instituciones.create_institucion(
            nombre=form.nombre.data,
            informacion=form.informacion.data,
            calle=form.calle.data,
            numero=form.numero.data,
            localizacion=form.localizacion.data,
            palabras_claves=form.palabras_claves.data,
            horarios=form.horarios.data,
            web=form.web.data,
            contacto=form.contacto.data
        )
        flash('Institucion agregada exitosamente', 'success')
        return redirect(url_for('instituciones.list_instituciones'))
    return render_template("instituciones/create_institucion.html", form=form)


@instituciones_bp.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):

    """
    Este método actualiza la institución con los
    nuevos valores que se obtienen desde el formulario
    """

    if not has_permissions(['institution_update']):
        abort(401)
    instit = instituciones.find_institucion_by_id(id)

    form = InstitucionForm(obj=instit)

    if form.validate_on_submit():
        instituciones.update_institucion(
            instit,
            nombre=form.nombre.data,
            informacion=form.informacion.data,
            calle=form.calle.data,
            numero=form.numero.data,
            localizacion=form.localizacion.data,
            palabras_claves=form.palabras_claves.data,
            horarios=form.horarios.data,
            web=form.web.data,
            contacto=form.contacto.data
        )

        flash('Institución actualizada exitosamente', 'success')
        return redirect(url_for('instituciones.list_instituciones'))

    return render_template("instituciones/update_institucion.html", instit=instit, form=form)


@instituciones_bp.route('/destroy/<int:id>', methods=['POST', 'DELETE'])
@login_required
def destroy(id):
    if not has_permissions(['institution_destroy']):
        abort(401)
    instituciones.delete_institucion(id)
    flash('Institución eliminada exitosamente', 'success')
    return redirect(url_for('instituciones.list_instituciones'))
