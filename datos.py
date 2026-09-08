from entidades import Usuario, Incidencia, Cliente

# Usuario
usuarios_registrados: list[Usuario] = []
usuarios_por_email: dict[str, Usuario] = {}
_contador_usuarios: int = 0

# Incidencias
incidencias_registradas: list[Incidencia] = []
incidencias_por_id: dict[int, Incidencia] = {}
_contador_incidencias: int = 0

# CLientes
clientes_registrados: list[Cliente] = []
clientes_por_email: dict[str, Cliente] = {}
_contador_clientes: int = 0

# funciones de
def obtener_siguiente_id_usuario() -> int:
    global _contador_usuarios
    _contador_usuarios += 1
    return _contador_usuarios

def obtener_siguiente_id_incidencia() -> int:
    global _contador_incidencias
    _contador_incidencias += 1
    return _contador_incidencias

def obtener_siguiente_id_cliente() -> int:
    global _contador_clientes
    _contador_clientes += 1
    return _contador_clientes

def reiniciar_datos():
    global usuarios_registrados, usuarios_por_email, _contador_usuarios
    global incidencias_registradas, incidencias_por_id, _contador_incidencias
    global clientes_registrados, clientes_por_email, _contador_clientes
    
    usuarios_registrados = []
    usuarios_por_email = {}
    _contador_usuarios = 0
    
    incidencias_registradas = []
    incidencias_por_id = {}
    _contador_incidencias = 0
    
    clientes_registrados = []
    clientes_por_email = {}
    _contador_clientes = 0