from flask import current_app

class Usuario:
    @staticmethod
    def registrar(email, password, cedula_profesional):
        user = current_app.auth.create_user(email=email, password=password)
        current_app.db.collection('usuarios').document(user.uid).set({
            'cedula_profesional': cedula_profesional,
            'email': email,
            'password': password
        })
        return user

    @staticmethod
    def autenticar(cedula_profesional, password):
        doc = current_app.db.collection('usuarios').where('cedula_profesional', '==', cedula_profesional).get()

        if doc:
            user_data = doc[0].to_dict()
            if user_data['password'] == password:
                return {'id': doc[0].id, **user_data}
        return None

    @staticmethod
    def actualizar_contrasena(cedula_profesional, nueva_contrasena):
        usuario_ref = current_app.db.collection('usuarios').where(filter=('cedula_profesional', '==', cedula_profesional)).get()
        if usuario_ref:
            usuario_id = usuario_ref[0].id
            current_app.db.collection('usuarios').document(usuario_id).update({'password': nueva_contrasena})

    @staticmethod
    def buscar_por_cedula(cedula_profesional):
        usuario_ref = current_app.db.collection('usuarios').where(filter=('cedula_profesional', '==', cedula_profesional)).get()
        if usuario_ref:
            return usuario_ref[0].to_dict() 
        return None
