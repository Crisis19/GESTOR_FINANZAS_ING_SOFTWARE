from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date
from models import Libro, Autor, Categoria, Usuario, Prestamo

# Operaciones CRUD para Libros
def crear_libro(db: Session, titulo: str, isbn: str, fecha_publicacion: date, cantidad: int = 1):
    libro = Libro(
        titulo=titulo,
        isbn=isbn,
        fecha_publicacion=fecha_publicacion,
        cantidad_disponible=cantidad
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

def obtener_libro(db: Session, libro_id: int):
    return db.query(Libro).filter(Libro.id == libro_id).first()

def listar_libros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Libro).offset(skip).limit(limit).all()

def actualizar_libro(db: Session, libro_id: int, titulo: str = None, isbn: str = None, 
                     fecha_publicacion: date = None, cantidad: int = None):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        return None
    
    if titulo is not None:
        libro.titulo = titulo
    if isbn is not None:
        libro.isbn = isbn
    if fecha_publicacion is not None:
        libro.fecha_publicacion = fecha_publicacion
    if cantidad is not None:
        libro.cantidad_disponible = cantidad
    
    db.commit()
    db.refresh(libro)
    return libro

def eliminar_libro(db: Session, libro_id: int):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro:
        db.delete(libro)
        db.commit()
        return True
    return False

# Operaciones CRUD para Autores
def crear_autor(db: Session, nombre: str, apellido: str = None, nacionalidad: str = None):
    autor = Autor(nombre=nombre, apellido=apellido, nacionalidad=nacionalidad)
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor

def obtener_autor(db: Session, autor_id: int):
    return db.query(Autor).filter(Autor.id == autor_id).first()

# Operaciones CRUD para Usuarios
def crear_usuario(db: Session, nombre: str, apellido: str = None, email: str = None, telefono: str = None):
    usuario = Usuario(nombre=nombre, apellido=apellido, email=email, telefono=telefono)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

# Operaciones para Préstamos
def registrar_prestamo(db: Session, libro_id: int, usuario_id: int, fecha_prestamo: date):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro or libro.cantidad_disponible < 1:
        return None
    
    prestamo = Prestamo(
        libro_id=libro_id,
        usuario_id=usuario_id,
        fecha_prestamo=fecha_prestamo,
        devuelto=False
    )
    
    libro.cantidad_disponible -= 1
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo

def marcar_devuelto(db: Session, prestamo_id: int, fecha_devolucion: date):
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        return None
    
    prestamo.devuelto = True
    prestamo.fecha_devolucion = fecha_devolucion
    
    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    if libro:
        libro.cantidad_disponible += 1
    
    db.commit()
    db.refresh(prestamo)
    return prestamo

def listar_prestamos_activos(db: Session):
    return db.query(Prestamo).filter(Prestamo.devuelto == False).all()

# Búsquedas
def buscar_libros_por_titulo(db: Session, titulo: str):
    return db.query(Libro).filter(Libro.titulo.ilike(f"%{titulo}%")).all()

def buscar_libros_por_autor(db: Session, autor_id: int):
    autor = db.query(Autor).filter(Autor.id == autor_id).first()
    if autor:
        return autor.libros
    return []

def buscar_libros_por_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria:
        return categoria.libros
    return []

# Consultas avanzadas
def obtener_autor_mas_libros(db: Session):
    return db.query(
        Autor,
        func.count(Libro.id).label('total_libros')
    ).join(
        Autor.libros
    ).group_by(
        Autor.id
    ).order_by(
        desc('total_libros')
    ).first()

def listar_libros_ordenados(db: Session, orden: str = 'titulo'):
    if orden == 'titulo':
        return db.query(Libro).order_by(Libro.titulo).all()
    elif orden == 'fecha':
        return db.query(Libro).order_by(desc(Libro.fecha_publicacion)).all()
    else:
        return db.query(Libro).all()