from flask import current_app

class Receta:
    @staticmethod
    def registrar(paciente_id, nombre_completo, edad, peso, altura, fecha, correo, telefono, diagnostico, cedula_profesional, clinica, tratamiento):
        receta_ref = current_app.db.collection('recetas').document()
        receta_ref.set({
            'paciente_id': paciente_id,
            'nombre_completo': nombre_completo,
            'edad': edad,
            'peso': peso,
            'altura': altura,
            'fecha': fecha,
            'correo': correo,
            'telefono': telefono,
            'diagnostico': diagnostico,
            'cedula_profesional': cedula_profesional,
            'clinica': clinica,
            'tratamiento': tratamiento
        })

    @staticmethod
    def obtener_por_paciente(paciente_id):
        recetas = current_app.db.collection('recetas').where(filter=('paciente_id', '==', paciente_id)).stream()

        return [{'id': receta.id, **receta.to_dict()} for receta in recetas]

    @staticmethod
    def obtener_por_id(receta_id):
        receta_ref = current_app.db.collection('recetas').document(receta_id)
        receta = receta_ref.get()
        if receta.exists:
            return receta.to_dict()
        return None

