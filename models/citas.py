from flask import current_app
from flask_mail import Message
from datetime import datetime
from models.paciente import Paciente

class Cita:
    @staticmethod
    def registrar(paciente_id, fecha, hora, minutos, razon, correo_doctor, correo_paciente):
        cita_ref = current_app.db.collection('citas').document()
        cita_ref.set({
            'paciente_id': paciente_id,
            'fecha': fecha,
            'hora': f"{hora}:{minutos}",
            'razon': razon,
            'correo_doctor': correo_doctor,
            'correo_paciente': correo_paciente 
        })

    @staticmethod
    def enviar_correo_cita(nombre_doctor, correo_doctor, correo_paciente, fecha, hora, minutos, razon):
        from app import mail
        msg = Message(
            subject="Confirmación de Cita Médica",
            sender=correo_doctor, 
            recipients=[correo_paciente],
            body=f"Estimado paciente,\n\n"
                f"El doctor {nombre_doctor} ({correo_doctor}) ha agendado una cita para usted.\n"
                f"📅 Fecha: {fecha}\n"
                f"🕒 Hora: {hora}:{minutos}\n"
                f"🩺 Razón: {razon}\n\n"
                f"Por favor, confirme su asistencia respondiendo a este correo.\n"
                f"Gracias por su confianza."
        )
        mail.send(msg)

    @staticmethod
    def obtener_citas_futuras_por_doctor(correo_doctor):
        citas_ref = current_app.db.collection('citas').where('correo_doctor', '==', correo_doctor)
        citas_raw = citas_ref.stream()
        citas = []

        for doc in citas_raw:
            cita_data = doc.to_dict()
            try:
                fecha_hora = datetime.strptime(f"{cita_data['fecha']} {cita_data['hora']}", "%d/%m/%Y %H:%M")
            except ValueError:
                continue

            if fecha_hora >= datetime.now():
                paciente_data = Paciente.obtener_por_id(cita_data['paciente_id'])
                if paciente_data:
                    nombre_completo = f"{paciente_data['nombre']} {paciente_data['apellido_paterno']} {paciente_data['apellido_materno']}"
                else:
                    nombre_completo = "Desconocido"
                cita_data['nombre_paciente'] = nombre_completo
                citas.append(cita_data)

        return citas
