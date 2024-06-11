from sqlalchemy import Column, Integer, String
from src.core.database import database as db


class ApiUsers(db.Model):
    __tablename__ = "apiusers"  # Nombre de la tabla
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(50), nullable=False)
    nombre = Column(String(40), nullable=False)
    apellido = Column(String(40), nullable=False)
    tipo_documento = Column(String(15), nullable=False)
    nro_documento = Column(String(15), nullable=False)
    direccion = Column(String(50), nullable=False)
    telefono = Column(String(15), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(100), nullable=True)
