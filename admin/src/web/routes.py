from src.web.controllers.auth import auth_bp
from src.web.controllers.users import users_bp
from src.web.controllers.services import services_bp
from src.web.controllers.maintenance import maintenance_bp
from src.web.api.api import api_bp
from src.web.controllers.instituciones import instituciones_bp
from src.web.controllers.home import home_bp
from src.web.controllers.administracion_instituciones import admin_users_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(instituciones_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_users_bp)