from datetime import date
from sqlalchemy.orm import Session
from database import init_db, get_db
from operations import *
import sys

def mostrar_menu_principal():
    print("\nSistema de Gestión de Biblioteca")
    print("1. Gestión de Libros")
    print("2. Gestión de Autores")
    print("3. Gestión de Usuarios")
    print("4. Gestión de Préstamos")
    print("5. Búsquedas")
    print("6. Consultas avanzadas")
    print("0. Salir")

def mostrar_menu_libros():
    print("\nGestión de Libros")
    print("1. Registrar nuevo libro")
    print("2. Listar todos los libros")
    print("3. Buscar libro por ID")
    print("4. Actualizar libro")
    print("5. Eliminar libro")
    print("0. Volver al menú principal")

def mostrar_menu_autores():
    print("\nGestión de Autores")
    print("1. Registrar nuevo autor")
    print("2. Listar todos los autores")
    print("3. Buscar autor por ID")
    print("0. Volver al menú principal")

def mostrar_menu_usuarios():
    print("\nGestión de Usuarios")
    print("1. Registrar nuevo usuario")
    print("2. Listar todos los usuarios")
    print("3. Buscar usuario por ID")
    print("0. Volver al menú principal")

def mostrar_menu_prestamos():
    print("\nGestión de Préstamos")
    print("1. Registrar nuevo préstamo")
    print("2. Listar préstamos activos")
    print("3. Marcar libro como devuelto")
    print("0. Volver al menú principal")

def mostrar_menu_busquedas():
    print("\nBúsquedas")
    print("1. Buscar libros por título")
    print("2. Buscar libros por autor")
    print("3. Buscar libros por categoría")
    print("0. Volver al menú principal")

def mostrar_menu_consultas():
    print("\nConsultas avanzadas")
    print("1. Autor con más libros")
    print("2. Listar libros ordenados")
    print("0. Volver al menú principal")

def gestion_libros(db: Session):
    while True:
        mostrar_menu_libros()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            titulo = input("Título del libro: ")
            isbn = input("ISBN: ")
            fecha_str = input("Fecha de publicación (YYYY-MM-DD): ")
            fecha = date.fromisoformat(fecha_str) if fecha_str else None
            cantidad = int(input("Cantidad disponible: ") or 1)
            
            libro = crear_libro(db, titulo, isbn, fecha, cantidad)
            print(f"Libro creado: ID {libro.id} - {libro.titulo}")
            
        elif opcion == "2":
            libros = listar_libros(db)
            for libro in libros:
                print(f"ID: {libro.id}, Título: {libro.titulo}, Disponibles: {libro.cantidad_disponible}")
                
        elif opcion == "3":
            libro_id = int(input("ID del libro: "))
            libro = obtener_libro(db, libro_id)
            if libro:
                print(f"ID: {libro.id}, Título: {libro.titulo}, ISBN: {libro.isbn}")
            else:
                print("Libro no encontrado")
                
        elif opcion == "4":
            libro_id = int(input("ID del libro a actualizar: "))
            titulo = input("Nuevo título (dejar vacío para no cambiar): ")
            isbn = input("Nuevo ISBN (dejar vacío para no cambiar): ")
            fecha_str = input("Nueva fecha (YYYY-MM-DD, dejar vacío para no cambiar): ")
            fecha = date.fromisoformat(fecha_str) if fecha_str else None
            cantidad = input("Nueva cantidad (dejar vacío para no cambiar): ")
            cantidad = int(cantidad) if cantidad else None
            
            libro = actualizar_libro(db, libro_id, titulo or None, isbn or None, fecha, cantidad)
            if libro:
                print("Libro actualizado correctamente")
            else:
                print("Error al actualizar el libro")
                
        elif opcion == "5":
            libro_id = int(input("ID del libro a eliminar: "))
            if eliminar_libro(db, libro_id):
                print("Libro eliminado correctamente")
            else:
                print("Error al eliminar el libro")
                
        elif opcion == "0":
            break

def gestion_autores(db: Session):
    while True:
        mostrar_menu_autores()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del autor: ")
            apellido = input("Apellido (opcional): ")
            nacionalidad = input("Nacionalidad (opcional): ")
            
            autor = crear_autor(db, nombre, apellido or None, nacionalidad or None)
            print(f"Autor creado: ID {autor.id} - {autor.nombre} {autor.apellido or ''}")
            
        elif opcion == "2":
            autores = db.query(Autor).all()
            for autor in autores:
                print(f"ID: {autor.id}, Nombre: {autor.nombre} {autor.apellido or ''}")
                
        elif opcion == "3":
            autor_id = int(input("ID del autor: "))
            autor = obtener_autor(db, autor_id)
            if autor:
                print(f"ID: {autor.id}, Nombre: {autor.nombre} {autor.apellido or ''}")
                print("Libros:")
                for libro in autor.libros:
                    print(f"  - {libro.titulo}")
            else:
                print("Autor no encontrado")
                
        elif opcion == "0":
            break

def gestion_usuarios(db: Session):
    while True:
        mostrar_menu_usuarios()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del usuario: ")
            apellido = input("Apellido (opcional): ")
            email = input("Email (opcional): ")
            telefono = input("Teléfono (opcional): ")
            
            usuario = crear_usuario(db, nombre, apellido or None, email or None, telefono or None)
            print(f"Usuario creado: ID {usuario.id} - {usuario.nombre} {usuario.apellido or ''}")
            
        elif opcion == "2":
            usuarios = db.query(Usuario).all()
            for usuario in usuarios:
                print(f"ID: {usuario.id}, Nombre: {usuario.nombre} {usuario.apellido or ''}")
                
        elif opcion == "3":
            usuario_id = int(input("ID del usuario: "))
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if usuario:
                print(f"ID: {usuario.id}, Nombre: {usuario.nombre} {usuario.apellido or ''}")
                print("Préstamos activos:")
                for prestamo in usuario.prestamos:
                    if not prestamo.devuelto:
                        print(f"  - {prestamo.libro.titulo} (Prestado el {prestamo.fecha_prestamo})")
            else:
                print("Usuario no encontrado")
                
        elif opcion == "0":
            break

def gestion_prestamos(db: Session):
    while True:
        mostrar_menu_prestamos()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            libro_id = int(input("ID del libro: "))
            usuario_id = int(input("ID del usuario: "))
            fecha_str = input("Fecha de préstamo (YYYY-MM-DD, hoy si se deja vacío): ")
            fecha = date.fromisoformat(fecha_str) if fecha_str else date.today()
            
            prestamo = registrar_prestamo(db, libro_id, usuario_id, fecha)
            if prestamo:
                print(f"Préstamo registrado: ID {prestamo.id}")
                print(f"Libro: {prestamo.libro.titulo}, Usuario: {prestamo.usuario.nombre}")
            else:
                print("No se pudo registrar el préstamo (libro no disponible o no encontrado)")
                
        elif opcion == "2":
            prestamos = listar_prestamos_activos(db)
            for prestamo in prestamos:
                print(f"ID: {prestamo.id}, Libro: {prestamo.libro.titulo}, Usuario: {prestamo.usuario.nombre}")
                print(f"  Fecha préstamo: {prestamo.fecha_prestamo}")
                
        elif opcion == "3":
            prestamo_id = int(input("ID del préstamo: "))
            fecha_str = input("Fecha de devolución (YYYY-MM-DD, hoy si se deja vacío): ")
            fecha = date.fromisoformat(fecha_str) if fecha_str else date.today()
            
            prestamo = marcar_devuelto(db, prestamo_id, fecha)
            if prestamo:
                print("Libro marcado como devuelto")
                print(f"Libro: {prestamo.libro.titulo} devuelto el {prestamo.fecha_devolucion}")
            else:
                print("Préstamo no encontrado")
                
        elif opcion == "0":
            break

def gestion_busquedas(db: Session):
    while True:
        mostrar_menu_busquedas()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            titulo = input("Título a buscar: ")
            libros = buscar_libros_por_titulo(db, titulo)
            for libro in libros:
                print(f"ID: {libro.id}, Título: {libro.titulo}")
                print(f"  Autores: {', '.join([a.nombre for a in libro.autores])}")
                
        elif opcion == "2":
            autor_id = int(input("ID del autor: "))
            libros = buscar_libros_por_autor(db, autor_id)
            if libros:
                for libro in libros:
                    print(f"ID: {libro.id}, Título: {libro.titulo}")
            else:
                print("No se encontraron libros o el autor no existe")
                
        elif opcion == "3":
            categoria_id = int(input("ID de la categoría: "))
            libros = buscar_libros_por_categoria(db, categoria_id)
            if libros:
                for libro in libros:
                    print(f"ID: {libro.id}, Título: {libro.titulo}")
            else:
                print("No se encontraron libros o la categoría no existe")
                
        elif opcion == "0":
            break

def gestion_consultas(db: Session):
    while True:
        mostrar_menu_consultas()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            resultado = obtener_autor_mas_libros(db)
            if resultado:
                autor, total = resultado
                print(f"Autor con más libros: {autor.nombre} {autor.apellido or ''}")
                print(f"Total de libros: {total}")
            else:
                print("No hay autores registrados")
                
        elif opcion == "2":
            orden = input("Ordenar por (titulo/fecha): ").lower()
            libros = listar_libros_ordenados(db, orden)
            for libro in libros:
                print(f"ID: {libro.id}, Título: {libro.titulo}")
                if orden == 'fecha':
                    print(f"  Fecha publicación: {libro.fecha_publicacion}")
                
        elif opcion == "0":
            break

def main():
    init_db()
    db = next(get_db())
    
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            gestion_libros(db)
        elif opcion == "2":
            gestion_autores(db)
        elif opcion == "3":
            gestion_usuarios(db)
        elif opcion == "4":
            gestion_prestamos(db)
        elif opcion == "5":
            gestion_busquedas(db)
        elif opcion == "6":
            gestion_consultas(db)
        elif opcion == "0":
            print("Saliendo del sistema...")
            sys.exit(0)

if __name__ == "__main__":
    main()