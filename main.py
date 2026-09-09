from funciones import (
    # Funciones de lógica
    listar_usuarios,
    listar_clientes,
    actualizar_usuario,
    eliminar_usuario,
    contar_usuarios,
    contar_clientes,
    registrar_incidencia,
    listar_incidencias,
    listar_incidencias_por_usuario,
    buscar_incidencia_por_id,
    actualizar_estado_incidencia,
    eliminar_incidencia,
    contar_incidencias,
    buscar_usuario_por_email,
    validar_nombre,
    
    # Funciones interactivas (con bucles)
    iniciar_sesion_interactivo_usuario,
    iniciar_sesion_interactivo_admin,
    registrar_usuario_interactivo,
    leer_y_validar_contrasena_actualizacion,
    leer_y_validar_telefono,
    leer_sector_interactivo,

)

# Importar crear_admin_si_no_existe desde datos.py
from datos import crear_admin_si_no_existe

import os
import time

usuario_autenticado = None
es_admin_autenticado = False

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(0.1)

def pausa():
    input("\nPresione Enter para continuar...")

def mostrar_encabezado(titulo: str):
    print("\n" + "=" * 60)
    print(f"  {titulo}")
    print("=" * 60)

def leer_texto(mensaje: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(mensaje).strip()
        if not obligatorio or valor:
            return valor
        print("Este campo es obligatorio.")

def leer_numero_entero(mensaje: str, min_valor: int = None, max_valor: int = None) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if min_valor is not None and valor < min_valor:
                print(f"El valor debe ser mayor o igual a {min_valor}.")
                continue
            if max_valor is not None and valor > max_valor:
                print(f"El valor debe ser menor o igual a {max_valor}.")
                continue
            return valor
        except ValueError:
            print("Debe ingresar un numero entero valido.")

def leer_opcion_menu(mensaje: str, opciones: list) -> str:
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            return opcion
        print(f" Opcion invalida. Elija entre {', '.join(opciones)}.")

#Submenús de gestión de usuarios

def submenu_registrar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("REGISTRAR NUEVO USUARIO")
    
    resultado = registrar_usuario_interactivo()
    
    if resultado['exito']:
        print(f"\n  ¡Éxito! {resultado['mensaje']}")
        print(f"  Usuario registrado: {resultado['usuario']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_actualizar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("ACTUALIZAR USUARIO")
    
    email = leer_texto("Ingrese el correo del usuario a actualizar: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n No se encontró ningún usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  Usuario actual:")
    print(f"    ID: {usuario.id}")
    print(f"    Nombre: {usuario.nombre}")
    print(f"    Email: {usuario.email}")
    print(f"    Rol: {usuario.rol}")
    print(f"    Teléfono: {usuario.telefono or 'No registrado'}")
    print(f"    Empresa: {usuario.empresa or 'No registrada'}")
    print(f"    Sector: {usuario.sector}")
    print("-" * 40)
    
    print("\n  Actualizar nombre (deje vacío para no cambiar):")
    nuevo_nombre = input("Nuevo nombre: ").strip()
    if nuevo_nombre and not validar_nombre(nuevo_nombre):
        print("\n El nombre solo debe contener letras y espacios.")
        pausa()
        return
    if not nuevo_nombre:
        nuevo_nombre = None
    
    print("\n  Actualizar contraseña (deje vacío para no cambiar):")
    nueva_contrasena = leer_y_validar_contrasena_actualizacion("Nueva contraseña: ")
    
    print("\n  Actualizar teléfono (deje vacío para no cambiar):")
    nuevo_telefono = leer_y_validar_telefono("Nuevo teléfono: ")
    if not nuevo_telefono:
        nuevo_telefono = None
    
    print("\n  Actualizar empresa (deje vacío para no cambiar):")
    nueva_empresa = input("Nueva empresa: ").strip()
    if not nueva_empresa:
        nueva_empresa = None
    
    print("\n  Actualizar sector (deje vacío para no cambiar):")
    cambiar_sector = input("¿Cambiar sector? (s/n): ").strip().lower()
    nuevo_sector = None
    if cambiar_sector == 's':
        nuevo_sector = leer_sector_interactivo()
    
    if nuevo_nombre is None and nueva_contrasena is None and nuevo_telefono is None and nueva_empresa is None and nuevo_sector is None:
        print("\n  No se realizaron cambios.")
        pausa()
        return
    
    resultado = actualizar_usuario(
        email, 
        nuevo_nombre=nuevo_nombre, 
        nueva_contrasena=nueva_contrasena,
        nuevo_telefono=nuevo_telefono,
        nueva_empresa=nueva_empresa,
        nuevo_sector=nuevo_sector
    )
    
    if resultado['exito']:
        print(f"\n  Éxito: {resultado['mensaje']}")
        print(f"  Usuario actualizado: {resultado['usuario']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_cambiar_contrasena():
    limpiar_pantalla()
    mostrar_encabezado("Cambiar contraseña")
    
    email = leer_texto("Ingrese su correo electrónico: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n No se encontró ningún usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  Usuario: {usuario.nombre}")
    
    nueva_contrasena = leer_y_validar_contrasena_actualizacion("Ingrese su nueva contraseña: ")
    if nueva_contrasena is None:
        print("\n No se realizaron cambios.")
        pausa()
        return
    
    resultado = actualizar_usuario(email, nueva_contrasena=nueva_contrasena)
    
    if resultado['exito']:
        print(f"\n Contraseña actualizada exitosamente.")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_buscar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("Buscar usuario")
    
    email = leer_texto("Ingrese el correo del usuario a buscar: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n No se encontró ningún usuario con ese correo.")
    else:
        print(f"\n  Usuario encontrado:")
        print(f"    ID: {usuario.id}")
        print(f"    Nombre: {usuario.nombre}")
        print(f"    Email: {usuario.email}")
        print(f"    Rol: {usuario.rol}")
        print(f"    Teléfono: {usuario.telefono or 'No registrado'}")
        print(f"    Empresa: {usuario.empresa or 'No registrada'}")
        print(f"    Sector: {usuario.sector}")
        
        # Mostrar incidencias del usuario
        incidencias = listar_incidencias_por_usuario(usuario.id)
        if incidencias:
            print(f"\n  Incidencias reportadas: {len(incidencias)}")
            for i in incidencias:
                print(f"    ID: {i.id} | {i.titulo} | Estado: {i.estado} | Prioridad: {i.prioridad}")
        else:
            print("\n  No ha reportado incidencias.")
    
    pausa()

def submenu_listar_usuarios():
    limpiar_pantalla()
    mostrar_encabezado("Lista de usuarios")
    
    usuarios = listar_usuarios()
    
    if len(usuarios) == 0:
        print("\n  No hay usuarios registrados.")
    else:
        print(f"\n  Total de usuarios: {len(usuarios)}")
        print("-" * 60)
        for u in usuarios:
            print(f"  ID: {u.id} | Nombre: {u.nombre} | Email: {u.email} | Rol: {u.rol}")
    
    pausa()

def submenu_listar_clientes():
    limpiar_pantalla()
    mostrar_encabezado("Lista de clientes")
    
    clientes = listar_clientes()
    
    if len(clientes) == 0:
        print("\n  No hay clientes registrados.")
    else:
        print(f"\n  Total de clientes: {len(clientes)}")
        print("-" * 60)
        for c in clientes:
            print(f"  ID: {c.id} | {c.nombre} | {c.email} | {c.empresa} | {c.sector}")
    
    pausa()

def submenu_eliminar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("Eliminar usuario")
    
    email = leer_texto("Ingrese el correo del usuario a eliminar: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n  Error: No se encontró ningún usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  ADVERTENCIA: Está a punto de eliminar al usuario:")
    print(f"    ID: {usuario.id}")
    print(f"    Nombre: {usuario.nombre}")
    print(f"    Email: {usuario.email}")
    print(f"    Rol: {usuario.rol}")
    
    confirmar = leer_texto("  Confirmar eliminación (s/n): ")
    if confirmar.lower() != 's':
        print("\n  Operación cancelada.")
        pausa()
        return
    
    resultado = eliminar_usuario(email)
    
    if resultado['exito']:
        print(f"\n  Éxito: {resultado['mensaje']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_contar_usuarios():
    limpiar_pantalla()
    mostrar_encabezado("Total de usuarios")
    
    total = contar_usuarios()
    total_clientes = contar_clientes()
    print(f"\n  Total de usuarios registrados: {total}")
    print(f"  Total de clientes: {total_clientes}")
    
    pausa()

def submenu_gestionar_usuarios():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("Gestión de usuarios")
        print("  1. Registrar nuevo usuario")
        print("  2. Buscar usuario")
        print("  3. Listar todos los usuarios")
        print("  4. Listar solo clientes")
        print("  5. Actualizar usuario")
        print("  6. Eliminar usuario")
        print("  7. Contar usuarios")
        print("  8. Cambiar contraseña")
        print("  9. Volver al menú principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        
        if opcion == '1':
            submenu_registrar_usuario()
        elif opcion == '2':
            submenu_buscar_usuario()
        elif opcion == '3':
            submenu_listar_usuarios()
        elif opcion == '4':
            submenu_listar_clientes()
        elif opcion == '5':
            submenu_actualizar_usuario()
        elif opcion == '6':
            submenu_eliminar_usuario()
        elif opcion == '7':
            submenu_contar_usuarios()
        elif opcion == '8':
            submenu_cambiar_contrasena()
        elif opcion == '9':
            return

#submenús de gestión de incidencias

def submenu_registrar_incidencia():
    limpiar_pantalla()
    mostrar_encabezado("Registrar incidencia")
    
    titulo = leer_texto("Título: ")
    descripcion = leer_texto("Descripción: ")
    
    print("\n  Seleccione la prioridad:")
    print("    1. Baja")
    print("    2. Media")
    print("    3. Alta")
    print("    4. Crítica")
    print("-" * 40)
    
    opcion_prioridad = leer_opcion_menu("Elija una opción (Enter para 'media'): ", ['1', '2', '3', '4', ''])
    
    if opcion_prioridad == '':
        prioridad = "media"
    elif opcion_prioridad == '1':
        prioridad = "baja"
    elif opcion_prioridad == '2':
        prioridad = "media"
    elif opcion_prioridad == '3':
        prioridad = "alta"
    elif opcion_prioridad == '4':
        prioridad = "critica"
    
    resultado = registrar_incidencia(
        usuario_autenticado.id,
        titulo,
        descripcion,
        prioridad
    )
    
    if resultado['exito']:
        print(f"\n  Éxito: {resultado['mensaje']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    pausa()

def submenu_gestionar_incidencias():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("Gestionar incidencias")
        print("  1. Registrar nueva incidencia")
        print("  2. Listar todas las incidencias")
        print("  3. Buscar incidencia por ID")
        print("  4. Cambiar estado de incidencia")
        print("  5. Eliminar incidencia")
        print("  6. Contar incidencias")
        print("  7. Volver al menú principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6', '7'])
        
        if opcion == '1':
            submenu_registrar_incidencia()
        elif opcion == '2':
            limpiar_pantalla()
            mostrar_encabezado("Todas las incidencias")
            
            incidencias = listar_incidencias()
            
            if len(incidencias) == 0:
                print("\n  No hay incidencias registradas.")
            else:
                print(f"\n  Total de incidencias: {len(incidencias)}")
                print("-" * 60)
                for i in incidencias:
                    print(f"  ID: {i.id} | {i.titulo} | Estado: {i.estado} | Prioridad: {i.prioridad}")
                    print(f"    Usuario ID: {i.usuario_id}")
                    print("-" * 40)
            pausa()
            
        elif opcion == '3':
            limpiar_pantalla()
            mostrar_encabezado("Buscar incidencia")
            
            id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
            incidencia = buscar_incidencia_por_id(id_incidencia)
            
            if incidencia is None:
                print("\n  Incidencia no encontrada.")
            else:
                print(f"\n  ID: {incidencia.id}")
                print(f"  Título: {incidencia.titulo}")
                print(f"  Descripción: {incidencia.descripcion}")
                print(f"  Estado: {incidencia.estado}")
                print(f"  Prioridad: {incidencia.prioridad}")
                print(f"  Usuario ID: {incidencia.usuario_id}")
                print(f"  Fecha: {incidencia.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
            pausa()
            
        elif opcion == '4':
            limpiar_pantalla()
            mostrar_encabezado("Cambiar estado de incidencia")
            
            id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
            
            incidencia = buscar_incidencia_por_id(id_incidencia)
            
            if incidencia is None:
                print("\n  Incidencia no encontrada.")
                pausa()
                continue
            
            print(f"\n  Incidencia seleccionada: {incidencia.titulo}")
            print(f"  Estado actual: {incidencia.estado}")
            print("-" * 40)
            
            print("  Seleccione el nuevo estado:")
            print("    1. Pendiente")
            print("    2. En proceso")
            print("    3. Resuelto")
            print("    4. Cerrado")
            print("-" * 40)
            
            opcion_estado = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4'])
            
            if opcion_estado == '1':
                nuevo_estado = "pendiente"
            elif opcion_estado == '2':
                nuevo_estado = "en_proceso"
            elif opcion_estado == '3':
                nuevo_estado = "resuelto"
            elif opcion_estado == '4':
                nuevo_estado = "cerrado"
            
            resultado = actualizar_estado_incidencia(id_incidencia, nuevo_estado)
            
            if resultado['exito']:
                print(f"\n  Éxito: {resultado['mensaje']}")
            else:
                print(f"\n  Error: {resultado['mensaje']}")
            pausa()
            
        elif opcion == '5':
            limpiar_pantalla()
            mostrar_encabezado("ELiminar incidencia")
            
            id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
            
            confirmar = leer_texto("Confirmar eliminación (s/n): ")
            if confirmar.lower() == 's':
                resultado = eliminar_incidencia(id_incidencia)
                if resultado['exito']:
                    print(f"\n  Éxito: {resultado['mensaje']}")
                else:
                    print(f"\n  Error: {resultado['mensaje']}")
            else:
                print("\n  Operación cancelada.")
            pausa()
            
        elif opcion == '6':
            limpiar_pantalla()
            mostrar_encabezado("Total de incidencias")
            
            total = contar_incidencias()
            print(f"\n  Total de incidencias registradas: {total}")
            pausa()
            
        elif opcion == '7':
            return

#Submenús de cliente (usuario autenticado)

def submenu_cliente_mis_incidencias():
    limpiar_pantalla()
    mostrar_encabezado("Mis incidencias")
    
    incidencias = listar_incidencias_por_usuario(usuario_autenticado.id)
    
    if len(incidencias) == 0:
        print("\n  No has reportado ninguna incidencia.")
    else:
        print(f"\n  Total de tus incidencias: {len(incidencias)}")
        print("-" * 60)
        for i in incidencias:
            print(f"  ID: {i.id} | {i.titulo} | Estado: {i.estado} | Prioridad: {i.prioridad}")
            print(f"    Fecha: {i.fecha_creacion.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 40)
    pausa()

def submenu_cliente_ver_incidencia():
    limpiar_pantalla()
    mostrar_encabezado("Ver detalle de incidencia")
    
    id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
    incidencia = buscar_incidencia_por_id(id_incidencia)
    
    if incidencia is None:
        print("\n  Incidencia no encontrada.")
    elif incidencia.usuario_id != usuario_autenticado.id:
        print("\n  Error: Esta incidencia no te pertenece.")
    else:
        print(f"\n  ID: {incidencia.id}")
        print(f"  Título: {incidencia.titulo}")
        print(f"  Descripción: {incidencia.descripcion}")
        print(f"  Estado: {incidencia.estado}")
        print(f"  Prioridad: {incidencia.prioridad}")
        print(f"  Fecha de creación: {incidencia.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
    pausa()

def submenu_ver_perfil():
    limpiar_pantalla()
    mostrar_encabezado("Mi Perfil")
    
    u = usuario_autenticado
    print(f"  ID: {u.id}")
    print(f"  Nombre: {u.nombre}")
    print(f"  Email: {u.email}")
    print(f"  Rol: {u.rol.upper()}")
    print(f"  Teléfono: {u.telefono or 'No registrado'}")
    print(f"  Empresa: {u.empresa or 'No registrada'}")
    print(f"  Sector: {u.sector}")
    
    pausa()

def submenu_actualizar_mi_perfil():
    global usuario_autenticado
    
    limpiar_pantalla()
    mostrar_encabezado("Actualizar mi perfil")
    
    u = usuario_autenticado
    print(f"  Usuario: {u.nombre}")
    print("-" * 40)
    
    print("\n  Actualizar nombre (deje vacío para no cambiar):")
    nuevo_nombre = input("Nuevo nombre: ").strip()
    if nuevo_nombre and not validar_nombre(nuevo_nombre):
        print("\n El nombre solo debe contener letras y espacios.")
        pausa()
        return
    if not nuevo_nombre:
        nuevo_nombre = None
    
    print("\n  Actualizar contraseña (deje vacío para no cambiar):")
    nueva_contrasena = leer_y_validar_contrasena_actualizacion("Nueva contraseña: ")
    
    print("\n  Actualizar teléfono (deje vacío para no cambiar):")
    nuevo_telefono = leer_y_validar_telefono("Nuevo teléfono: ")
    if not nuevo_telefono:
        nuevo_telefono = None
    
    print("\n  Actualizar empresa (deje vacío para no cambiar):")
    nueva_empresa = input("Nueva empresa: ").strip()
    if not nueva_empresa:
        nueva_empresa = None
    
    print("\n  Actualizar sector (deje vacío para no cambiar):")
    cambiar_sector = input("¿Cambiar sector? (s/n): ").strip().lower()
    nuevo_sector = None
    if cambiar_sector == 's':
        nuevo_sector = leer_sector_interactivo()
    
    if nuevo_nombre is None and nueva_contrasena is None and nuevo_telefono is None and nueva_empresa is None and nuevo_sector is None:
        print("\n  No se realizaron cambios.")
        pausa()
        return
    
    resultado = actualizar_usuario(
        usuario_autenticado.email,
        nuevo_nombre=nuevo_nombre,
        nueva_contrasena=nueva_contrasena,
        nuevo_telefono=nuevo_telefono,
        nueva_empresa=nueva_empresa,
        nuevo_sector=nuevo_sector
    )
    
    if resultado['exito']:
        usuario_autenticado = resultado['usuario']
        print(f"\n  Éxito: {resultado['mensaje']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

#menus principal

def menu_iniciar_sesion() -> bool:
    global usuario_autenticado, es_admin_autenticado
    
    while True:
        limpiar_pantalla()
        mostrar_encabezado("Iniciar sesión")
        
        print("  1. Iniciar sesión como usuario")
        print("  2. Acceso de administrador (contraseña especial)")
        print("  3. Volver")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3'])
        
        if opcion == '3':
            return False
        
        if opcion == '1':
            limpiar_pantalla()
            resultado = iniciar_sesion_interactivo_usuario()
            if resultado['exito']:
                usuario_autenticado = resultado['usuario']
                es_admin_autenticado = resultado['es_admin']
                print(f"\n  Éxito: {resultado['mensaje']}")
                print(f"  Bienvenido, {usuario_autenticado.nombre}!")
                pausa()
                return True
        
        elif opcion == '2':
            limpiar_pantalla()
            resultado = iniciar_sesion_interactivo_admin()
            if resultado['exito']:
                usuario_autenticado = resultado['usuario']
                es_admin_autenticado = True
                print(f"\n  Éxito: {resultado['mensaje']}")
                print(f"  Bienvenido, {usuario_autenticado.nombre}!")
                pausa()
                return True

def menu_principal_autenticado():
    global usuario_autenticado, es_admin_autenticado
    
    while True:
        limpiar_pantalla()
        mostrar_encabezado("Solucuiones 2T - Menú principal")
        print(f"  Usuario: {usuario_autenticado.nombre}")
        print(f"  Rol: {'ADMINISTRADOR' if es_admin_autenticado else 'CLIENTE'}")
        print("-" * 60)
        
        if es_admin_autenticado:
            print("  1. Gestionar usuarios")
            print("  2. Gestionar incidencias (ver todas, cambiar estado, eliminar)")
            print("  3. Ver mi perfil")
            print("  4. Actualizar mi perfil")
            print("  5. Cerrar sesión")
            print("  6. Salir del sistema")
        else:
            print("  1. Reportar nueva incidencia")
            print("  2. Ver mis incidencias")
            print("  3. Ver detalle de una incidencia")
            print("  4. Ver mi perfil")
            print("  5. Actualizar mi perfil")
            print("  6. Cerrar sesión")
            print("  7. Salir del sistema")
        
        print("-" * 60)
        
        if es_admin_autenticado:
            opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6'])
            
            if opcion == '1':
                submenu_gestionar_usuarios()
            elif opcion == '2':
                submenu_gestionar_incidencias()
            elif opcion == '3':
                submenu_ver_perfil()
            elif opcion == '4':
                submenu_actualizar_mi_perfil()
            elif opcion == '5':
                usuario_autenticado = None
                es_admin_autenticado = False
                print("\n  Sesión cerrada exitosamente.")
                pausa()
                return
            elif opcion == '6':
                print("\n  Gracias por usar Soluciones 2T.")
                pausa()
                exit(0)
        else:
            opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6', '7'])
            
            if opcion == '1':
                submenu_registrar_incidencia()
            elif opcion == '2':
                submenu_cliente_mis_incidencias()
            elif opcion == '3':
                submenu_cliente_ver_incidencia()
            elif opcion == '4':
                submenu_ver_perfil()
            elif opcion == '5':
                submenu_actualizar_mi_perfil()
            elif opcion == '6':
                usuario_autenticado = None
                es_admin_autenticado = False
                print("\n  Sesión cerrada exitosamente.")
                pausa()
                return
            elif opcion == '7':
                print("\n  Gracias por usar Soluciones 2T.")
                pausa()
                exit(0)

def menu_principal_no_autenticado():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("Soluciones 2T - Sistema de gestión de incidencias")
        print("  El poder de la tecnología al alcance de todos.")
        print("-" * 60)
        print("  1. Iniciar sesión")
        print("  2. Registrarse")
        print("  3. Salir")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3'])
        
        if opcion == '1':
            if menu_iniciar_sesion():
                menu_principal_autenticado()
        elif opcion == '2':
            submenu_registrar_usuario()
        elif opcion == '3':
            print("\n  Gracias por usar Soluciones 2T.")
            pausa()
            exit(0)

def main():
    try:

        crear_admin_si_no_existe()
        menu_principal_no_autenticado()
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario.")
        print("  Gracias por usar Soluciones 2T.")
    except Exception as e:
        print(f"\n  Error inesperado: {e}")
        print("  El sistema se cerrará.")

if __name__ == "__main__":
    main()