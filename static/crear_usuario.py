import sqlite3

def init_db():
    # Conexión a la base de datos
    conn = sqlite3.connect('colegio.db')
    cursor = conn.cursor()

    # Crear la tabla de estudiantes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        grado TEXT NOT NULL,
        correo TEXT,
        telefono TEXT,
        direccion TEXT,
        genero TEXT,
        fecha_inscripcion DATE NOT NULL,
        estado TEXT NOT NULL
    );
    ''')

    # Crear la tabla de usuarios (administradores o maestros)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    ''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
