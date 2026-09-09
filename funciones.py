# Importar las entidades para crear objetos
from entidades import Usuario, Incidencia

# Importamos las colecciones y funciones desde datos.py
from datos import (
    usuarios_registrados,
    usuarios_por_email,
    obtener_siguiente_id_usuario,
    incidencias_registradas,
    incidencias_por_id,
    obtener_siguiente_id_incidencia,
    ADMIN_EMAIL,
    ADMIN_PASSWORD
)

# Sirve para buscar, coincidir y validar patrones de texto de forma avanzada
import re

# Se usa datetime para trabajar con fechas y horas
from datetime import datetime


# Validaciones

def validar_email(email: str) -> bool:
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_contrasena(contrasena: str) -> bool:
    if len(contrasena) < 6:
        return False
    if not re.search(r'[A-Z]', contrasena):
        return False
    if not re.search(r'[0-9]', contrasena):
        return False
    return True

def validar_nombre(nombre: str) -> bool:
    if not nombre or len(nombre.strip()) == 0:
        return False
    patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
    return re.match(patron, nombre) is not None

def validar_telefono(telefono: str) -> bool:
    if not telefono:
        return True
    patron = r'^[0-9+\-\s]{8,15}$'
    return re.match(patron, telefono) is not None

# LÓGICA DE NEGOCIO - USUARIOS

def registrar_usuario(nombre: str, email: str, contrasena: str, confirmar_contrasena: str,
                      telefono: str = "", empresa: str = "", sector: str = "otros") -> dict:
    if contrasena != confirmar_contrasena:
        return {'exito': False, 'mensaje': 'Las contrasenas no coinciden.', 'usuario': None}
    
    if not validar_nombre(nombre):
        return {'exito': False, 'mensaje': 'El nombre solo debe contener letras y espacios.', 'usuario': None}
    
    if not validar_email(email):
        return {'exito': False, 'mensaje': 'El formato del correo electronico no es valido.', 'usuario': None}
    
    email_normalizado = email.lower().strip()
    if email_normalizado in usuarios_por_email:
        return {'exito': False, 'mensaje': 'El correo electronico ya esta registrado.', 'usuario': None}
    
    if not validar_contrasena(contrasena):
        return {'exito': False, 'mensaje': 'La contrasena debe tener al menos 6 caracteres, una mayuscula y un numero.', 'usuario': None}
    
    if telefono and not validar_telefono(telefono):
        return {'exito': False, 'mensaje': 'El telefono debe tener entre 8 y 15 digitos.', 'usuario': None}
    
    sectores_validos = ['publico', 'privado', 'educativo', 'otros']
    if sector not in sectores_validos:
        return {'exito': False, 'mensaje': 'Sector invalido. Use: publico, privado, educativo, otros.', 'usuario': None}
    
    nuevo_id = obtener_siguiente_id_usuario()
    usuario = Usuario(
        id=nuevo_id,
        nombre=nombre.strip(),
        email=email_normalizado,
        contrasena=contrasena,
        rol="cliente",
        telefono=telefono.strip(),
        empresa=empresa.strip() if empresa else "Soluciones 2T",
        sector=sector
    )
    
    usuarios_registrados.append(usuario)
    usuarios_por_email[usuario.email] = usuario
    
    return {'exito': True, 'mensaje': 'Usuario registrado exitosamente.', 'usuario': usuario}

def buscar_usuario_por_email(email: str) -> Usuario | None:
    return usuarios_por_email.get(email.lower().strip())

def buscar_usuario_por_id(id: int) -> Usuario | None:
    for usuario in usuarios_registrados:
        if usuario.id == id:
            return usuario
    return None

def listar_usuarios() -> list[Usuario]:
    return usuarios_registrados.copy()

def listar_clientes() -> list[Usuario]:
    """Retorna solo los usuarios con rol 'cliente'"""
    return [u for u in usuarios_registrados if u.rol == "cliente"]

def actualizar_usuario(email: str, nuevo_nombre: str = None, nueva_contrasena: str = None,
                       nuevo_telefono: str = None, nueva_empresa: str = None,
                       nuevo_sector: str = None) -> dict:
    email_normalizado = email.lower().strip()
    usuario = usuarios_por_email.get(email_normalizado)
    
    if usuario is None:
        return {'exito': False, 'mensaje': 'Usuario no encontrado.', 'usuario': None}
    
    if usuario.email == ADMIN_EMAIL and usuario.rol == "admin":
        return {'exito': False, 'mensaje': 'No se puede modificar al administrador.', 'usuario': None}
    
    if nuevo_nombre is not None:
        if not validar_nombre(nuevo_nombre):
            return {'exito': False, 'mensaje': 'El nombre solo debe contener letras y espacios.', 'usuario': None}
        usuario.nombre = nuevo_nombre.strip()
    
    if nueva_contrasena is not None:
        if not validar_contrasena(nueva_contrasena):
            return {'exito': False, 'mensaje': 'La contrasena debe tener al menos 6 caracteres, una mayuscula y un numero.', 'usuario': None}
        usuario.contrasena = nueva_contrasena
    
    if nuevo_telefono is not None:
        if nuevo_telefono and not validar_telefono(nuevo_telefono):
            return {'exito': False, 'mensaje': 'El telefono debe tener entre 8 y 15 digitos.', 'usuario': None}
        usuario.telefono = nuevo_telefono.strip()
    
    if nueva_empresa is not None:
        usuario.empresa = nueva_empresa.strip() if nueva_empresa else "Soluciones 2T"
    
    if nuevo_sector is not None:
        sectores_validos = ['publico', 'privado', 'educativo', 'otros']
        if nuevo_sector not in sectores_validos:
            return {'exito': False, 'mensaje': 'Sector invalido. Use: publico, privado, educativo, otros.', 'usuario': None}
        usuario.sector = nuevo_sector
    
    return {'exito': True, 'mensaje': 'Usuario actualizado exitosamente.', 'usuario': usuario}

def eliminar_usuario(email: str) -> dict:
    email_normalizado = email.lower().strip()
    usuario = usuarios_por_email.get(email_normalizado)
    
    if usuario is None:
        return {'exito': False, 'mensaje': 'Usuario no encontrado.'}
    
    if usuario.email == ADMIN_EMAIL:
        return {'exito': False, 'mensaje': 'No se puede eliminar al administrador.'}
    
    del usuarios_por_email[email_normalizado]
    usuarios_registrados[:] = [u for u in usuarios_registrados if u.email != email_normalizado]
    
    return {'exito': True, 'mensaje': 'Usuario eliminado exitosamente.'}

def contar_usuarios() -> int:
    return len(usuarios_registrados)

def contar_clientes() -> int:
    return len([u for u in usuarios_registrados if u.rol == "cliente"])

def iniciar_sesion(email: str, contrasena: str) -> dict:
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        return {'exito': False, 'mensaje': 'Usuario no encontrado.', 'usuario': None, 'es_admin': False}
    
    if usuario.contrasena != contrasena:
        return {'exito': False, 'mensaje': 'Contrasena incorrecta.', 'usuario': None, 'es_admin': False}
    
    es_admin = usuario.email == ADMIN_EMAIL
    
    return {'exito': True, 'mensaje': 'Inicio de sesion exitoso.', 'usuario': usuario, 'es_admin': es_admin}

def iniciar_sesion_admin(contrasena_admin: str) -> dict:
    if contrasena_admin == ADMIN_PASSWORD:
        admin = usuarios_por_email.get(ADMIN_EMAIL)
        if admin is None:
            admin = Usuario(
                id=obtener_siguiente_id_usuario(),
                nombre="Administrador",
                email=ADMIN_EMAIL,
                contrasena=ADMIN_PASSWORD,
                rol="admin"
            )
            usuarios_registrados.append(admin)
            usuarios_por_email[admin.email] = admin
        
        return {'exito': True, 'mensaje': 'Acceso de administrador concedido.', 'usuario': admin, 'es_admin': True}
    else:
        return {'exito': False, 'mensaje': 'Contraseña de administrador incorrecta.', 'usuario': None, 'es_admin': False}

#logica de negocio - incidencias

def registrar_incidencia(usuario_id: int, titulo: str, descripcion: str, prioridad: str = "media") -> dict:
    if not titulo or len(titulo.strip()) == 0:
        return {'exito': False, 'mensaje': 'El titulo no puede estar vacio.', 'incidencia': None}
    
    if not descripcion or len(descripcion.strip()) == 0:
        return {'exito': False, 'mensaje': 'La descripcion no puede estar vacia.', 'incidencia': None}
    
    prioridades_validas = ['baja', 'media', 'alta', 'critica']
    if prioridad not in prioridades_validas:
        return {'exito': False, 'mensaje': 'Prioridad invalida. Use: baja, media, alta, critica.', 'incidencia': None}
    
    nuevo_id = obtener_siguiente_id_incidencia()
    fecha_actual = datetime.now()
    
    incidencia = Incidencia(
        id=nuevo_id,
        usuario_id=usuario_id,
        titulo=titulo.strip(),
        descripcion=descripcion.strip(),
        estado='pendiente',
        fecha_creacion=fecha_actual,
        prioridad=prioridad
    )
    
    incidencias_registradas.append(incidencia)
    incidencias_por_id[nuevo_id] = incidencia
    
    return {'exito': True, 'mensaje': 'Incidencia registrada exitosamente.', 'incidencia': incidencia}

def listar_incidencias() -> list:
    return incidencias_registradas.copy()

def listar_incidencias_por_usuario(usuario_id: int) -> list:
    return [i for i in incidencias_registradas if i.usuario_id == usuario_id]

def buscar_incidencia_por_id(id: int):
    return incidencias_por_id.get(id)

def actualizar_estado_incidencia(id: int, nuevo_estado: str) -> dict:
    estados_validos = ['pendiente', 'en_proceso', 'resuelto', 'cerrado']
    if nuevo_estado not in estados_validos:
        return {'exito': False, 'mensaje': 'Estado invalido. Use: pendiente, en_proceso, resuelto, cerrado.'}
    
    incidencia = incidencias_por_id.get(id)
    
    if incidencia is None:
        return {'exito': False, 'mensaje': 'Incidencia no encontrada.'}
    
    incidencia.estado = nuevo_estado

    nombres_legibles = {
        'pendiente': 'Pendiente',
        'en_proceso': 'En proceso',
        'resuelto': 'Resuelto',
        'cerrado': 'Cerrado'
    }
    
    estado_mostrar = nombres_legibles.get(nuevo_estado, nuevo_estado)
    
    return {'exito': True, 'mensaje': f'Estado actualizado a "{estado_mostrar}" exitosamente.', 'incidencia': incidencia}

def eliminar_incidencia(id: int) -> dict:
    incidencia = incidencias_por_id.get(id)
    
    if incidencia is None:
        return {'exito': False, 'mensaje': 'Incidencia no encontrada.'}
    
    del incidencias_por_id[id]
    incidencias_registradas[:] = [i for i in incidencias_registradas if i.id != id]
    
    return {'exito': True, 'mensaje': 'Incidencia eliminada exitosamente.'}

def contar_incidencias() -> int:
    return len(incidencias_registradas)

#validar y leer datos de usuario de forma interactiva

def leer_y_validar_email(mensaje: str) -> str:
    while True:
        email = input(mensaje).strip()
        if validar_email(email):
            return email.lower().strip()
        print("El formato del correo no es válido. Ejemplo: usuario@dominio.com")

def leer_y_validar_nombre(mensaje: str) -> str:
    while True:
        nombre = input(mensaje).strip()
        if validar_nombre(nombre):
            return nombre.strip()
        print("El nombre solo debe contener letras y espacios.")

def leer_y_validar_contrasena(mensaje: str, confirmar: bool = True) -> str:
    while True:
        contrasena = input(mensaje).strip()
        
        if not validar_contrasena(contrasena):
            print("La contraseña debe tener mínimo 6 caracteres, una mayúscula y un número.")
            continue
        
        if not confirmar:
            return contrasena
        
        confirmacion = input("Confirme su contraseña: ").strip()
        
        if contrasena != confirmacion:
            print("Las contraseñas no coinciden.")
            continue
        
        return contrasena

def leer_y_validar_contrasena_actualizacion(mensaje: str) -> str | None:
    while True:
        contrasena = input(mensaje).strip()
        
        if contrasena == "":
            return None
        
        if not validar_contrasena(contrasena):
            print("La contraseña debe tener mínimo 6 caracteres, una mayúscula y un número.")
            continue
        
        confirmacion = input("Confirme la nueva contraseña: ").strip()
        
        if contrasena != confirmacion:
            print("Las contraseñas no coinciden.")
            continue
        
        return contrasena

def leer_y_validar_telefono(mensaje: str) -> str:
    while True:
        telefono = input(mensaje).strip()
        if not telefono or validar_telefono(telefono):
            return telefono
        print("El teléfono debe tener entre 8 y 15 dígitos.")

def leer_sector_interactivo() -> str:
    """Lee un sector del usuario con opciones"""
    print("\n  Sectores disponibles:")
    print("    1. Público")
    print("    2. Privado")
    print("    3. Educativo")
    print("    4. Otros")
    
    while True:
        opcion = input("  Elija una opción (1-4): ").strip()
        if opcion == '1':
            return 'publico'
        elif opcion == '2':
            return 'privado'
        elif opcion == '3':
            return 'educativo'
        elif opcion == '4':
            return 'otros'
        print("Opción inválida. Elija entre 1, 2, 3 o 4.")

#alias para funciones con ñ

# Para que funcione con import de validar_contraseña (con ñ)
validar_contraseña = validar_contrasena

# Para que funcione con import de leer_y_validar_contraseña_actualizacion (con ñ)
leer_y_validar_contraseña_actualizacion = leer_y_validar_contrasena_actualizacion

#bucles interactivos para iniciar sesión y registrar usuarios

def iniciar_sesion_interactivo_usuario() -> dict:
    
    print(" Iniciar sesión de usuario")
    print("-" * 60)
    
    while True:
        email = leer_y_validar_email("Ingrese su correo electrónico: ")
        contrasena = input("Ingrese su contraseña: ").strip()
        
        resultado = iniciar_sesion(email, contrasena)
        
        if resultado['exito']:
            return resultado
        else:
            print(f"\n  Error: {resultado['mensaje']}")
            print("  Intente nuevamente...\n")

def iniciar_sesion_interactivo_admin() -> dict:
   
    print("Acceso de administrador")
    print("-" * 60)
    print("  (No necesita email, solo la contraseña especial)")
    
    while True:
        contrasena_admin = input("Ingrese la contraseña de administrador: ").strip()
        
        resultado = iniciar_sesion_admin(contrasena_admin)
        
        if resultado['exito']:
            return resultado
        else:
            print(f"\n  Error: {resultado['mensaje']}")
            print("  Intente nuevamente...\n")

def registrar_usuario_interactivo() -> dict:
   
    print("  Complete los siguientes datos:")
    print("-" * 40)
    
    nombre = leer_y_validar_nombre("Nombre completo: ")
    email = leer_y_validar_email("Correo electrónico: ")
    
    while buscar_usuario_por_email(email) is not None:
        print("Este correo electrónico ya está registrado.")
        email = leer_y_validar_email("Correo electrónico: ")
    
    contrasena = leer_y_validar_contrasena("Ingrese su contraseña: ", confirmar=True)
    telefono = leer_y_validar_telefono("Teléfono (opcional): ")

    empresa = input("Empresa (Enter para 'Soluciones 2T'): ").strip()
    if not empresa:
        empresa = "Soluciones 2T"
    
    sector = leer_sector_interactivo()
    
    resultado = registrar_usuario(nombre, email, contrasena, contrasena, telefono, empresa, sector)
    return resultado