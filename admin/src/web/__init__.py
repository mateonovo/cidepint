from flask import Flask
from flask import session
from flask_oauthlib.client import OAuth
from src.core import database, mail
from src.web.config import config, cache
from src.web import routes
from src.web import commands
from src.web import error_handlers
from src.web import jinja
from src.web import jwt
from src.web import oauth
import logging
from flask_cors import CORS


#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    CORS(app, supports_credentials=True)
    database.init_app(app)
    mail.init_app(app)
    jwt.init_jwt(app)
    routes.register_routes(app)
    commands.register_commands(app)
    error_handlers.register_errors(app)
    jinja.register_jinja_env_globals(app)
    cache.init_app(app)
    oauth.init_app(app)

    return app
