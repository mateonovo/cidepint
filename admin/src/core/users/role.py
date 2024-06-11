from src.core.database import database as db


role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id",
              db.Integer,
              db.ForeignKey("roles.id")),
    db.Column("permission_id",
              db.Integer,
              db.ForeignKey("permissions.id"))
)


class UserRoleInstitution(db.Model):
    __tablename__ = "user_institution_role"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    institution_id = db.Column(db.Integer, db.ForeignKey("instituciones.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    # Relaciones con las tablas relacionadas
    user = db.relationship("Users")
    institution = db.relationship("Institucion")
    role = db.relationship("Roles")

    def __init__(self, user_id, institution_id, role_id):
        self.user_id = user_id
        self.institution_id = institution_id
        self.role_id = role_id


class Roles(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    permisos = db.relationship("Permissions",
                               secondary=role_permissions,
                               back_populates="roles")

    def __init__(self, nombre):
        self.nombre = nombre
