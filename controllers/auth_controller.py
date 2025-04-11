from flask import Blueprint, request, render_template, redirect, url_for, session, current_app
from models.usuario import Usuario
import firebase_admin
from firebase_admin import auth, credentials
from flask import Blueprint, request, jsonify, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cedula_profesional = request.form['cedula_profesional']
        password = request.form['password']

        try:
            user = Usuario.autenticar(cedula_profesional, password)
            if user:
                session['user_id'] = user['id']
                session['cedula_profesional'] = user['cedula_profesional']

                return redirect(url_for('main.menu_principal'))
            else:
                return render_template('login.html', error="Credenciales incorrectas.")
        except Exception as e:
            return render_template('login.html', error=f"Error en la autenticación: {e}")

    return render_template('login.html')

@auth_bp.route('/olvidar_contrasena', methods=['GET', 'POST'])
def olvidar_contrasena():
    if request.method == 'POST':
        cedula_profesional = request.form['cedula_profesional']
        
        usuario = Usuario.buscar_por_cedula(cedula_profesional)
        if not usuario:
            return render_template('olvidar_contrasena.html', error="La cédula profesional no es válida.")

        return redirect(url_for('auth.nueva_contrasena', cedula_profesional=cedula_profesional))
    
    return render_template('olvidar_contrasena.html')


@auth_bp.route('/nueva_contrasena/<cedula_profesional>', methods=['GET', 'POST'])
def nueva_contrasena(cedula_profesional):
    if request.method == 'POST':
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        
        if not nueva_contrasena or not confirmar_contrasena:
            return render_template('nueva_contrasena.html', error="Ambos campos son obligatorios.", cedula_profesional=cedula_profesional)
        
        if nueva_contrasena != confirmar_contrasena:
            return render_template('nueva_contrasena.html', error="Las contraseñas no coinciden.", cedula_profesional=cedula_profesional)
        
        if len(nueva_contrasena) < 6:
            return render_template('nueva_contrasena.html', error="La contraseña debe tener al menos 6 caracteres.", cedula_profesional=cedula_profesional)
        
        try:
            Usuario.actualizar_contrasena(cedula_profesional, nueva_contrasena)
            return redirect(url_for('auth.login'))
        except Exception as e:
            return render_template('nueva_contrasena.html', error=f"Error al actualizar la contraseña: {e}", cedula_profesional=cedula_profesional)
    
    return render_template('nueva_contrasena.html', cedula_profesional=cedula_profesional)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        cedula_profesional = request.form['cedula_profesional']
        email = request.form['email']
        password = request.form['password']

        if len(password) < 6:
            return jsonify({"message": "La contraseña debe tener al menos 6 caracteres"}), 400

        try:
            user = current_app.auth.create_user(
                email=email,
                password=password
            )
            
            current_app.db.collection('usuarios').document(user.uid).set({
                'cedula_profesional': cedula_profesional,
                'email': email,
                'password': password
            })

            return redirect(url_for('auth.login'))
        except firebase_admin.auth.EmailAlreadyExistsError:
            return jsonify({"message": "El correo electrónico ya está en uso. Intenta con otro correo electrónico."}), 400
        except Exception as e:
            return jsonify({"message": f"Error al registrar el usuario: {e}"}), 400

    return render_template('registrar.html')
