from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, 
                            QLabel, QLineEdit, QDateEdit, QComboBox, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt, QDate
from operations import *
from database import get_db

class BibliotecaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Biblioteca")
        self.setGeometry(100, 100, 900, 600)
        
        self.db = next(get_db())
        
        self.initUI()
        self.cargar_datos_iniciales()
        
    def initUI(self):
        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Pestañas para las diferentes secciones
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Crear las pestañas
        self.crear_tab_libros()
        self.crear_tab_autores()
        self.crear_tab_usuarios()
        self.crear_tab_prestamos()
        self.crear_tab_busquedas()
        self.crear_tab_consultas()
        
    def crear_tab_libros(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Libros")
        layout = QVBoxLayout(tab)
        
        # Formulario para agregar/editar libros
        form_layout = QFormLayout()
        
        self.libro_id_edit = QLineEdit()
        self.libro_id_edit.setEnabled(False)
        form_layout.addRow("ID:", self.libro_id_edit)
        
        self.libro_titulo_edit = QLineEdit()
        form_layout.addRow("Título:", self.libro_titulo_edit)
        
        self.libro_isbn_edit = QLineEdit()
        form_layout.addRow("ISBN:", self.libro_isbn_edit)
        
        self.libro_fecha_edit = QDateEdit()
        self.libro_fecha_edit.setCalendarPopup(True)
        form_layout.addRow("Fecha Publicación:", self.libro_fecha_edit)
        
        self.libro_cantidad_edit = QLineEdit()
        self.libro_cantidad_edit.setText("1")
        form_layout.addRow("Cantidad:", self.libro_cantidad_edit)
        
        # Botones para operaciones CRUD
        btn_layout = QHBoxLayout()
        
        self.btn_agregar_libro = QPushButton("Agregar")
        self.btn_agregar_libro.clicked.connect(self.agregar_libro)
        btn_layout.addWidget(self.btn_agregar_libro)
        
        self.btn_actualizar_libro = QPushButton("Actualizar")
        self.btn_actualizar_libro.clicked.connect(self.actualizar_libro)
        btn_layout.addWidget(self.btn_actualizar_libro)
        
        self.btn_eliminar_libro = QPushButton("Eliminar")
        self.btn_eliminar_libro.clicked.connect(self.eliminar_libro)
        btn_layout.addWidget(self.btn_eliminar_libro)
        
        self.btn_limpiar_libro = QPushButton("Limpiar")
        self.btn_limpiar_libro.clicked.connect(self.limpiar_formulario_libro)
        btn_layout.addWidget(self.btn_limpiar_libro)
        
        form_layout.addRow(btn_layout)
        layout.addLayout(form_layout)
        
        # Tabla para mostrar los libros
        self.libros_table = QTableWidget()
        self.libros_table.setColumnCount(5)
        self.libros_table.setHorizontalHeaderLabels(["ID", "Título", "ISBN", "Publicación", "Disponibles"])
        self.libros_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.libros_table.cellClicked.connect(self.seleccionar_libro)
        
        layout.addWidget(QLabel("Lista de Libros:"))
        layout.addWidget(self.libros_table)
        
    def crear_tab_autores(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Autores")
        layout = QVBoxLayout(tab)
        
        # Formulario para autores
        form_layout = QFormLayout()
        
        self.autor_id_edit = QLineEdit()
        self.autor_id_edit.setEnabled(False)
        form_layout.addRow("ID:", self.autor_id_edit)
        
        self.autor_nombre_edit = QLineEdit()
        form_layout.addRow("Nombre:", self.autor_nombre_edit)
        
        self.autor_apellido_edit = QLineEdit()
        form_layout.addRow("Apellido:", self.autor_apellido_edit)
        
        self.autor_nacionalidad_edit = QLineEdit()
        form_layout.addRow("Nacionalidad:", self.autor_nacionalidad_edit)
        
        # Botones para autores
        btn_layout = QHBoxLayout()
        
        self.btn_agregar_autor = QPushButton("Agregar")
        self.btn_agregar_autor.clicked.connect(self.agregar_autor)
        btn_layout.addWidget(self.btn_agregar_autor)
        
        self.btn_limpiar_autor = QPushButton("Limpiar")
        self.btn_limpiar_autor.clicked.connect(self.limpiar_formulario_autor)
        btn_layout.addWidget(self.btn_limpiar_autor)
        
        form_layout.addRow(btn_layout)
        layout.addLayout(form_layout)
        
        # Tabla de autores
        self.autores_table = QTableWidget()
        self.autores_table.setColumnCount(4)
        self.autores_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Nacionalidad"])
        self.autores_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.autores_table.cellClicked.connect(self.seleccionar_autor)
        
        layout.addWidget(QLabel("Lista de Autores:"))
        layout.addWidget(self.autores_table)
        
    def crear_tab_usuarios(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Usuarios")
        layout = QVBoxLayout(tab)
        
        # Formulario para usuarios
        form_layout = QFormLayout()
        
        self.usuario_id_edit = QLineEdit()
        self.usuario_id_edit.setEnabled(False)
        form_layout.addRow("ID:", self.usuario_id_edit)
        
        self.usuario_nombre_edit = QLineEdit()
        form_layout.addRow("Nombre:", self.usuario_nombre_edit)
        
        self.usuario_apellido_edit = QLineEdit()
        form_layout.addRow("Apellido:", self.usuario_apellido_edit)
        
        self.usuario_email_edit = QLineEdit()
        form_layout.addRow("Email:", self.usuario_email_edit)
        
        self.usuario_telefono_edit = QLineEdit()
        form_layout.addRow("Teléfono:", self.usuario_telefono_edit)
        
        # Botones para usuarios
        btn_layout = QHBoxLayout()
        
        self.btn_agregar_usuario = QPushButton("Agregar")
        self.btn_agregar_usuario.clicked.connect(self.agregar_usuario)
        btn_layout.addWidget(self.btn_agregar_usuario)
        
        self.btn_limpiar_usuario = QPushButton("Limpiar")
        self.btn_limpiar_usuario.clicked.connect(self.limpiar_formulario_usuario)
        btn_layout.addWidget(self.btn_limpiar_usuario)
        
        form_layout.addRow(btn_layout)
        layout.addLayout(form_layout)
        
        # Tabla de usuarios
        self.usuarios_table = QTableWidget()
        self.usuarios_table.setColumnCount(5)
        self.usuarios_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Email", "Teléfono"])
        self.usuarios_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.usuarios_table.cellClicked.connect(self.seleccionar_usuario)
        
        layout.addWidget(QLabel("Lista de Usuarios:"))
        layout.addWidget(self.usuarios_table)
        
    def crear_tab_prestamos(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Préstamos")
        layout = QVBoxLayout(tab)
        
        # Formulario para préstamos
        form_layout = QFormLayout()
        
        self.prestamo_id_edit = QLineEdit()
        self.prestamo_id_edit.setEnabled(False)
        form_layout.addRow("ID Préstamo:", self.prestamo_id_edit)
        
        # Combobox para seleccionar libro
        self.prestamo_libro_combo = QComboBox()
        form_layout.addRow("Libro:", self.prestamo_libro_combo)
        
        # Combobox para seleccionar usuario
        self.prestamo_usuario_combo = QComboBox()
        form_layout.addRow("Usuario:", self.prestamo_usuario_combo)
        
        self.prestamo_fecha_edit = QDateEdit()
        self.prestamo_fecha_edit.setDate(QDate.currentDate())
        self.prestamo_fecha_edit.setCalendarPopup(True)
        form_layout.addRow("Fecha Préstamo:", self.prestamo_fecha_edit)
        
        self.prestamo_devuelto_check = QComboBox()
        self.prestamo_devuelto_check.addItems(["No", "Sí"])
        form_layout.addRow("Devuelto:", self.prestamo_devuelto_check)
        
        self.prestamo_fecha_devolucion_edit = QDateEdit()
        self.prestamo_fecha_devolucion_edit.setDate(QDate.currentDate())
        self.prestamo_fecha_devolucion_edit.setCalendarPopup(True)
        form_layout.addRow("Fecha Devolución:", self.prestamo_fecha_devolucion_edit)
        
        # Botones para préstamos
        btn_layout = QHBoxLayout()
        
        self.btn_agregar_prestamo = QPushButton("Registrar Préstamo")
        self.btn_agregar_prestamo.clicked.connect(self.registrar_prestamo)
        btn_layout.addWidget(self.btn_agregar_prestamo)
        
        self.btn_devolver_libro = QPushButton("Marcar como Devuelto")
        self.btn_devolver_libro.clicked.connect(self.marcar_devuelto)
        btn_layout.addWidget(self.btn_devolver_libro)
        
        self.btn_limpiar_prestamo = QPushButton("Limpiar")
        self.btn_limpiar_prestamo.clicked.connect(self.limpiar_formulario_prestamo)
        btn_layout.addWidget(self.btn_limpiar_prestamo)
        
        form_layout.addRow(btn_layout)
        layout.addLayout(form_layout)
        
        # Tabla de préstamos
        self.prestamos_table = QTableWidget()
        self.prestamos_table.setColumnCount(7)
        self.prestamos_table.setHorizontalHeaderLabels(["ID", "Libro", "Usuario", "Fecha Préstamo", "Fecha Devolución", "Devuelto", "Estado"])
        self.prestamos_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.prestamos_table.cellClicked.connect(self.seleccionar_prestamo)
        
        layout.addWidget(QLabel("Préstamos Activos:"))
        layout.addWidget(self.prestamos_table)
        
    def crear_tab_busquedas(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Búsquedas")
        layout = QVBoxLayout(tab)
        
        # Opciones de búsqueda
        search_layout = QHBoxLayout()
        
        self.busqueda_tipo = QComboBox()
        self.busqueda_tipo.addItems(["Por título", "Por autor", "Por categoría"])
        search_layout.addWidget(self.busqueda_tipo)
        
        self.busqueda_parametro = QLineEdit()
        search_layout.addWidget(self.busqueda_parametro)
        
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.realizar_busqueda)
        search_layout.addWidget(self.btn_buscar)
        
        layout.addLayout(search_layout)
        
        # Resultados de búsqueda
        self.resultados_busqueda_table = QTableWidget()
        self.resultados_busqueda_table.setColumnCount(4)
        self.resultados_busqueda_table.setHorizontalHeaderLabels(["ID", "Título", "Autores", "Disponibles"])
        
        layout.addWidget(QLabel("Resultados:"))
        layout.addWidget(self.resultados_busqueda_table)
        
    def crear_tab_consultas(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Consultas")
        layout = QVBoxLayout(tab)
        
        # Botones para consultas avanzadas
        btn_layout = QHBoxLayout()
        
        self.btn_autor_mas_libros = QPushButton("Autor con más libros")
        self.btn_autor_mas_libros.clicked.connect(self.mostrar_autor_mas_libros)
        btn_layout.addWidget(self.btn_autor_mas_libros)
        
        self.btn_libros_ordenados = QPushButton("Libros ordenados")
        self.btn_libros_ordenados.clicked.connect(self.mostrar_libros_ordenados)
        btn_layout.addWidget(self.btn_libros_ordenados)
        
        layout.addLayout(btn_layout)
        
        # Resultados de consultas
        self.resultados_consulta_table = QTableWidget()
        self.resultados_consulta_table.setColumnCount(4)
        self.resultados_consulta_table.setHorizontalHeaderLabels(["ID", "Título", "Autores", "Publicación"])
        
        layout.addWidget(QLabel("Resultados:"))
        layout.addWidget(self.resultados_consulta_table)
        
    def cargar_datos_iniciales(self):
        self.actualizar_tabla_libros()
        self.actualizar_tabla_autores()
        self.actualizar_tabla_usuarios()
        self.actualizar_tabla_prestamos()
        self.actualizar_combos_prestamos()
        
    def actualizar_tabla_libros(self):
        libros = listar_libros(self.db)
        self.libros_table.setRowCount(len(libros))
        
        for i, libro in enumerate(libros):
            self.libros_table.setItem(i, 0, QTableWidgetItem(str(libro.id)))
            self.libros_table.setItem(i, 1, QTableWidgetItem(libro.titulo))
            self.libros_table.setItem(i, 2, QTableWidgetItem(libro.isbn or ""))
            self.libros_table.setItem(i, 3, QTableWidgetItem(str(libro.fecha_publicacion) if libro.fecha_publicacion else ""))
            self.libros_table.setItem(i, 4, QTableWidgetItem(str(libro.cantidad_disponible)))
            
    def actualizar_tabla_autores(self):
        autores = self.db.query(Autor).all()
        self.autores_table.setRowCount(len(autores))
        
        for i, autor in enumerate(autores):
            self.autores_table.setItem(i, 0, QTableWidgetItem(str(autor.id)))
            self.autores_table.setItem(i, 1, QTableWidgetItem(autor.nombre))
            self.autores_table.setItem(i, 2, QTableWidgetItem(autor.apellido or ""))
            self.autores_table.setItem(i, 3, QTableWidgetItem(autor.nacionalidad or ""))
            
    def actualizar_tabla_usuarios(self):
        usuarios = self.db.query(Usuario).all()
        self.usuarios_table.setRowCount(len(usuarios))
        
        for i, usuario in enumerate(usuarios):
            self.usuarios_table.setItem(i, 0, QTableWidgetItem(str(usuario.id)))
            self.usuarios_table.setItem(i, 1, QTableWidgetItem(usuario.nombre))
            self.usuarios_table.setItem(i, 2, QTableWidgetItem(usuario.apellido or ""))
            self.usuarios_table.setItem(i, 3, QTableWidgetItem(usuario.email or ""))
            self.usuarios_table.setItem(i, 4, QTableWidgetItem(usuario.telefono or ""))
            
    def actualizar_tabla_prestamos(self):
        prestamos = listar_prestamos_activos(self.db)
        self.prestamos_table.setRowCount(len(prestamos))
        
        for i, prestamo in enumerate(prestamos):
            self.prestamos_table.setItem(i, 0, QTableWidgetItem(str(prestamo.id)))
            self.prestamos_table.setItem(i, 1, QTableWidgetItem(prestamo.libro.titulo))
            self.prestamos_table.setItem(i, 2, QTableWidgetItem(f"{prestamo.usuario.nombre} {prestamo.usuario.apellido or ''}"))
            self.prestamos_table.setItem(i, 3, QTableWidgetItem(str(prestamo.fecha_prestamo)))
            self.prestamos_table.setItem(i, 4, QTableWidgetItem(str(prestamo.fecha_devolucion) if prestamo.fecha_devolucion else ""))
            self.prestamos_table.setItem(i, 5, QTableWidgetItem("Sí" if prestamo.devuelto else "No"))
            self.prestamos_table.setItem(i, 6, QTableWidgetItem("Devuelto" if prestamo.devuelto else "Activo"))
            
    def actualizar_combos_prestamos(self):
        self.prestamo_libro_combo.clear()
        libros = listar_libros(self.db)
        for libro in libros:
            if libro.cantidad_disponible > 0:
                self.prestamo_libro_combo.addItem(libro.titulo, libro.id)
                
        self.prestamo_usuario_combo.clear()
        usuarios = self.db.query(Usuario).all()
        for usuario in usuarios:
            self.prestamo_usuario_combo.addItem(f"{usuario.nombre} {usuario.apellido or ''}", usuario.id)
            
    # Métodos para libros
    def seleccionar_libro(self, row, column):
        libro_id = int(self.libros_table.item(row, 0).text())
        libro = obtener_libro(self.db, libro_id)
        
        if libro:
            self.libro_id_edit.setText(str(libro.id))
            self.libro_titulo_edit.setText(libro.titulo)
            self.libro_isbn_edit.setText(libro.isbn or "")
            self.libro_fecha_edit.setDate(QDate.fromString(str(libro.fecha_publicacion), "yyyy-MM-dd") if libro.fecha_publicacion else QDate.currentDate())
            self.libro_cantidad_edit.setText(str(libro.cantidad_disponible))
            
    def limpiar_formulario_libro(self):
        self.libro_id_edit.clear()
        self.libro_titulo_edit.clear()
        self.libro_isbn_edit.clear()
        self.libro_fecha_edit.setDate(QDate.currentDate())
        self.libro_cantidad_edit.setText("1")
        
    def agregar_libro(self):
        titulo = self.libro_titulo_edit.text()
        isbn = self.libro_isbn_edit.text()
        fecha = self.libro_fecha_edit.date().toPyDate()
        cantidad = int(self.libro_cantidad_edit.text())
        
        if not titulo:
            QMessageBox.warning(self, "Error", "El título es obligatorio")
            return
            
        libro = crear_libro(self.db, titulo, isbn or None, fecha, cantidad)
        if libro:
            QMessageBox.information(self, "Éxito", f"Libro '{libro.titulo}' creado con ID {libro.id}")
            self.actualizar_tabla_libros()
            self.limpiar_formulario_libro()
            self.actualizar_combos_prestamos()
            
    def actualizar_libro(self):
        libro_id = self.libro_id_edit.text()
        if not libro_id:
            QMessageBox.warning(self, "Error", "Seleccione un libro para actualizar")
            return
            
        libro_id = int(libro_id)
        titulo = self.libro_titulo_edit.text()
        isbn = self.libro_isbn_edit.text()
        fecha = self.libro_fecha_edit.date().toPyDate()
        cantidad = int(self.libro_cantidad_edit.text())
        
        libro = actualizar_libro(self.db, libro_id, titulo, isbn or None, fecha, cantidad)
        if libro:
            QMessageBox.information(self, "Éxito", f"Libro '{libro.titulo}' actualizado")
            self.actualizar_tabla_libros()
            self.actualizar_combos_prestamos()
            
    def eliminar_libro(self):
        libro_id = self.libro_id_edit.text()
        if not libro_id:
            QMessageBox.warning(self, "Error", "Seleccione un libro para eliminar")
            return
            
        respuesta = QMessageBox.question(self, "Confirmar", "¿Está seguro de eliminar este libro?")
        if respuesta == QMessageBox.Yes:
            if eliminar_libro(self.db, int(libro_id)):
                QMessageBox.information(self, "Éxito", "Libro eliminado")
                self.actualizar_tabla_libros()
                self.limpiar_formulario_libro()
                self.actualizar_combos_prestamos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el libro")
                
    # Métodos para autores
    def seleccionar_autor(self, row, column):
        autor_id = int(self.autores_table.item(row, 0).text())
        autor = obtener_autor(self.db, autor_id)
        
        if autor:
            self.autor_id_edit.setText(str(autor.id))
            self.autor_nombre_edit.setText(autor.nombre)
            self.autor_apellido_edit.setText(autor.apellido or "")
            self.autor_nacionalidad_edit.setText(autor.nacionalidad or "")
            
    def limpiar_formulario_autor(self):
        self.autor_id_edit.clear()
        self.autor_nombre_edit.clear()
        self.autor_apellido_edit.clear()
        self.autor_nacionalidad_edit.clear()
        
    def agregar_autor(self):
        nombre = self.autor_nombre_edit.text()
        apellido = self.autor_apellido_edit.text()
        nacionalidad = self.autor_nacionalidad_edit.text()
        
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return
            
        autor = crear_autor(self.db, nombre, apellido or None, nacionalidad or None)
        if autor:
            QMessageBox.information(self, "Éxito", f"Autor '{autor.nombre} {autor.apellido or ''}' creado con ID {autor.id}")
            self.actualizar_tabla_autores()
            self.limpiar_formulario_autor()
            
    # Métodos para usuarios
    def seleccionar_usuario(self, row, column):
        usuario_id = int(self.usuarios_table.item(row, 0).text())
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if usuario:
            self.usuario_id_edit.setText(str(usuario.id))
            self.usuario_nombre_edit.setText(usuario.nombre)
            self.usuario_apellido_edit.setText(usuario.apellido or "")
            self.usuario_email_edit.setText(usuario.email or "")
            self.usuario_telefono_edit.setText(usuario.telefono or "")
            
    def limpiar_formulario_usuario(self):
        self.usuario_id_edit.clear()
        self.usuario_nombre_edit.clear()
        self.usuario_apellido_edit.clear()
        self.usuario_email_edit.clear()
        self.usuario_telefono_edit.clear()
        
    def agregar_usuario(self):
        nombre = self.usuario_nombre_edit.text()
        apellido = self.usuario_apellido_edit.text()
        email = self.usuario_email_edit.text()
        telefono = self.usuario_telefono_edit.text()
        
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return
            
        usuario = crear_usuario(self.db, nombre, apellido or None, email or None, telefono or None)
        if usuario:
            QMessageBox.information(self, "Éxito", f"Usuario '{usuario.nombre} {usuario.apellido or ''}' creado con ID {usuario.id}")
            self.actualizar_tabla_usuarios()
            self.limpiar_formulario_usuario()
            self.actualizar_combos_prestamos()
            
    # Métodos para préstamos
    def seleccionar_prestamo(self, row, column):
        prestamo_id = int(self.prestamos_table.item(row, 0).text())
        prestamo = self.db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
        
        if prestamo:
            self.prestamo_id_edit.setText(str(prestamo.id))
            
            # Buscar índice del libro en el combo
            libro_index = self.prestamo_libro_combo.findData(prestamo.libro_id)
            if libro_index >= 0:
                self.prestamo_libro_combo.setCurrentIndex(libro_index)
                
            # Buscar índice del usuario en el combo
            usuario_index = self.prestamo_usuario_combo.findData(prestamo.usuario_id)
            if usuario_index >= 0:
                self.prestamo_usuario_combo.setCurrentIndex(usuario_index)
                
            self.prestamo_fecha_edit.setDate(QDate.fromString(str(prestamo.fecha_prestamo), "yyyy-MM-dd"))
            self.prestamo_devuelto_check.setCurrentIndex(1 if prestamo.devuelto else 0)
            
            if prestamo.fecha_devolucion:
                self.prestamo_fecha_devolucion_edit.setDate(QDate.fromString(str(prestamo.fecha_devolucion), "yyyy-MM-dd"))
            else:
                self.prestamo_fecha_devolucion_edit.setDate(QDate.currentDate())
                
    def limpiar_formulario_prestamo(self):
        self.prestamo_id_edit.clear()
        self.prestamo_libro_combo.setCurrentIndex(0)
        self.prestamo_usuario_combo.setCurrentIndex(0)
        self.prestamo_fecha_edit.setDate(QDate.currentDate())
        self.prestamo_devuelto_check.setCurrentIndex(0)
        self.prestamo_fecha_devolucion_edit.setDate(QDate.currentDate())
        
    def registrar_prestamo(self):
        libro_id = self.prestamo_libro_combo.currentData()
        usuario_id = self.prestamo_usuario_combo.currentData()
        fecha_prestamo = self.prestamo_fecha_edit.date().toPyDate()
        
        if not libro_id or not usuario_id:
            QMessageBox.warning(self, "Error", "Seleccione libro y usuario")
            return
            
        prestamo = registrar_prestamo(self.db, libro_id, usuario_id, fecha_prestamo)
        if prestamo:
            QMessageBox.information(self, "Éxito", f"Préstamo registrado con ID {prestamo.id}")
            self.actualizar_tabla_prestamos()
            self.actualizar_tabla_libros()
            self.limpiar_formulario_prestamo()
            
    def marcar_devuelto(self):
        prestamo_id = self.prestamo_id_edit.text()
        if not prestamo_id:
            QMessageBox.warning(self, "Error", "Seleccione un préstamo")
            return
            
        prestamo_id = int(prestamo_id)
        fecha_devolucion = self.prestamo_fecha_devolucion_edit.date().toPyDate()
        
        prestamo = marcar_devuelto(self.db, prestamo_id, fecha_devolucion)
        if prestamo:
            QMessageBox.information(self, "Éxito", f"Libro '{prestamo.libro.titulo}' marcado como devuelto")
            self.actualizar_tabla_prestamos()
            self.actualizar_tabla_libros()
            self.limpiar_formulario_prestamo()
            
    # Métodos para búsquedas
    def realizar_busqueda(self):
        tipo = self.busqueda_tipo.currentText()
        parametro = self.busqueda_parametro.text()
        
        if not parametro:
            QMessageBox.warning(self, "Error", "Ingrese un parámetro de búsqueda")
            return
            
        if tipo == "Por título":
            libros = buscar_libros_por_titulo(self.db, parametro)
        elif tipo == "Por autor":
            # Buscar autores que coincidan
            autores = self.db.query(Autor).filter(
                (Autor.nombre.ilike(f"%{parametro}%")) | 
                (Autor.apellido.ilike(f"%{parametro}%"))
            ).all()
            
            if not autores:
                QMessageBox.information(self, "Resultados", "No se encontraron autores con ese nombre")
                return
                
            # Mostrar libros de los autores encontrados
            libros = []
            for autor in autores:
                libros.extend(autor.libros)
        elif tipo == "Por categoría":
            categorias = self.db.query(Categoria).filter(
                Categoria.nombre.ilike(f"%{parametro}%")
            ).all()
            
            if not categorias:
                QMessageBox.information(self, "Resultados", "No se encontraron categorías con ese nombre")
                return
                
            libros = []
            for categoria in categorias:
                libros.extend(categoria.libros)
                
        self.mostrar_resultados_busqueda(libros)
        
    def mostrar_resultados_busqueda(self, libros):
        self.resultados_busqueda_table.setRowCount(len(libros))
        
        for i, libro in enumerate(libros):
            self.resultados_busqueda_table.setItem(i, 0, QTableWidgetItem(str(libro.id)))
            self.resultados_busqueda_table.setItem(i, 1, QTableWidgetItem(libro.titulo))
            self.resultados_busqueda_table.setItem(i, 2, QTableWidgetItem(", ".join([f"{a.nombre} {a.apellido or ''}" for a in libro.autores])))
            self.resultados_busqueda_table.setItem(i, 3, QTableWidgetItem(str(libro.cantidad_disponible)))
            
    # Métodos para consultas avanzadas
    def mostrar_autor_mas_libros(self):
        resultado = obtener_autor_mas_libros(self.db)
        if resultado:
            autor, total = resultado
            libros = autor.libros
            
            self.resultados_consulta_table.setRowCount(len(libros))
            self.resultados_consulta_table.setHorizontalHeaderLabels(["ID", "Título", "Autor", "Publicación"])
            
            for i, libro in enumerate(libros):
                self.resultados_consulta_table.setItem(i, 0, QTableWidgetItem(str(libro.id)))
                self.resultados_consulta_table.setItem(i, 1, QTableWidgetItem(libro.titulo))
                self.resultados_consulta_table.setItem(i, 2, QTableWidgetItem(f"{autor.nombre} {autor.apellido or ''}"))
                self.resultados_consulta_table.setItem(i, 3, QTableWidgetItem(str(libro.fecha_publicacion) if libro.fecha_publicacion else ""))
                
            QMessageBox.information(self, "Resultado", 
                                  f"Autor con más libros: {autor.nombre} {autor.apellido or ''}\nTotal: {total} libros")
        else:
            QMessageBox.information(self, "Resultado", "No hay autores registrados")
            
    def mostrar_libros_ordenados(self):
        libros = listar_libros_ordenados(self.db, 'fecha')
        
        self.resultados_consulta_table.setRowCount(len(libros))
        self.resultados_consulta_table.setHorizontalHeaderLabels(["ID", "Título", "Autores", "Publicación"])
        
        for i, libro in enumerate(libros):
            self.resultados_consulta_table.setItem(i, 0, QTableWidgetItem(str(libro.id)))
            self.resultados_consulta_table.setItem(i, 1, QTableWidgetItem(libro.titulo))
            self.resultados_consulta_table.setItem(i, 2, QTableWidgetItem(", ".join([f"{a.nombre} {a.apellido or ''}" for a in libro.autores])))
            self.resultados_consulta_table.setItem(i, 3, QTableWidgetItem(str(libro.fecha_publicacion) if libro.fecha_publicacion else ""))