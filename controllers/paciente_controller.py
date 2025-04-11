from flask import Blueprint, request, render_template, redirect, url_for, current_app, session
from models.paciente import Paciente

paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        direccion = request.form['direccion']
        correo = request.form['correo']
        fecha_nacimiento = {
            'dia': request.form['dia'],
            'mes': request.form['mes'],
            'ano': request.form['ano']
        }
        edad = request.form['edad']
        telefono = request.form['telefono']
        es_alergico = request.form.get('es_alergico') == 'on'
        alergias = request.form['alergias'] if es_alergico else ''

        Paciente.registrar(nombre, apellido_paterno, apellido_materno, direccion, correo, fecha_nacimiento, edad, telefono, es_alergico, alergias)

        return redirect(url_for('main.menu_principal'))

    return render_template('paciente.html', paciente=None, titulo="Registrar Paciente")


@paciente_bp.route('/actualizar_paciente/<id>', methods=['GET', 'POST'])
def actualizar_paciente(id):
    paciente = Paciente.obtener_por_id(id)

    if not paciente:
        return redirect(url_for('main.menu_principal'))

    if request.method == 'POST':
        Paciente.actualizar(id, request.form)
        return redirect(url_for('main.menu_principal'))

    return render_template('paciente.html', paciente=paciente, titulo="Actualizar Paciente")
