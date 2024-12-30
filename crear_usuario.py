import sqlite3

def init_db():
    # Conexión a la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Crear la tabla de estudiantes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        grado TEXT NOT NULL,
        genero TEXT,
        fecha_inscripcion DATE NOT NULL,
        estado TEXT NOT NULL,
        nombre_acudiente TEXT NOT NULL,
        telefono_acudiente TEXT,
        correo_acudiente TEXT,
        direccion_acudiente TEXT
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

def crear_usuario(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (username, password) VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()
    print(f"Usuario '{username}' creado exitosamente.")

if __name__ == "__main__":
    init_db()
    # Cambia 'admin' y 'admin' por el nombre de usuario y la contraseña que desees
    crear_usuario('admin', 'admin')