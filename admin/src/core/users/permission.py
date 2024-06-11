from src.core.database import database as db
from src.core.users.role import role_permissions


class Permissions(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    roles = db.relationship("Roles", secondary=role_permissions, back_populates="permisos")

    def __init__(self, nombre):
        self.nombre = nombre
