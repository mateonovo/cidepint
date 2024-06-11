from src.core.database import database as db
from datetime import datetime
from src.core.api import ApiUsers


class Servicio(db.Model):
    __tablename__ = "servicios"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    keywords = db.Column(db.String(200), nullable=False)
    tipo_servicio = db.Column(db.Enum('Análisis', 'Consultoría', 'Desarrollo',name="tipo_servicio_enum"), nullable=False)
    habilitado = db.Column(db.Boolean, nullable=False)
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones.id'))
    institucion = db.relationship("Institucion", back_populates='servicios')
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nombre, descripcion, keywords, tipo_servicio, habilitado, institucion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.keywords = keywords
        self.tipo_servicio = tipo_servicio
        self.habilitado = habilitado
        self.institucion = institucion


class Solicitud(db.Model):
    __tablename__ = "solicitudes"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"))
    cliente_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    detalles = db.Column(db.String(500), nullable=True)
    estado = db.Column(db.String(20), nullable=False, default='EN PROCESO')  # Estados: aceptada, rechazada, en proceso, finalizada, canceladaa
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cambio_estado = db.Column(db.DateTime, default=datetime.utcnow)
    observacion_cambio_estado = db.Column(db.String(200), default='')
    comentario = db.Column(db.String(500), default='')
    # Falta el campo de archivos adjuntos
    cliente = db.relationship('Users', backref='solicitudes')
    servicio = db.relationship('Servicio', backref='solicitudes')

    def __init__(self, servicio_id, cliente_id, detalles):
        self.servicio_id = servicio_id
        self.cliente_id = cliente_id
        self.detalles = detalles
