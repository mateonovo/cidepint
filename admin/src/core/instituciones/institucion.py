from src.core.database import database as db
from datetime import datetime


class Institucion(db.Model):
    __tablename__ = "instituciones"  # Nombre de la tabla
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(50), nullable=False)
    informacion = db.Column(db.String(255), nullable=False)
    calle = db.Column(db.String(15), nullable=True)
    numero = db.Column(db.String(15), nullable=True)
    localizacion = db.Column(db.String(100), nullable=True)
    palabras_claves = db.Column(db.String(50), nullable=False)
    horarios = db.Column(db.String(50), nullable=True)
    web = db.Column(db.String(50), nullable=True)
    contacto = db.Column(db.String(50), nullable=False)
    habilitado = db.Column(db.Boolean, default=False)
    servicios = db.relationship('Servicio', back_populates='institucion', cascade='all, delete-orphan')
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nombre, informacion, localizacion, calle, numero,
                 palabras_claves, horarios, web, contacto, habilitado=False):
        self.nombre = nombre
        self.informacion = informacion
        self.localizacion = localizacion
        self.calle = calle
        self.numero = numero
        self.palabras_claves = palabras_claves
        self.horarios = horarios
        self.web = web
        self.contacto = contacto
        self.habilitado = habilitado
    

    def __str__(self):
        return self.nombre
