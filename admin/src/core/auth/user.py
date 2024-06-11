from src.core.database import database as db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"  # Nombre de la tabla
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(32), unique=True, nullable=True)
    activo = db.Column(db.Boolean, default=False)
    google_id = db.Column(db.String, unique=True, nullable=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nombre, apellido, email, token=None, password=None, activo=False, google_id=None):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.token = token
        self.password = password
        self.activo = activo
        self.google_id = google_id
