from flask import Blueprint, render_template, request, redirect, url_for, session
from models.paciente import Paciente
from models.citas import Cita
from models.usuario import Usuario
from datetime import datetime, timedelta

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

        nueva_cita_dt = datetime.strptime(f"{fecha} {hora}:{minutos}", "%d/%m/%Y %H:%M")

        citas_existentes = Cita.obtener_citas_futuras_por_doctor(correo_doctor)

        for cita in citas_existentes:
            fecha_hora_cita = datetime.strptime(f"{cita['fecha']} {cita['hora']}", "%d/%m/%Y %H:%M")
            diferencia = abs((nueva_cita_dt - fecha_hora_cita).total_seconds()) / 60
            if diferencia < 30:
                error = "❌ No se puede agendar esta cita. Debe haber al menos 30 minutos de diferencia con otras citas existentes."
                return render_template('citas.html', paciente=paciente, usuario=usuario, citas=citas_existentes, error=error)

        Cita.registrar(paciente_id, fecha, hora, minutos, razon, correo_doctor, correo_paciente)
        Cita.enviar_correo_cita(nombre_doctor, correo_doctor, correo_paciente, fecha, hora, minutos, razon)

        return redirect(url_for('main.menu_principal'))

    citas = Cita.obtener_citas_futuras_por_doctor(usuario['email'])

    return render_template('citas.html', paciente=paciente, usuario=usuario, citas=citas)

