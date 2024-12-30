from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['password'])
    return None

def get_db_connection():
    conn = sqlite3.connect('colegio.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@login_required
def index():
    nombre = request.args.get('nombre', '')
    apellido = request.args.get('apellido', '')
    grado = request.args.get('grado', '')
    page = int(request.args.get('page', 1))
    per_page = 10

    conn = get_db_connection()
    query = 'SELECT * FROM estudiantes WHERE 1=1'
    params = []

    if nombre:
        query += ' AND nombre LIKE ?'
        params.append(f'%{nombre}%')
    if apellido:
        query += ' AND apellido LIKE ?'
        params.append(f'%{apellido}%')
    if grado:
        query += ' AND grado = ?'
        params.append(grado)

    total_estudiantes = conn.execute(query, params).fetchall()
    total_pages = (len(total_estudiantes) + per_page - 1) // per_page

    query += ' LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])

    estudiantes = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('index.html', estudiantes=estudiantes, page=page, total_pages=total_pages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            user_obj = User(user['id'], user['username'], user['password'])
            login_user(user_obj)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

@app.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        grado = request.form['grado']
        genero = request.form['genero']
        fecha_inscripcion = request.form['fecha_inscripcion']
        estado = request.form['estado']
        nombre_acudiente = request.form['nombre_acudiente']
        telefono_acudiente = request.form['telefono_acudiente']
        correo_acudiente = request.form['correo_acudiente']
        direccion_acudiente = request.form['direccion_acudiente']

        conn = get_db_connection()
        conn.execute('INSERT INTO estudiantes (nombre, apellido, fecha_nacimiento, grado, genero, fecha_inscripcion, estado, nombre_acudiente, telefono_acudiente, correo_acudiente, direccion_acudiente) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (nombre, apellido, fecha_nacimiento, grado, genero, fecha_inscripcion, estado, nombre_acudiente, telefono_acudiente, correo_acudiente, direccion_acudiente))
        conn.commit()
        conn.close()
        flash('Estudiante registrado exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('crear.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    conn = get_db_connection()
    estudiante = conn.execute('SELECT * FROM estudiantes WHERE id = ?', (id,)).fetchone()
    conn.close()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        grado = request.form['grado']
        genero = request.form['genero']
        fecha_inscripcion = request.form['fecha_inscripcion']
        estado = request.form['estado']
        nombre_acudiente = request.form['nombre_acudiente']
        telefono_acudiente = request.form['telefono_acudiente']
        correo_acudiente = request.form['correo_acudiente']
        direccion_acudiente = request.form['direccion_acudiente']

        conn = get_db_connection()
        conn.execute('UPDATE estudiantes SET nombre = ?, apellido = ?, fecha_nacimiento = ?, grado = ?, genero = ?, fecha_inscripcion = ?, estado = ?, nombre_acudiente = ?, telefono_acudiente = ?, correo_acudiente = ?, direccion_acudiente = ? WHERE id = ?',
                     (nombre, apellido, fecha_nacimiento, grado, genero, fecha_inscripcion, estado, nombre_acudiente, telefono_acudiente, correo_acudiente, direccion_acudiente, id))
        conn.commit()
        conn.close()
        flash('Estudiante actualizado exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('editar.html', estudiante=estudiante)

@app.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM estudiantes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Estudiante eliminado exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)