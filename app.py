import os
import json
from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, template_folder='views', static_folder='static')

    app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

    if not firebase_admin._apps:
        firebase_credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        if firebase_credentials_json:
            try:
                cred_dict = json.loads(firebase_credentials_json)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                app.db = firestore.client()
            except Exception as e:
                raise ValueError(f"Error al cargar las credenciales de Firebase: {e}")
        else:
            raise ValueError("No se encontró la variable de entorno GOOGLE_APPLICATION_CREDENTIALS_JSON")

    # Configuración del correo
    app.config.update({
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': 587,
        'MAIL_USE_TLS': True,
        'MAIL_USE_SSL': False,
        'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
        'MAIL_DEFAULT_SENDER': os.getenv('MAIL_USERNAME')
    })

    print("MAIL_USERNAME:", os.getenv('MAIL_USERNAME'))
    print("MAIL_PASSWORD:", os.getenv('MAIL_PASSWORD'))

    mail.init_app(app)

    # Importar Blueprints
    from controllers.auth_controller import auth_bp
    from controllers.paciente_controller import paciente_bp
    from controllers.main_controller import main_bp
    from controllers.receta_controller import receta_bp
    from controllers.nota_controller import nota_bp
    from controllers.citas_controller import cita_bp

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(receta_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(cita_bp)

    # Carpeta de subida
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

