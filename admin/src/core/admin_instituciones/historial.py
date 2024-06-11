from src.core.database import database as db


class Historial(db.Model):
    __tablename__ = "historial"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    rol_id = db.Column(db.Integer, nullable=False)
    institucion_id = db.Column(db.Integer, nullable=False)
   
 
    def __init__(self, email, user_id, rol_id, institucion_id):
        self.email = email
        self.user_id = user_id
        self.rol_id = rol_id
        self.institucion_id = institucion_id