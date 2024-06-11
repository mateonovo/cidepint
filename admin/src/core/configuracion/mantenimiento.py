from src.core.database import database as db


class Mantenimiento(db.Model):
    __tablename__ = "mantenimiento"

    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(255))
    mode = db.Column(db.Boolean, default=False) 
    per_page = db.Column(db.Integer, default=10)


    def __init__(self, mode=False, mensaje=None, per_page=10):
        self.mode = mode
        self.mensaje = mensaje
        self.per_page = per_page
