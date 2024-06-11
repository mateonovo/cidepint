from src.core.database import database as db


class Contacto(db.Model):
    __tablename__ = "contacto"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    direccion = db.Column(db.String(255))

    def __init__(self, email, telefono, direccion):
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
