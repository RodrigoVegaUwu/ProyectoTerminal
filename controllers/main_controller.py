from flask import Blueprint, render_template, redirect, url_for, session, current_app
from models.paciente import Paciente

main_bp = Blueprint('main', __name__)

@main_bp.route('/menu_principal')
def menu_principal():
    if 'user_id' in session:
        pacientes_list = Paciente.obtener_todos()
        return render_template('menu_principal.html', pacientes=pacientes_list)
    return redirect(url_for('auth.login'))
