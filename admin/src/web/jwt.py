from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from datetime import timedelta
from flask import jsonify


def init_jwt(app):
    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = "grupo17-1"
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    @app.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(e):
        return jsonify(error="Token JWT no proporcionado. Inicie sesión para acceder a este recurso."), 401
