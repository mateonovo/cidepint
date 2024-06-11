from src.web.helpers import auth
from src.web.helpers import maintenance
from src.web.helpers import institutions


def register_jinja_env_globals(app):
    app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)
    app.jinja_env.globals.update(has_permissions=auth.has_permissions)
    app.jinja_env.globals.update(is_superadmin=auth.is_superadmin)
    app.jinja_env.globals.update(is_maintenance=maintenance.is_maintenance)
    app.jinja_env.globals.update(user_institutions=institutions.user_institutions)
    app.jinja_env.globals.update(is_owner=auth.is_owner)
    app.jinja_env.globals.update(info_contacto=maintenance.info_contacto)
