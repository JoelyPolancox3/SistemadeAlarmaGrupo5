from funciones import (
    # Funciones de lógica
    listar_usuarios,
    actualizar_usuario,
    eliminar_usuario,
    contar_usuarios,
    reportar_problema,
    registrar_incidencia,
    listar_incidencias,
    buscar_incidencia_por_id,
    actualizar_estado_incidencia,
    eliminar_incidencia,
    contar_incidencias,
    listar_clientes,
    buscar_cliente_por_email,
    actualizar_cliente,
    eliminar_cliente,
    contar_clientes,
    buscar_usuario_por_email,
    validar_nombre,
    
    # Funciones interactivas (con bucles)
    iniciar_sesion_interactivo_usuario,
    iniciar_sesion_interactivo_admin,
    registrar_usuario_interactivo,
    registrar_cliente_interactivo,
    leer_y_validar_contrasena_actualizacion,
)
import os
import time

usuario_autenticado = None
es_admin_autenticado = False

def limpiar_pantalla():
    print('\033[2J\033[H', end='')
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
        print("  Error: Este campo es obligatorio.")

def leer_numero_entero(mensaje: str, min_valor: int = None, max_valor: int = None) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if min_valor is not None and valor < min_valor:
                print(f"  Error: El valor debe ser mayor o igual a {min_valor}.")
                continue
            if max_valor is not None and valor > max_valor:
                print(f"  Error: El valor debe ser menor o igual a {max_valor}.")
                continue
            return valor
        except ValueError:
            print("  Error: Debe ingresar un numero entero valido.")

def leer_opcion_menu(mensaje: str, opciones: list) -> str:
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            return opcion
        print(f"  Error: Opcion invalida. Elija entre {', '.join(opciones)}.")

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
        print("\n  Error: No se encontró ningún usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  Usuario actual:")
    print(f"    ID: {usuario.id}")
    print(f"    Nombre: {usuario.nombre}")
    print(f"    Email: {usuario.email}")
    print("-" * 40)
    
    print("\n  Actualizar nombre (deje vacío para no cambiar):")
    nuevo_nombre = input("Nuevo nombre: ").strip()
    if nuevo_nombre:
        if not validar_nombre(nuevo_nombre):
            print("\n  Error: El nombre solo debe contener letras y espacios.")
            pausa()
            return
    else:
        nuevo_nombre = None
    
    print("\n  Actualizar contraseña (deje vacío para no cambiar):")
    nueva_contrasena = leer_y_validar_contrasena_actualizacion("Nueva contraseña: ")
    
    if nuevo_nombre is None and nueva_contrasena is None:
        print("\n  No se realizaron cambios.")
        pausa()
        return
    
    resultado = actualizar_usuario(email, nuevo_nombre, nueva_contrasena)
    
    if resultado['exito']:
        print(f"\n  Éxito: {resultado['mensaje']}")
        print(f"  Usuario actualizado: {resultado['usuario']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_cambiar_contrasena():
    limpiar_pantalla()
    mostrar_encabezado("CAMBIAR CONTRASEÑA")
    
    email = leer_texto("Ingrese su correo electrónico: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n  Error: No se encontró ningún usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  Usuario: {usuario.nombre}")
    
    nueva_contrasena = leer_y_validar_contrasena_actualizacion("Ingrese su nueva contraseña: ")
    
    resultado = actualizar_usuario(email, nueva_contrasena=nueva_contrasena)
    
    if resultado['exito']:
        print(f"\n  Éxito: Contraseña actualizada exitosamente.")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_registrar_cliente():
    limpiar_pantalla()
    mostrar_encabezado("REGISTRAR CLIENTE")
    
    resultado = registrar_cliente_interactivo()
    
    if resultado['exito']:
        print(f"\n  Éxito: {resultado['mensaje']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_buscar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("BUSCAR USUARIO")
    
    email = leer_texto("Ingrese el correo del usuario a buscar: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n  Resultado: No se encontró ningún usuario con ese correo.")
    else:
        print(f"\n  Usuario encontrado:")
        print(f"    ID: {usuario.id}")
        print(f"    Nombre: {usuario.nombre}")
        print(f"    Email: {usuario.email}")
        print(f"    Rol: {usuario.rol}")
    
    pausa()

def submenu_listar_usuarios():
    limpiar_pantalla()
    mostrar_encabezado("LISTA DE USUARIOS REGISTRADOS")
    
    usuarios = listar_usuarios()
    
    if len(usuarios) == 0:
        print("\n  No hay usuarios registrados.")
    else:
        print(f"\n  Total de usuarios: {len(usuarios)}")
        print("-" * 60)
        for u in usuarios:
            print(f"  ID: {u.id} | Nombre: {u.nombre} | Email: {u.email} | Rol: {u.rol}")
    
    pausa()

def submenu_eliminar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("ELIMINAR USUARIO")
    
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
    mostrar_encabezado("TOTAL DE USUARIOS")
    
    total = contar_usuarios()
    print(f"\n  Total de usuarios registrados: {total}")
    
    pausa()

def submenu_gestionar_usuarios():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIÓN DE USUARIOS")
        print("  1. Registrar nuevo usuario")
        print("  2. Buscar usuario")
        print("  3. Listar todos los usuarios")
        print("  4. Actualizar usuario")
        print("  5. Eliminar usuario")
        print("  6. Contar usuarios")
        print("  7. Cambiar contraseña")
        print("  8. Volver al menú principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6', '7', '8'])
        
        if opcion == '1':
            submenu_registrar_usuario()
        elif opcion == '2':
            submenu_buscar_usuario()
        elif opcion == '3':
            submenu_listar_usuarios()
        elif opcion == '4':
            submenu_actualizar_usuario()
        elif opcion == '5':
            submenu_eliminar_usuario()
        elif opcion == '6':
            submenu_contar_usuarios()
        elif opcion == '7':
            submenu_cambiar_contrasena()
        elif opcion == '8':
            return

def submenu_gestionar_incidencias():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIÓN DE INCIDENCIAS")
        print("  1. Registrar nueva incidencia")
        print("  2. Listar incidencias")
        print("  3. Buscar incidencia por ID")
        print("  4. Cambiar estado de incidencia")
        print("  5. Eliminar incidencia")
        print("  6. Contar incidencias")
        print("  7. Volver al menú principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6', '7'])
        
        if opcion == '1':
            limpiar_pantalla()
            mostrar_encabezado("REGISTRAR INCIDENCIA")
            
            titulo = leer_texto("Título: ")
            descripcion = leer_texto("Descripción: ")
            
            # Selección de prioridad con números
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
                usuario_autenticado.id if usuario_autenticado else 0,
                titulo,
                descripcion,
                prioridad
            )
            
            if resultado['exito']:
                print(f"\n  Éxito: {resultado['mensaje']}")
            else:
                print(f"\n  Error: {resultado['mensaje']}")
            pausa()
            
        elif opcion == '2':
            limpiar_pantalla()
            mostrar_encabezado("LISTA DE INCIDENCIAS")
            
            incidencias = listar_incidencias()
            
            if len(incidencias) == 0:
                print("\n  No hay incidencias registradas.")
            else:
                for i in incidencias:
                    print(f"  ID: {i.id} | {i.Titulo} | Estado: {i.Estado} | Prioridad: {i.prioridad}")
            pausa()
            
        elif opcion == '3':
            limpiar_pantalla()
            mostrar_encabezado("BUSCAR INCIDENCIA")
            
            id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
            incidencia = buscar_incidencia_por_id(id_incidencia)
            
            if incidencia is None:
                print("\n  Incidencia no encontrada.")
            else:
                print(f"\n  ID: {incidencia.id}")
                print(f"  Título: {incidencia.Titulo}")
                print(f"  Descripción: {incidencia.Descripcion}")
                print(f"  Estado: {incidencia.Estado}")
                print(f"  Prioridad: {incidencia.prioridad}")
                # Fecha sin microsegundos
                print(f"  Fecha: {incidencia.Fecha_Creacion.strftime('%Y-%m-%d %H:%M:%S')}")
            pausa()
            
        elif opcion == '4':
            limpiar_pantalla()
            mostrar_encabezado("CAMBIAR ESTADO DE INCIDENCIA")
            
            id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
            
            incidencia = buscar_incidencia_por_id(id_incidencia)
            
            if incidencia is None:
                print("\n  Incidencia no encontrada.")
                pausa()
                continue
            
            print(f"\n  Incidencia seleccionada: {incidencia.Titulo}")
            print(f"  Estado actual: {incidencia.Estado}")
            print("-" * 40)
            
            # Selección de estado con números (sin guiones bajos)
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
            mostrar_encabezado("ELIMINAR INCIDENCIA")
            
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
            mostrar_encabezado("TOTAL DE INCIDENCIAS")
            
            total = contar_incidencias()
            print(f"\n  Total de incidencias registradas: {total}")
            pausa()
            
        elif opcion == '7':
            return

def submenu_gestionar_clientes():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIÓN DE CLIENTES")
        print("  1. Registrar nuevo cliente")
        print("  2. Listar clientes")
        print("  3. Buscar cliente por email")
        print("  4. Actualizar cliente")
        print("  5. Eliminar cliente")
        print("  6. Contar clientes")
        print("  7. Volver al menú principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6', '7'])
        
        if opcion == '1':
            submenu_registrar_cliente()
            
        elif opcion == '2':
            limpiar_pantalla()
            mostrar_encabezado("LISTA DE CLIENTES")
            
            clientes = listar_clientes()
            
            if len(clientes) == 0:
                print("\n  No hay clientes registrados.")
            else:
                for c in clientes:
                    print(f"  {c.nombre} | {c.email} | {c.empresa} | {c.sector}")
            pausa()
            
        elif opcion == '3':
            limpiar_pantalla()
            mostrar_encabezado("BUSCAR CLIENTE")
            
            email = leer_texto("Email del cliente: ")
            cliente = buscar_cliente_por_email(email)
            
            if cliente is None:
                print("\n  Cliente no encontrado.")
            else:
                print(f"\n  ID: {cliente.id}")
                print(f"  Nombre: {cliente.nombre}")
                print(f"  Email: {cliente.email}")
                print(f"  Teléfono: {cliente.telefono}")
                print(f"  Empresa: {cliente.empresa}")
                print(f"  Sector: {cliente.sector}")
            pausa()
            
        elif opcion == '4':
            limpiar_pantalla()
            mostrar_encabezado("ACTUALIZAR CLIENTE")
            
            email = leer_texto("Email del cliente a actualizar: ")
            
            cliente = buscar_cliente_por_email(email)
            if cliente is None:
                print("\n  Cliente no encontrado.")
                pausa()
                continue
            
            print(f"\n  Cliente actual: {cliente.nombre}")
            
            nuevo_nombre = input("Nuevo nombre (Enter para no cambiar): ").strip()
            if nuevo_nombre and not validar_nombre(nuevo_nombre):
                print("  Error: El nombre solo debe contener letras y espacios.")
                pausa()
                continue
                
            nuevo_telefono = input("Nuevo teléfono (Enter para no cambiar): ").strip()
            nueva_empresa = input("Nueva empresa (Enter para no cambiar): ").strip()
            
            resultado = actualizar_cliente(
                email,
                nuevo_nombre if nuevo_nombre else None,
                nuevo_telefono if nuevo_telefono else None,
                nueva_empresa if nueva_empresa else None
            )
            
            if resultado['exito']:
                print(f"\n  Éxito: {resultado['mensaje']}")
            else:
                print(f"\n  Error: {resultado['mensaje']}")
            pausa()
            
        elif opcion == '5':
            limpiar_pantalla()
            mostrar_encabezado("ELIMINAR CLIENTE")
            
            email = leer_texto("Email del cliente a eliminar: ")
            
            confirmar = leer_texto("Confirmar eliminación (s/n): ")
            if confirmar.lower() == 's':
                resultado = eliminar_cliente(email)
                if resultado['exito']:
                    print(f"\n  Éxito: {resultado['mensaje']}")
                else:
                    print(f"\n  Error: {resultado['mensaje']}")
            else:
                print("\n  Operación cancelada.")
            pausa()
            
        elif opcion == '6':
            limpiar_pantalla()
            mostrar_encabezado("TOTAL DE CLIENTES")
            
            total = contar_clientes()
            print(f"\n  Total de clientes registrados: {total}")
            pausa()
            
        elif opcion == '7':
            return

def menu_iniciar_sesion() -> bool:
    global usuario_autenticado, es_admin_autenticado
    
    while True:
        limpiar_pantalla()
        mostrar_encabezado("INICIAR SESIÓN")
        
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

def submenu_ver_perfil():
    global usuario_autenticado
    
    limpiar_pantalla()
    mostrar_encabezado("MI PERFIL")
    
    print(f"  ID: {usuario_autenticado.id}")
    print(f"  Nombre: {usuario_autenticado.nombre}")
    print(f"  Email: {usuario_autenticado.email}")
    print(f"  Rol: {usuario_autenticado.rol}")
    
    pausa()

def submenu_reportar_problema():
    global usuario_autenticado
    
    limpiar_pantalla()
    mostrar_encabezado("REPORTAR PROBLEMA")
    
    print("  Describa el problema que desea reportar:")
    problema = leer_texto("  > ")
    
    resultado = reportar_problema(usuario_autenticado, problema)
    
    if resultado['exito']:
        print(f"\n  Éxito: {resultado['mensaje']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_ver_incidencias_usuario():
    limpiar_pantalla()
    mostrar_encabezado("TODAS LAS INCIDENCIAS")
    
    incidencias = listar_incidencias()
    
    if len(incidencias) == 0:
        print("\n  No hay incidencias registradas.")
    else:
        print(f"\n  Total de incidencias: {len(incidencias)}")
        print("-" * 60)
        for i in incidencias:
            print(f"  ID: {i.id} | {i.Titulo} | Estado: {i.Estado} | Prioridad: {i.prioridad}")
            print(f"    Descripción: {i.Descripcion[:50]}...")
            print("-" * 40)
    
    pausa()

def menu_principal_autenticado():
    global usuario_autenticado, es_admin_autenticado
    
    while True:
        limpiar_pantalla()
        mostrar_encabezado("SOLUCIONES 2T - SISTEMA DE GESTIÓN")
        print(f"  Usuario: {usuario_autenticado.nombre}")
        print(f"  Rol: {'ADMINISTRADOR' if es_admin_autenticado else 'USUARIO'}")
        print("-" * 60)
        
        if es_admin_autenticado:
            # ===== MENÚ DE ADMINISTRADOR (Gestiona TODAS las incidencias) =====
            print("  1. Ver todas las incidencias")
            print("  2. Gestionar incidencias (cambiar estado, eliminar)")
            print("  3. Ver clientes")
            print("  4. Ver mi perfil")
            print("  5. Cerrar sesión")
            print("  6. Salir del sistema")
        else:
            # ===== MENÚ DE USUARIO FINAL (Helpdesk) =====
            print("  1. Reportar nueva incidencia")
            print("  2. Ver mis incidencias")
            print("  3. Ver detalle de una incidencia")
            print("  4. Ver mi perfil")
            print("  5. Cerrar sesión")
            print("  6. Salir del sistema")
        
        print("-" * 60)
        
        if es_admin_autenticado:
            opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6'])
        else:
            opcion = leer_opcion_menu("Elija una opción: ", ['1', '2', '3', '4', '5', '6'])
        
        if es_admin_autenticado:
            if opcion == '1':
                # Ver TODAS las incidencias
                limpiar_pantalla()
                mostrar_encabezado("TODAS LAS INCIDENCIAS")
                
                incidencias = listar_incidencias()
                
                if len(incidencias) == 0:
                    print("\n  No hay incidencias registradas.")
                else:
                    print(f"\n  Total de incidencias: {len(incidencias)}")
                    print("-" * 60)
                    for i in incidencias:
                        print(f"  ID: {i.id} | {i.Titulo} | Estado: {i.Estado} | Prioridad: {i.prioridad}")
                        print(f"    Usuario ID: {i.usuario_id}")
                        print(f"    Descripción: {i.Descripcion[:50]}...")
                        print("-" * 40)
                pausa()
                
            elif opcion == '2':
                # Gestionar incidencias
                submenu_gestionar_incidencias()
                
            elif opcion == '3':
                # Ver clientes registrados
                limpiar_pantalla()
                mostrar_encabezado("LISTA DE CLIENTES")
                
                clientes = listar_clientes()
                
                if len(clientes) == 0:
                    print("\n  No hay clientes registrados.")
                else:
                    print(f"\n  Total de clientes: {len(clientes)}")
                    print("-" * 60)
                    for c in clientes:
                        print(f"  ID: {c.id} | Nombre: {c.nombre} | Email: {c.email} | Empresa: {c.empresa}")
                pausa()
                
            elif opcion == '4':
                submenu_ver_perfil()
                
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
            # ===== MENÚ DE USUARIO FINAL =====
            if opcion == '1':
                # Reportar nueva incidencia
                limpiar_pantalla()
                mostrar_encabezado("REPORTAR NUEVA INCIDENCIA")
                
                titulo = leer_texto("Título: ")
                descripcion = leer_texto("Descripción: ")
                
                # Selección de prioridad con números
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
                    usuario_autenticado.id if usuario_autenticado else 0,
                    titulo,
                    descripcion,
                    prioridad
                )
                
                if resultado['exito']:
                    print(f"\n  Éxito: {resultado['mensaje']}")
                else:
                    print(f"\n  Error: {resultado['mensaje']}")
                pausa()
                
            elif opcion == '2':
                # Ver SOLO las incidencias del usuario autenticado
                limpiar_pantalla()
                mostrar_encabezado("MIS INCIDENCIAS")
                
                # Filtrar las incidencias por el ID del usuario autenticado
                incidencias = [i for i in listar_incidencias() if i.usuario_id == usuario_autenticado.id]
                
                if len(incidencias) == 0:
                    print("\n  No has reportado ninguna incidencia.")
                else:
                    print(f"\n  Total de tus incidencias: {len(incidencias)}")
                    print("-" * 60)
                    for i in incidencias:
                        print(f"  ID: {i.id} | {i.Titulo} | Estado: {i.Estado} | Prioridad: {i.prioridad}")
                        print(f"    Descripción: {i.Descripcion[:50]}...")
                        print("-" * 40)
                pausa()
                
            elif opcion == '3':
                # Ver detalle de una incidencia (solo si es suya)
                limpiar_pantalla()
                mostrar_encabezado("VER DETALLE DE INCIDENCIA")
                
                id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
                incidencia = buscar_incidencia_por_id(id_incidencia)
                
                if incidencia is None:
                    print("\n  Incidencia no encontrada.")
                elif incidencia.usuario_id != usuario_autenticado.id:
                    print("\n  Error: Esta incidencia no te pertenece.")
                else:
                    print(f"\n  ID: {incidencia.id}")
                    print(f"  Título: {incidencia.Titulo}")
                    print(f"  Descripción: {incidencia.Descripcion}")
                    print(f"  Estado: {incidencia.Estado}")
                    print(f"  Prioridad: {incidencia.prioridad}")
                    print(f"  Fecha de creación: {incidencia.Fecha_Creacion.strftime('%Y-%m-%d %H:%M:%S')}")
                pausa()
                
            elif opcion == '4':
                submenu_ver_perfil()
                
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

def menu_principal_no_autenticado():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("SOLUCIONES 2T")
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
        menu_principal_no_autenticado()
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario.")
        print("  Gracias por usar Soluciones 2T.")
    except Exception as e:
        print(f"\n  Error inesperado: {e}")
        print("  El sistema se cerrará.")

if __name__ == "__main__":
    main()