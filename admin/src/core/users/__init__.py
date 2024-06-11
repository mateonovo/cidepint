from src.core.users.role import Roles, UserRoleInstitution
from src.core.users.permission import Permissions
from src.core.database import database as db


def create_role(**kwargs):
    role = Roles(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role


def assign_role_in_institution_to_user(role, institution, user):
    insertion = UserRoleInstitution(user.id, institution.id, role.id)
    db.session.add(insertion)
    db.session.commit()
   
     
def assign_role_in_institution_to_user_by_id(role, institution, user):
    insertion = UserRoleInstitution(user, institution, role)
    db.session.add(insertion)
    db.session.commit()


def delete_role_in_institution_to_user_by_id(institution_id, user_id):
    UserRoleInstitution.query.filter_by(
        user_id=user_id, institution_id=institution_id
    ).delete()
    db.session.commit()


def create_permission(**kwargs):
    permission = Permissions(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission


def assign_permission_role(role, permission):
    role.permisos.append(permission)
    db.session.add(role)
    db.session.commit()


def list_permissions_by_user(user):
    """
    Obtiene los permisos de un usuario.
    Solo se usaría cuando el usuario se autentica.
    """
    list_permissions = set()
    for role in get_user_roles(user):
        for permission in role.permisos:
            list_permissions.add(permission.nombre)

    return list(list_permissions)


def set_permission(permission):
    return Permissions.query.filter_by(nombre=permission).first()


def get_user_roles(user):
    tuplas = UserRoleInstitution.query.filter_by(user_id=user.id).all()
    roles = set()
    for t in tuplas:
        roles.add(t.role)
    return list(roles)


def get_user_institutions(user):
    tuplas = UserRoleInstitution.query.filter_by(user_id=user.id).all()
    institutions = set()
    for t in tuplas:
        if t.institution_id != 1:
            institutions.add(t.institution)
    return list(institutions)


def get_user_institutions_by_role(user_id, role_id):
    tuplas = UserRoleInstitution.query.filter_by(user_id=user_id, role_id=role_id).all()
    institutions = set()
    for t in tuplas:
        if t.institution_id != 1:
            institutions.add(t.institution)
    return list(institutions)


def get_user_institutions_and_roles(user):
    """
    Esta función retorna una lista con tuplas, donde cada tupla representa a
    cada renglon de la tabla UserRoleInstitution a la cuál el usuario está
    presente.
    """
    tuplas = UserRoleInstitution.query.filter_by(user_id=user.id).all()
    institutions_roles = set()
    for t in tuplas:
        institutions_roles.add((t.institution, t.role))
    return list(institutions_roles)


def update_role_for_user_in_institution(user_id, institution_id, new_role_id):
    """
    Actualiza el rol de un usuario en una institución
    """
    user_institution_relationship = UserRoleInstitution.query.filter_by(
        user_id=user_id, institution_id=institution_id
    ).first()
    user_institution_relationship.role_id = new_role_id
    db.session.add(user_institution_relationship)
    db.session.commit()


def cascade_delete_user(user_id):
    UserRoleInstitution.query.filter_by(user_id=user_id).delete()
    db.session.commit()


def get_role_by_id(role_id):
    return Roles.query.get_or_404(role_id)


def get_role_in_institution(user_id, institution_id):
    return UserRoleInstitution.query.filter_by(user_id=user_id, institution_id=institution_id).first()


