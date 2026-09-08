# Importar las entidades para crear objetos
from entidades import Usuario, Incidencia, Cliente

# Importamos las colecciones y funciones desde datos.py
from datos import (
    usuarios_registrados, 
    usuarios_por_email, 
    obtener_siguiente_id_usuario,
    incidencias_registradas, 
    incidencias_por_id, 
    obtener_siguiente_id_incidencia,
    clientes_registrados, 
    clientes_por_email, 
    obtener_siguiente_id_cliente
)

#Sirve para buscar, coincidir y validar patrones de texto de forma avanzada
import re

#Se usa datetime para trabajar con fechas y horas
from datetime import datetime

#VALIDACIONES

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

def registrar_usuario(nombre: str, email: str, contrasena: str, confirmar_contrasena: str) -> dict:
    if contrasena != confirmar_contrasena:
        return {
            'exito': False,
            'mensaje': 'Las contrasenas no coinciden.',
            'usuario': None
        }
    
    if not validar_nombre(nombre):
        return {
            'exito': False,
            'mensaje': 'El nombre solo debe contener letras y espacios.',
            'usuario': None
        }
    
    if not validar_email(email):
        return {
            'exito': False,
            'mensaje': 'El formato del correo electronico no es valido.',
            'usuario': None
        }
    
    email_normalizado = email.lower().strip()
    if email_normalizado in usuarios_por_email:
        return {
            'exito': False,
            'mensaje': 'El correo electronico ya esta registrado.',
            'usuario': None
        }
    
    if not validar_contrasena(contrasena):
        return {
            'exito': False,
            'mensaje': 'La contrasena debe tener al menos 6 caracteres, una mayuscula y un numero.',
            'usuario': None
        }
    
    nuevo_id = obtener_siguiente_id_usuario()
    usuario = Usuario(
        id=nuevo_id,
        nombre=nombre.strip(),
        email=email_normalizado,
        contrasena=contrasena
    )
    
    usuarios_registrados.append(usuario)
    usuarios_por_email[usuario.email] = usuario
    
    return {
        'exito': True,
        'mensaje': 'Usuario registrado exitosamente.',
        'usuario': usuario
    }

def buscar_usuario_por_email(email: str) -> Usuario | None:
    return usuarios_por_email.get(email.lower().strip())

def buscar_usuario_por_id(id: int) -> Usuario | None:
    for usuario in usuarios_registrados:
        if usuario.id == id:
            return usuario
    return None

def listar_usuarios() -> list[Usuario]:
    return usuarios_registrados.copy()

def actualizar_usuario(email: str, nuevo_nombre: str = None, nueva_contrasena: str = None) -> dict:
    email_normalizado = email.lower().strip()
    usuario = usuarios_por_email.get(email_normalizado)
    
    if usuario is None:
        return {
            'exito': False,
            'mensaje': 'Usuario no encontrado.',
            'usuario': None
        }
    
    if nuevo_nombre is not None:
        if not validar_nombre(nuevo_nombre):
            return {
                'exito': False,
                'mensaje': 'El nombre solo debe contener letras y espacios.',
                'usuario': None
            }
        usuario.nombre = nuevo_nombre.strip()
    
    if nueva_contrasena is not None:
        if not validar_contrasena(nueva_contrasena):
            return {
                'exito': False,
                'mensaje': 'La contrasena debe tener al menos 6 caracteres, una mayuscula y un numero.',
                'usuario': None
            }
        usuario.contrasena = nueva_contrasena
    
    return {
        'exito': True,
        'mensaje': 'Usuario actualizado exitosamente.',
        'usuario': usuario
    }

def eliminar_usuario(email: str) -> dict:
    email_normalizado = email.lower().strip()
    usuario = usuarios_por_email.get(email_normalizado)
    
    if usuario is None:
        return {
            'exito': False,
            'mensaje': 'Usuario no encontrado.'
        }
    
    del usuarios_por_email[email_normalizado]
    usuarios_registrados[:] = [u for u in usuarios_registrados if u.email != email_normalizado]
    
    return {
        'exito': True,
        'mensaje': 'Usuario eliminado exitosamente.'
    }

def contar_usuarios() -> int:
    return len(usuarios_registrados)

def iniciar_sesion(email: str, contrasena: str) -> dict:
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        return {
            'exito': False,
            'mensaje': 'Usuario no encontrado.',
            'usuario': None
        }
    
    if usuario.contrasena != contrasena:
        return {
            'exito': False,
            'mensaje': 'Contrasena incorrecta.',
            'usuario': None
        }
    
    return {
        'exito': True,
        'mensaje': 'Inicio de sesion exitoso.',
        'usuario': usuario
    }

def reportar_problema(usuario: Usuario, problema: str) -> dict:
    if not problema or len(problema.strip()) == 0:
        return {
            'exito': False,
            'mensaje': 'El problema no puede estar vacio.'
        }
    
    print("\n" + "=" * 60)
    print("  REPORTE DE PROBLEMA")
    print("=" * 60)
    print(f"  Usuario: {usuario.nombre} ({usuario.email})")
    print(f"  Problema: {problema}")
    print(f"  Estado: Pendiente de revision")
    print("=" * 60)
    
    return {
        'exito': True,
        'mensaje': 'Problema reportado exitosamente.'
    }

def registrar_incidencia(usuario_id: int, titulo: str, descripcion: str, prioridad: str = "media") -> dict:
    if not titulo or len(titulo.strip()) == 0:
        return {
            'exito': False,
            'mensaje': 'El titulo no puede estar vacio.',
            'incidencia': None
        }
    
    if not descripcion or len(descripcion.strip()) == 0:
        return {
            'exito': False,
            'mensaje': 'La descripcion no puede estar vacia.',
            'incidencia': None
        }
    
    prioridades_validas = ['baja', 'media', 'alta', 'critica']
    if prioridad not in prioridades_validas:
        return {
            'exito': False,
            'mensaje': 'Prioridad invalida. Use: baja, media, alta, critica.',
            'incidencia': None
        }
    
    nuevo_id = obtener_siguiente_id_incidencia()
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
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
    
    return {
        'exito': True,
        'mensaje': 'Incidencia registrada exitosamente.',
        'incidencia': incidencia
    }

def listar_incidencias() -> list:
    return incidencias_registradas.copy()

def buscar_incidencia_por_id(id: int):
    return incidencias_por_id.get(id)

def actualizar_estado_incidencia(id: int, nuevo_estado: str) -> dict:
    estados_validos = ['pendiente', 'en_proceso', 'resuelto', 'cerrado']
    if nuevo_estado not in estados_validos:
        return {
            'exito': False,
            'mensaje': 'Estado invalido. Use: pendiente, en_proceso, resuelto, cerrado.'
        }
    
    incidencia = incidencias_por_id.get(id)
    
    if incidencia is None:
        return {
            'exito': False,
            'mensaje': 'Incidencia no encontrada.'
        }
    
    incidencia.estado = nuevo_estado
    
    return {
        'exito': True,
        'mensaje': f'Estado actualizado a "{nuevo_estado}" exitosamente.',
        'incidencia': incidencia
    }

def eliminar_incidencia(id: int) -> dict:
    incidencia = incidencias_por_id.get(id)
    
    if incidencia is None:
        return {
            'exito': False,
            'mensaje': 'Incidencia no encontrada.'
        }
    
    del incidencias_por_id[id]
    incidencias_registradas[:] = [i for i in incidencias_registradas if i.id != id]
    
    return {
        'exito': True,
        'mensaje': 'Incidencia eliminada exitosamente.'
    }

def contar_incidencias() -> int:
    return len(incidencias_registradas)

def registrar_cliente(nombre: str, email: str, telefono: str, empresa: str, sector: str) -> dict:
    if not validar_nombre(nombre):
        return {
            'exito': False,
            'mensaje': 'Nombre invalido.',
            'cliente': None
        }
    
    if not validar_email(email):
        return {
            'exito': False,
            'mensaje': 'Email invalido.',
            'cliente': None
        }
    
    email_normalizado = email.lower().strip()
    if email_normalizado in clientes_por_email:
        return {
            'exito': False,
            'mensaje': 'Email ya registrado.',
            'cliente': None
        }
    
    sectores_validos = ['publico', 'privado', 'educativo', 'otro']
    if sector not in sectores_validos:
        return {
            'exito': False,
            'mensaje': 'Sector invalido. Use: publico, privado, educativo, otro.',
            'cliente': None
        }
    
    nuevo_id = obtener_siguiente_id_cliente()
    
    cliente = Cliente(
        id=nuevo_id,
        nombre=nombre.strip(),
        email=email_normalizado,
        telefono=telefono.strip() if telefono else "",
        empresa=empresa.strip() if empresa else "",
        sector=sector
    )
    
    clientes_registrados.append(cliente)
    clientes_por_email[cliente.email] = cliente
    
    return {
        'exito': True,
        'mensaje': 'Cliente registrado exitosamente.',
        'cliente': cliente
    }

def listar_clientes() -> list:
    return clientes_registrados.copy()

def buscar_cliente_por_email(email: str):
    return clientes_por_email.get(email.lower().strip())

def actualizar_cliente(email: str, nuevo_nombre: str = None, nuevo_telefono: str = None, nueva_empresa: str = None) -> dict:
    email_normalizado = email.lower().strip()
    cliente = clientes_por_email.get(email_normalizado)
    
    if cliente is None:
        return {
            'exito': False,
            'mensaje': 'Cliente no encontrado.',
            'cliente': None
        }
    
    if nuevo_nombre is not None:
        if not validar_nombre(nuevo_nombre):
            return {
                'exito': False,
                'mensaje': 'Nombre invalido.',
                'cliente': None
            }
        cliente.nombre = nuevo_nombre.strip()
    
    if nuevo_telefono is not None:
        cliente.telefono = nuevo_telefono.strip()
    
    if nueva_empresa is not None:
        cliente.empresa = nueva_empresa.strip()
    
    return {
        'exito': True,
        'mensaje': 'Cliente actualizado exitosamente.',
        'cliente': cliente
    }

def eliminar_cliente(email: str) -> dict:
    email_normalizado = email.lower().strip()
    cliente = clientes_por_email.get(email_normalizado)
    
    if cliente is None:
        return {
            'exito': False,
            'mensaje': 'Cliente no encontrado.'
        }
    
    del clientes_por_email[email_normalizado]
    clientes_registrados[:] = [c for c in clientes_registrados if c.email != email_normalizado]
    
    return {
        'exito': True,
        'mensaje': 'Cliente eliminado exitosamente.'
    }

def contar_clientes() -> int:
    return len(clientes_registrados)