from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
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

        citas_ref = current_app.db.collection('citas').where('correo_doctor', '==', correo_doctor)
        citas_existentes = [doc.to_dict() for doc in citas_ref.stream()]

        for cita in citas_existentes:
            fecha_hora_cita = datetime.strptime(f"{cita['fecha']} {cita['hora']}", "%d/%m/%Y %H:%M")
            diferencia = abs((nueva_cita_dt - fecha_hora_cita).total_seconds()) / 60
            if diferencia < 30:
                error = "❌ No se puede agendar esta cita. Debe haber al menos 30 minutos de diferencia con otras citas existentes."
                return render_template('citas.html', paciente=paciente, usuario=usuario, citas=citas_existentes, error=error)

        Cita.registrar(paciente_id, fecha, hora, minutos, razon, correo_doctor, correo_paciente)
        Cita.enviar_correo_cita(nombre_doctor, correo_doctor, correo_paciente, fecha, hora, minutos, razon)

        return redirect(url_for('main.menu_principal'))

    citas_ref = current_app.db.collection('citas').where('paciente_id', '==', paciente_id)
    citas_raw = citas_ref.stream()
    citas = []

    for doc in citas_raw:
        cita_data = doc.to_dict()
        paciente_data = Paciente.obtener_por_id(cita_data['paciente_id'])
        if paciente_data:
            nombre_completo = f"{paciente_data['nombre']} {paciente_data['apellido_paterno']} {paciente_data['apellido_materno']}"
        else:
            nombre_completo = "Desconocido"
        cita_data['nombre_paciente'] = nombre_completo
        citas.append(cita_data)

    return render_template('citas.html', paciente=paciente, usuario=usuario, citas=citas)

