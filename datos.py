from entidades import Usuario, Incidencia

# ================================================================
# CONFIGURACIÓN DE ADMINISTRADOR (AGREGAR ESTO)
# ================================================================
ADMIN_EMAIL = "admin@soluciones2t.com"
ADMIN_PASSWORD = "admin123"

# Usuarios
usuarios_registrados: list[Usuario] = []
usuarios_por_email: dict[str, Usuario] = {}
_contador_usuarios: int = 0

# Incidencias
incidencias_registradas: list[Incidencia] = []
incidencias_por_id: dict[int, Incidencia] = {}
_contador_incidencias: int = 0

# Funciones para IDs
def obtener_siguiente_id_usuario() -> int:
    global _contador_usuarios
    _contador_usuarios += 1
    return _contador_usuarios

def obtener_siguiente_id_incidencia() -> int:
    global _contador_incidencias
    _contador_incidencias += 1
    return _contador_incidencias

# Crear admin al inicio
def crear_admin_si_no_existe():
    admin_email = ADMIN_EMAIL  # <--- Usar constante
    admin_password = ADMIN_PASSWORD  # <--- Usar constante
    
    # Buscar si ya existe admin
    for usuario in usuarios_registrados:
        if usuario.email == admin_email:
            return
    
    # Crear admin
    admin = Usuario(
        id=obtener_siguiente_id_usuario(),
        nombre="Administrador",
        email=admin_email,
        contrasena=admin_password,
        rol="admin",
        telefono="",
        empresa="Soluciones 2T",
        sector="privado"
    )
    usuarios_registrados.append(admin)
    usuarios_por_email[admin.email] = admin