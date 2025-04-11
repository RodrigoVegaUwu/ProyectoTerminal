from flask import current_app

class Paciente:
    @staticmethod
    def registrar(nombre, apellido_paterno, apellido_materno, direccion, correo, fecha_nacimiento, edad, telefono, es_alergico, alergias):
        paciente_ref = current_app.db.collection('pacientes').document()
        paciente_ref.set({
            'nombre': nombre,
            'apellido_paterno': apellido_paterno,
            'apellido_materno': apellido_materno,
            'direccion': direccion,
            'correo': correo,
            'fecha_nacimiento': fecha_nacimiento,
            'edad': edad,
            'telefono': telefono,
            'es_alergico': es_alergico,
            'alergias': alergias
        })

    @staticmethod
    def obtener_por_id(id):
        paciente_ref = current_app.db.collection('pacientes').document(id)
        paciente = paciente_ref.get()
        if paciente.exists:
            paciente_data = paciente.to_dict()
            paciente_data['id'] = id
            return paciente_data
        return None

    @staticmethod
    def actualizar(id, data):
        paciente_ref = current_app.db.collection('pacientes').document(id)
        paciente_ref.update({
            'nombre': data['nombre'],
            'apellido_paterno': data['apellido_paterno'],
            'apellido_materno': data['apellido_materno'],
            'direccion': data['direccion'],
            'correo': data['correo'],
            'fecha_nacimiento': {
                'dia': data['dia'],
                'mes': data['mes'],
                'ano': data['ano']
            },
            'edad': data['edad'], 
            'telefono': data['telefono'],
            'es_alergico': data.get('es_alergico') == 'on',
            'alergias': data['alergias'] if data.get('es_alergico') == 'on' else ''
        })

    @staticmethod
    def obtener_todos():
        pacientes = current_app.db.collection('pacientes').stream()
        return [{'id': paciente.id, **paciente.to_dict()} for paciente in pacientes]
