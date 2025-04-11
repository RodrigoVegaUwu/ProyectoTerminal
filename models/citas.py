from flask import current_app
from flask_mail import Message

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