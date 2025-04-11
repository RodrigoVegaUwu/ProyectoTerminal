from flask import Blueprint, render_template, request, redirect, url_for, session
from models.paciente import Paciente
from models.receta import Receta
from models.usuario import Usuario

receta_bp = Blueprint('receta', __name__)


@receta_bp.route('/historial_recetas/<paciente_id>')
def historial_recetas(paciente_id):

    paciente = Paciente.obtener_por_id(paciente_id)
    cedula_profesional = session.get('cedula_profesional')
    if not paciente:
        return redirect(url_for('main.menu_principal'))
    
    usuario = Usuario.buscar_por_cedula(cedula_profesional)
    recetas = Receta.obtener_por_paciente(paciente_id)
    return render_template('receta_medica.html', paciente=paciente, recetas=recetas, usuario=usuario)



@receta_bp.route('/nueva_receta/<paciente_id>', methods=['GET', 'POST'])
def nueva_receta(paciente_id):
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        edad = request.form['edad']
        peso = request.form['peso']
        altura = request.form['altura']
        fecha = request.form['fecha']
        correo = request.form['correo']
        telefono = request.form['telefono']  
        diagnostico = request.form['diagnostico']
        cedula_profesional = request.form['cedula_profesional']
        clinica = request.form['clinica']
        tratamiento = request.form['tratamiento']

        Receta.registrar(paciente_id, nombre_completo, edad, peso, altura, fecha, correo, telefono, diagnostico, cedula_profesional, clinica, tratamiento)

        return redirect(url_for('receta.historial_recetas', paciente_id=paciente_id))
    

    paciente = Paciente.obtener_por_id(paciente_id)
    if not paciente:
        return redirect(url_for('main.menu_principal'))

    return render_template('nueva_receta.html', paciente=paciente)

@receta_bp.route('/detalle_receta/<receta_id>')
def detalle_receta(receta_id):
    receta = Receta.obtener_por_id(receta_id) 
    if not receta:
        return redirect(url_for('main.menu_principal')) 
    
    return render_template('detalle_receta.html', receta=receta)
