from src.web import error


def register_errors(app):
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(503, error.service_unavaible)
    app.register_error_handler(403, error.forbbiden)
