from flask import Blueprint, render_template, request, redirect, url_for, session
from models.paciente import Paciente
from models.citas import Cita
from models.usuario import Usuario


cita_bp = Blueprint('cita', __name__)

@cita_bp.route('/generar_cita/<paciente_id>', methods=['GET', 'POST'])
def generar_cita(paciente_id):
    paciente = Paciente.obtener_por_id(paciente_id)
    cedula_profesional = session.get('cedula_profesional')
    usuario = Usuario.buscar_por_cedula(cedula_profesional)  

    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        minutos = request.form['minutos']
        razon = request.form['razon']
        correo_doctor = usuario['email']
        nombre_doctor = usuario['nombre']
        correo_paciente = paciente['correo'] 

        Cita.registrar(paciente_id, fecha, hora, minutos, razon, correo_doctor, correo_paciente)

        Cita.enviar_correo_cita(nombre_doctor, correo_doctor, correo_paciente, fecha, hora, minutos, razon)

        return redirect(url_for('main.menu_principal'))

    return render_template('citas.html', paciente=paciente, usuario=usuario)
