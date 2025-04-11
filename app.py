import os
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

    firebase_cred_path = "gestiondehistorialesmedicos-firebase-adminsdk-9emsw-b003efa3e0.json"

    firebase_cred_path = "gestiondehistorialesmedicos-firebase-adminsdk-9emsw-b003efa3e0.json"
    if not firebase_admin._apps:
        if os.path.exists(firebase_cred_path):
            cred = credentials.Certificate(firebase_cred_path)
            firebase_admin.initialize_app(cred)
            app.db = firestore.client()
        else:
            raise FileNotFoundError(f"No se encontró el archivo de credenciales de Firebase: {firebase_cred_path}")

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

    from controllers.auth_controller import auth_bp
    from controllers.paciente_controller import paciente_bp
    from controllers.main_controller import main_bp
    from controllers.receta_controller import receta_bp
    from controllers.nota_controller import nota_bp
    from controllers.citas_controller import cita_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(receta_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(cita_bp)

    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
