from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base

# Tabla de asociación para relación muchos-a-muchos entre Libro y Autor
libro_autor = Table(
    'libro_autor', Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.id')),
    Column('autor_id', Integer, ForeignKey('autores.id'))
)

# Tabla de asociación para relación muchos-a-muchos entre Libro y Categoria
libro_categoria = Table(
    'libro_categoria', Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.id')),
    Column('categoria_id', Integer, ForeignKey('categorias.id'))
)

class Libro(Base):
    __tablename__ = 'libros'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    isbn = Column(String, unique=True)
    fecha_publicacion = Column(Date)
    cantidad_disponible = Column(Integer, default=1)
    
    # Relaciones
    autores = relationship("Autor", secondary=libro_autor, back_populates="libros")
    categorias = relationship("Categoria", secondary=libro_categoria, back_populates="libros")
    prestamos = relationship("Prestamo", back_populates="libro")

class Autor(Base):
    __tablename__ = 'autores'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String)
    nacionalidad = Column(String)
    
    libros = relationship("Libro", secondary=libro_autor, back_populates="autores")

class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    
    libros = relationship("Libro", secondary=libro_categoria, back_populates="categorias")

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String)
    email = Column(String, unique=True)
    telefono = Column(String)
    
    prestamos = relationship("Prestamo", back_populates="usuario")

class Prestamo(Base):
    __tablename__ = 'prestamos'
    
    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer, ForeignKey('libros.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_prestamo = Column(Date, nullable=False)
    fecha_devolucion = Column(Date)
    devuelto = Column(Boolean, default=False)
    
    # Relaciones
    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")