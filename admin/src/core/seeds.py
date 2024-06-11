from src.core import auth
from src.core import users
from src.core import services
from src.core import api
from src.core import instituciones
from src.core import configuracion

def run():
    configuracion.create_maintenance(
        mensaje="Estamos en mantenimiento",
        mode=False
    )

    configuracion.create_info_contacto(
        email="",
        telefono="",
        direccion=""
    )

    # Creación de usuarios:
    user_superadmin = auth.create_User(
        email="juan@admin.com",
        password="1234",
        token=None,
        nombre="Juan",
        apellido="Perez",
        activo=True
    )


    user_op1 = auth.create_User(
        email="ana@op.com",
        password="1234",
        nombre="Ana",
        apellido="Diaz",
        activo=True
    )

    user_ow1 = auth.create_User(
        email="jose@owner.com",
        password="1234",
        nombre="Jose",
        apellido="Lopez",
        activo=True
    )

    user_admin1 = auth.create_User(
        email="pablo@admin.com",
        password="1234",
        nombre="Pablo",
        apellido="Garcia",
        activo=True
    )

    user_to_delete = auth.create_User(
        email="sacrifice@user.com",
        password="1234",
        nombre="Joe",
        apellido="Doe",
        activo=True
    )

    # Creación de roles:
    superadmin_role = users.create_role(nombre="superadmin")
    owner_role = users.create_role(nombre="owner")
    admin_role = users.create_role(nombre="admin")
    operator_role = users.create_role(nombre="operator")

    # Creación de instituciones:
    superadmin_institution = instituciones.create_institucion(
        nombre="Institucion de Superadministradores",
        informacion="",
        calle="",
        numero="",
        localizacion="",
        palabras_claves="",
        horarios="",
        web="",
        contacto=""
    )

    cidepint_institution = instituciones.create_institucion(
        nombre="Institucion CIDEPINT",
        informacion="Somos la institución principal",
        calle="10",
        numero="1356",
        localizacion="La Plata",
        palabras_claves="Pinturas Recubrimientos Investigacion Centro",
        horarios="08:00hs - 20:00hs",
        web="https://cidepint.ing.unlp.edu.ar/",
        contacto="0221 421-6214"
    )

    nueva_institucion = instituciones.create_institucion(
        nombre="Nueva Institucion",
        informacion="Somos",
        calle="8",
        numero="755",
        localizacion="Bs As",
        palabras_claves="Pinturas",
        horarios="24 hs",
        web="www.hola.com",
        contacto="123456"
    )

    institucion1 = instituciones.create_institucion(
        nombre="Institución 1",
        informacion="Somos la institución 1",
        calle="50",
        numero="1200",
        localizacion="La Plata",
        palabras_claves="Software Proyecto",
        horarios="10:00hs - 19:00hs",
        web="https://www.info.unlp.edu.ar/",
        contacto="0221 427-7270"
    )


    # Creación de permisos:
    # Modulo usuarios
    user_index_permission = users.create_permission(nombre="user_index")
    user_show_permission = users.create_permission(nombre="user_show")
    user_new_permission = users.create_permission(nombre="user_new")
    user_destroy_permission = users.create_permission(nombre="user_destroy")
    user_update_permission = users.create_permission(nombre="user_update")
    
    """
    creo  permisos para dueños de instituciones
    """
    owner_index_permission = users.create_permission(nombre="owner_index")
    owner_show_permission = users.create_permission(nombre="owner_show")
    owner_new_permission = users.create_permission(nombre="owner_new")
    owner_destroy_permission = users.create_permission(nombre="owner_destroy")
    owner_update_permission = users.create_permission(nombre="owner_update")
    
    
    


    # Modulo instituciones
    institution_index_permission = users.create_permission(nombre="institution_index")
    institution_show_permission = users.create_permission(nombre="institution_show")
    institution_new_permission = users.create_permission(nombre="institution_new")
    institution_destroy_permission = users.create_permission(nombre="institution_destroy")
    institution_update_permission = users.create_permission(nombre="institution_update")


    # Modulo configuracion
    user_config_show_permission = users.create_permission(nombre="config_show")
    user_config_update_permission = users.create_permission(nombre="config_update")
    
    
    #Modulo servicios
    services_index_permission = users.create_permission(nombre="services_index")
    services_show_permission = users.create_permission(nombre="services_show")
    services_new_permission = users.create_permission(nombre="services_new")
    services_destroy_permission = users.create_permission(nombre="services_destroy")
    services_update_permission = users.create_permission(nombre="services_update")
    
    
    #Modulo Solicitudes
    solicitudes_index_permission = users.create_permission(nombre="solicitudes_index")
    solicitudes_show_permission = users.create_permission(nombre="solicitudes_show")
    solicitudes_destroy_permission = users.create_permission(nombre="solicitudes_destroy")
    solicitudes_update_permission = users.create_permission(nombre="solicitudes_update")

    # Estadísticas de Vue
    statistics_index = users.create_permission(nombre="statistics_index")
    statistics_all_institutions = users.create_permission(nombre="statistics_all_institutions")


    # users.assign_role_user(user_superadmin, superadmin_role)
    # Asignación de usuarios en una institución con un rol:
    users.assign_role_in_institution_to_user(superadmin_role, superadmin_institution, user_superadmin)
    users.assign_role_in_institution_to_user(admin_role, cidepint_institution, user_admin1)
    users.assign_role_in_institution_to_user(owner_role, cidepint_institution, user_ow1)
    users.assign_role_in_institution_to_user(operator_role, cidepint_institution, user_op1)
    users.assign_role_in_institution_to_user(operator_role, cidepint_institution, user_to_delete)
    users.assign_role_in_institution_to_user(admin_role, nueva_institucion, user_ow1 )
    
    
    # Asignación de permisos y roles:
    #Modulo Instituciones
    users.assign_permission_role(superadmin_role, institution_index_permission)
    users.assign_permission_role(superadmin_role, institution_show_permission)
    users.assign_permission_role(superadmin_role, institution_new_permission)
    users.assign_permission_role(superadmin_role, institution_destroy_permission)
    users.assign_permission_role(superadmin_role, institution_update_permission)
    
    
    #Modulo configuracion
    users.assign_permission_role(superadmin_role, user_config_update_permission)
    users.assign_permission_role(superadmin_role, user_config_show_permission)
    
    
    #Modulo usuarios
    users.assign_permission_role(superadmin_role, user_index_permission)
    users.assign_permission_role(superadmin_role, user_show_permission)
    users.assign_permission_role(superadmin_role, user_new_permission)
    users.assign_permission_role(superadmin_role, user_destroy_permission)
    users.assign_permission_role(superadmin_role, user_update_permission)

    
    #Modulo servicios
    users.assign_permission_role(owner_role, services_index_permission)
    users.assign_permission_role(owner_role, services_show_permission)
    users.assign_permission_role(owner_role, services_update_permission)
    users.assign_permission_role(owner_role, services_new_permission)
    users.assign_permission_role(owner_role, services_destroy_permission)
    
    
    users.assign_permission_role(admin_role, services_index_permission)
    users.assign_permission_role(admin_role, services_show_permission)
    users.assign_permission_role(admin_role, services_update_permission)
    users.assign_permission_role(admin_role, services_new_permission)
    users.assign_permission_role(admin_role, services_destroy_permission)
    
    
    users.assign_permission_role(operator_role, services_index_permission)
    users.assign_permission_role(operator_role, services_show_permission)
    users.assign_permission_role(operator_role, services_update_permission)
    users.assign_permission_role(operator_role, services_new_permission)

    """
    asigno permisos a los usuarios dueños de las instituciones
    """
    users.assign_permission_role(owner_role,owner_index_permission  )
    users.assign_permission_role(owner_role,owner_show_permission )
    users.assign_permission_role(owner_role,owner_new_permission )
    users.assign_permission_role(owner_role,owner_destroy_permission)
    users.assign_permission_role(owner_role,owner_update_permission)
    

    #Modulo Solicitudes
    users.assign_permission_role(owner_role, solicitudes_index_permission)
    users.assign_permission_role(owner_role, solicitudes_show_permission)
    users.assign_permission_role(owner_role, solicitudes_update_permission)
    users.assign_permission_role(owner_role, solicitudes_destroy_permission)

    users.assign_permission_role(admin_role, solicitudes_index_permission)
    users.assign_permission_role(admin_role, solicitudes_show_permission)
    users.assign_permission_role(admin_role, solicitudes_update_permission)
    users.assign_permission_role(admin_role, solicitudes_destroy_permission)

    users.assign_permission_role(operator_role, solicitudes_index_permission)
    users.assign_permission_role(operator_role, solicitudes_show_permission)
    users.assign_permission_role(operator_role, solicitudes_update_permission)
                
    # Asignación de permisos para estadísticas
    users.assign_permission_role(owner_role, statistics_index)
    users.assign_permission_role(superadmin_role, statistics_index)
    users.assign_permission_role(superadmin_role, statistics_all_institutions)


    services.create_service(
        nombre="f",
        descripcion="f",
        keywords="f",
        tipo_servicio="Desarrollo",
        habilitado=True,
        institucion=cidepint_institution
    )
    
    api.create_user(
        username="fedeherce",
        nombre="Federico",
        apellido="Herce",
        tipo_documento="DNI",
        nro_documento="42708561",
        direccion="10 y 60",
        telefono='2920687309',
        email="fede@gmail.com",
        password="1234"
    )
    api.create_user(
        username="mateo",
        nombre="mateo",
        apellido="novo",
        tipo_documento="DNI",
        nro_documento="42338561",
        direccion="10 y 32",
        telefono='292056757309',
        email="mateo@gmail.com",
        password="1234"
    )

    services.create_solicitud(
        servicio_id=1,
        cliente_id=1,
        detalles="Detalles"
    )

    services.create_solicitud(
        servicio_id=1,
        cliente_id=1,
        detalles="Otros detalles"
    )