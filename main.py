from funciones import (
    registrar_usuario,
    buscar_usuario_por_email,
    listar_usuarios,
    actualizar_usuario,
    eliminar_usuario,
    contar_usuarios,
    iniciar_sesion,
    reportar_problema,
    registrar_incidencia,
    listar_incidencias,
    buscar_incidencia_por_id,
    actualizar_estado_incidencia,
    eliminar_incidencia,
    contar_incidencias,
    registrar_cliente,
    listar_clientes,
    buscar_cliente_por_email,
    actualizar_cliente,
    eliminar_cliente,
    contar_clientes
)
import os

usuario_autenticado = None

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    
    nombre = leer_texto("Ingrese su nombre completo: ")
    email = leer_texto("Ingrese su correo electronico: ")
    
    from funciones import validar_email
    while not validar_email(email):
        print("  Error: El formato del correo no es valido.")
        email = leer_texto("Ingrese su correo electronico: ")
    
    contrasena = leer_texto("Ingrese su contrasena: ")
    confirmar = leer_texto("Confirme su contrasena: ")
    
    resultado = registrar_usuario(nombre, email, contrasena, confirmar)
    
    if resultado['exito']:
        print(f"\n  Exito: {resultado['mensaje']}")
        print(f"  Usuario registrado: {resultado['usuario']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_buscar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("BUSCAR USUARIO")
    
    email = leer_texto("Ingrese el correo del usuario a buscar: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n  Resultado: No se encontro ningun usuario con ese correo.")
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

def submenu_actualizar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("ACTUALIZAR USUARIO")
    
    email = leer_texto("Ingrese el correo del usuario a actualizar: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n  Error: No se encontro ningun usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  Usuario actual:")
    print(f"    ID: {usuario.id}")
    print(f"    Nombre: {usuario.nombre}")
    print(f"    Email: {usuario.email}")
    print("-" * 40)
    
    nuevo_nombre = input("Nuevo nombre (Enter para no cambiar): ").strip()
    if nuevo_nombre == "":
        nuevo_nombre = None
    
    nueva_contrasena = input("Nueva contrasena (Enter para no cambiar): ").strip()
    if nueva_contrasena == "":
        nueva_contrasena = None
    else:
        confirmar = leer_texto("Confirme la nueva contrasena: ")
        if nueva_contrasena != confirmar:
            print("\n  Error: Las contrasenas no coinciden.")
            pausa()
            return
    
    resultado = actualizar_usuario(email, nuevo_nombre, nueva_contrasena)
    
    if resultado['exito']:
        print(f"\n  Exito: {resultado['mensaje']}")
        print(f"  Usuario actualizado: {resultado['usuario']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_eliminar_usuario():
    limpiar_pantalla()
    mostrar_encabezado("ELIMINAR USUARIO")
    
    email = leer_texto("Ingrese el correo del usuario a eliminar: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n  Error: No se encontro ningun usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  ADVERTENCIA: Esta a punto de eliminar al usuario:")
    print(f"    ID: {usuario.id}")
    print(f"    Nombre: {usuario.nombre}")
    print(f"    Email: {usuario.email}")
    
    confirmar = leer_texto("  Confirmar eliminacion (s/n): ")
    if confirmar.lower() != 's':
        print("\n  Operacion cancelada.")
        pausa()
        return
    
    resultado = eliminar_usuario(email)
    
    if resultado['exito']:
        print(f"\n  Exito: {resultado['mensaje']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_contar_usuarios():
    limpiar_pantalla()
    mostrar_encabezado("TOTAL DE USUARIOS")
    
    total = contar_usuarios()
    print(f"\n  Total de usuarios registrados: {total}")
    
    pausa()

def submenu_cambiar_contrasena():
    limpiar_pantalla()
    mostrar_encabezado("CAMBIAR CONTRASENA")
    
    email = leer_texto("Ingrese su correo electronico: ")
    usuario = buscar_usuario_por_email(email)
    
    if usuario is None:
        print("\n  Error: No se encontro ningun usuario con ese correo.")
        pausa()
        return
    
    print(f"\n  Usuario encontrado: {usuario.nombre}")
    
    nueva_contrasena = leer_texto("Ingrese su nueva contrasena: ")
    confirmar = leer_texto("Confirme su nueva contrasena: ")
    
    if nueva_contrasena != confirmar:
        print("\n  Error: Las contrasenas no coinciden.")
        pausa()
        return
    
    resultado = actualizar_usuario(email, nueva_contrasena=nueva_contrasena)
    
    if resultado['exito']:
        print(f"\n  Exito: Contrasena actualizada exitosamente.")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def submenu_gestionar_usuarios():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTION DE USUARIOS")
        print("  1. Registrar nuevo usuario")
        print("  2. Buscar usuario")
        print("  3. Listar todos los usuarios")
        print("  4. Actualizar usuario")
        print("  5. Eliminar usuario")
        print("  6. Contar usuarios")
        print("  7. Cambiar contrasena")
        print("  8. Volver al menu principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opcion: ", ['1', '2', '3', '4', '5', '6', '7', '8'])
        
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
        mostrar_encabezado("GESTION DE INCIDENCIAS")
        print("  1. Registrar nueva incidencia")
        print("  2. Listar incidencias")
        print("  3. Buscar incidencia por ID")
        print("  4. Cambiar estado de incidencia")
        print("  5. Eliminar incidencia")
        print("  6. Contar incidencias")
        print("  7. Volver al menu principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opcion: ", ['1', '2', '3', '4', '5', '6', '7'])
        
        if opcion == '1':
            limpiar_pantalla()
            mostrar_encabezado("REGISTRAR INCIDENCIA")
            
            titulo = leer_texto("Titulo: ")
            descripcion = leer_texto("Descripcion: ")
            
            print("Prioridades: baja, media, alta, critica")
            prioridad = leer_texto("Prioridad (Enter para 'media'): ", obligatorio=False)
            if prioridad == "":
                prioridad = "media"
            
            resultado = registrar_incidencia(
                usuario_autenticado.id if usuario_autenticado else 0,
                titulo,
                descripcion,
                prioridad
            )
            
            if resultado['exito']:
                print(f"\n  Exito: {resultado['mensaje']}")
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
                    print(f"  ID: {i.id} | {i.titulo} | Estado: {i.estado} | Prioridad: {i.prioridad}")
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
                print(f"  Titulo: {incidencia.titulo}")
                print(f"  Descripcion: {incidencia.descripcion}")
                print(f"  Estado: {incidencia.estado}")
                print(f"  Prioridad: {incidencia.prioridad}")
                print(f"  Fecha: {incidencia.fecha_creacion}")
            pausa()
            
        elif opcion == '4':
            limpiar_pantalla()
            mostrar_encabezado("CAMBIAR ESTADO DE INCIDENCIA")
            
            id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
            
            print("Estados: pendiente, en_proceso, resuelto, cerrado")
            nuevo_estado = leer_texto("Nuevo estado: ")
            
            resultado = actualizar_estado_incidencia(id_incidencia, nuevo_estado)
            
            if resultado['exito']:
                print(f"\n  Exito: {resultado['mensaje']}")
            else:
                print(f"\n  Error: {resultado['mensaje']}")
            pausa()
            
        elif opcion == '5':
            limpiar_pantalla()
            mostrar_encabezado("ELIMINAR INCIDENCIA")
            
            id_incidencia = leer_numero_entero("ID de la incidencia: ", min_valor=1)
            
            confirmar = leer_texto("Confirmar eliminacion (s/n): ")
            if confirmar.lower() == 's':
                resultado = eliminar_incidencia(id_incidencia)
                if resultado['exito']:
                    print(f"\n  Exito: {resultado['mensaje']}")
                else:
                    print(f"\n  Error: {resultado['mensaje']}")
            else:
                print("\n  Operacion cancelada.")
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
        mostrar_encabezado("GESTION DE CLIENTES")
        print("  1. Registrar nuevo cliente")
        print("  2. Listar clientes")
        print("  3. Buscar cliente por email")
        print("  4. Actualizar cliente")
        print("  5. Eliminar cliente")
        print("  6. Contar clientes")
        print("  7. Volver al menu principal")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opcion: ", ['1', '2', '3', '4', '5', '6', '7'])
        
        if opcion == '1':
            limpiar_pantalla()
            mostrar_encabezado("REGISTRAR CLIENTE")
            
            nombre = leer_texto("Nombre completo: ")
            email = leer_texto("Email: ")
            telefono = leer_texto("Telefono: ")
            empresa = leer_texto("Empresa: ")
            
            print("Sectores: publico, privado, educativo, otro")
            sector = leer_texto("Sector: ")
            
            resultado = registrar_cliente(nombre, email, telefono, empresa, sector)
            
            if resultado['exito']:
                print(f"\n  Exito: {resultado['mensaje']}")
            else:
                print(f"\n  Error: {resultado['mensaje']}")
            pausa()
            
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
                print(f"  Telefono: {cliente.telefono}")
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
            nuevo_telefono = input("Nuevo telefono (Enter para no cambiar): ").strip()
            nueva_empresa = input("Nueva empresa (Enter para no cambiar): ").strip()
            
            resultado = actualizar_cliente(
                email,
                nuevo_nombre if nuevo_nombre else None,
                nuevo_telefono if nuevo_telefono else None,
                nueva_empresa if nueva_empresa else None
            )
            
            if resultado['exito']:
                print(f"\n  Exito: {resultado['mensaje']}")
            else:
                print(f"\n  Error: {resultado['mensaje']}")
            pausa()
            
        elif opcion == '5':
            limpiar_pantalla()
            mostrar_encabezado("ELIMINAR CLIENTE")
            
            email = leer_texto("Email del cliente a eliminar: ")
            
            confirmar = leer_texto("Confirmar eliminacion (s/n): ")
            if confirmar.lower() == 's':
                resultado = eliminar_cliente(email)
                if resultado['exito']:
                    print(f"\n  Exito: {resultado['mensaje']}")
                else:
                    print(f"\n  Error: {resultado['mensaje']}")
            else:
                print("\n  Operacion cancelada.")
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
    global usuario_autenticado
    
    limpiar_pantalla()
    mostrar_encabezado("INICIAR SESION")
    
    email = leer_texto("Ingrese su correo electronico: ")
    contrasena = leer_texto("Ingrese su contrasena: ")
    
    resultado = iniciar_sesion(email, contrasena)
    
    if resultado['exito']:
        usuario_autenticado = resultado['usuario']
        print(f"\n  Exito: {resultado['mensaje']}")
        print(f"  Bienvenido, {usuario_autenticado.nombre}!")
        pausa()
        return True
    else:
        print(f"\n  Error: {resultado['mensaje']}")
        pausa()
        return False

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
        print(f"\n  Exito: {resultado['mensaje']}")
    else:
        print(f"\n  Error: {resultado['mensaje']}")
    
    pausa()

def menu_principal_autenticado():
    global usuario_autenticado
    
    while True:
        limpiar_pantalla()
        mostrar_encabezado("SOLUCIONES 2T - SISTEMA DE GESTION")
        print(f"  Usuario autenticado: {usuario_autenticado.nombre}")
        print("-" * 60)
        print("  1. Gestionar usuarios")
        print("  2. Gestionar incidencias")
        print("  3. Gestionar clientes")
        print("  4. Reportar problema")
        print("  5. Ver mi perfil")
        print("  6. Cerrar sesion")
        print("  7. Salir del sistema")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opcion: ", ['1', '2', '3', '4', '5', '6', '7'])
        
        if opcion == '1':
            submenu_gestionar_usuarios()
        elif opcion == '2':
            submenu_gestionar_incidencias()
        elif opcion == '3':
            submenu_gestionar_clientes()
        elif opcion == '4':
            submenu_reportar_problema()
        elif opcion == '5':
            submenu_ver_perfil()
        elif opcion == '6':
            usuario_autenticado = None
            print("\n  Sesion cerrada exitosamente.")
            pausa()
            return
        elif opcion == '7':
            print("\n  Gracias por usar Soluciones 2T.")
            pausa()
            exit(0)

def menu_principal_no_autenticado():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("SOLUCIONES 2T")
        print("  El poder de la tecnologia al alcance de todos.")
        print("-" * 60)
        print("  1. Iniciar sesion")
        print("  2. Registrarse")
        print("  3. Salir")
        print("-" * 60)
        
        opcion = leer_opcion_menu("Elija una opcion: ", ['1', '2', '3'])
        
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
        print("  El sistema se cerrara.")

if __name__ == "__main__":
    main()