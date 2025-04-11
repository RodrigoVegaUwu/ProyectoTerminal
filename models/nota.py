from flask import current_app

class Nota:
    @staticmethod
    def registrar(paciente_id, titulo, descripcion, cedula_profesional, imagen_path=None):
        nota_ref = current_app.db.collection('notas').document()
        nota_ref.set({
            'paciente_id': paciente_id,
            'titulo': titulo,
            'descripcion': descripcion,
            'cedula_profesional': cedula_profesional,
            'imagen_path': imagen_path
        })

    @staticmethod
    def obtener_por_paciente(paciente_id):
        notas = current_app.db.collection('notas').where('paciente_id', '==', paciente_id).stream()

        return [{'id': nota.id, **nota.to_dict()} for nota in notas]

    @staticmethod
    def obtener_por_id(nota_id):
        nota_ref = current_app.db.collection('notas').document(nota_id)
        nota = nota_ref.get()
        if nota.exists:
            return nota.to_dict()
        return None

