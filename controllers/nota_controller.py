from flask import Blueprint, render_template, request, redirect, url_for, current_app, session
from models.paciente import Paciente
from models.nota import Nota
from models.usuario import Usuario
from werkzeug.utils import secure_filename
import os

nota_bp = Blueprint('nota', __name__)

@nota_bp.route('/historial_notas/<paciente_id>')
def historial_notas(paciente_id):
    paciente = Paciente.obtener_por_id(paciente_id)
    cedula_profesional = session.get('cedula_profesional')
    if not paciente:
        return redirect(url_for('main.menu_principal'))
    usuario = Usuario.buscar_por_cedula(cedula_profesional)
    notas = Nota.obtener_por_paciente(paciente_id)
    return render_template('notas_medicas.html', paciente=paciente, notas=notas, usuario=usuario)


@nota_bp.route('/nueva_nota/<paciente_id>', methods=['GET', 'POST'])
def nueva_nota(paciente_id):
    paciente = Paciente.obtener_por_id(paciente_id)
    if not paciente:
        return redirect(url_for('main.menu_principal'))

    cedula_profesional = session.get('cedula_profesional')

    if request.method == 'POST':
        titulo = request.form['titulo'] 
        nota_texto = request.form['nota']

        imagen = request.files.get('imagen')

        if imagen and imagen.filename != '':
            try:
                filename = secure_filename(imagen.filename)
                relative_path = os.path.join('uploads', filename)
                relative_path = relative_path.replace('\\', '/')  
                absolute_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)  
                imagen.save(absolute_path)
            except Exception as e:
                return render_template('nueva_nota.html', paciente=paciente, cedula_profesional=cedula_profesional, error=f"Error al guardar la imagen: {e}")
        else:
            relative_path = None  

        Nota.registrar(paciente_id, titulo, nota_texto, cedula_profesional, relative_path)

        return redirect(url_for('nota.historial_notas', paciente_id=paciente_id))

    return render_template('nueva_nota.html', paciente=paciente, cedula_profesional=cedula_profesional)


@nota_bp.route('/detalle_nota/<nota_id>')
def detalle_nota(nota_id):
    nota = Nota.obtener_por_id(nota_id)
    if not nota:
        return redirect(url_for('main.menu_principal'))

    if nota.get('imagen_path'):
        nota['imagen_path'] = nota['imagen_path'].replace('\\', '/')
    
    return render_template('detalle_nota.html', nota=nota)