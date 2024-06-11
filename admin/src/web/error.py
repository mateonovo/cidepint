from flask import render_template
from src.core import configuracion


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La URL a la que quiere acceder no existe"
    }

    return render_template("error.html", **kwargs), 404


def unauthorized(e):
    kwargs = {
        "error_name": "401 Unauthorized",
        "error_description": """
            Usted no posee los permisos necesarios para
            ingresar a esta URL.
        """
    }

    return render_template("error.html", **kwargs), 401


def forbbiden(e):
    kwargs = {
        "error_name": "403 Forbbiden",
        "error_description": """
            Lo sentimos, no ha podido acceder al sistema.
            Por favor contacte a uno de los administradores.
        """
    }

    return render_template("error.html", **kwargs), 403


def service_unavaible(e):
    kwargs = {
        "error_name": "503 Service Unavailable",
        "error_description": configuracion.get_mensaje()
    }
    return render_template("error.html", **kwargs), 503
