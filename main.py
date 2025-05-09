import sys
from PyQt5.QtWidgets import QApplication
from main_window import BibliotecaApp
from database import init_db

def main():
    # Inicializar la base de datos
    init_db()
    
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    
    # Crear y mostrar ventana principal
    ventana = BibliotecaApp()
    ventana.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()