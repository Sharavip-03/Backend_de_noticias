from flask_restful import Resource
from flask_restful import Resource
from flask import jsonify
from flask import request
from ..modelos import db, Usuario, UsuarioSchema, Noticias, NoticiasSchema, Comentarios, ComentariosSchema, Calificacion, CalificacionSchema, Admin, AdminSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token

usuario_schema = UsuarioSchema()
noticias_schema = NoticiasSchema()
comentarios_schema = ComentariosSchema()
calificacion_schema = CalificacionSchema()
admin_schema = AdminSchema()


from flask import request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta

from werkzeug.security import generate_password_hash, check_password_hash

class VistaSignIn(Resource):
    def post(self):
        nuevo_usuario = Usuario(
            username=request.json["username"],
            email=request.json.get("email"),
            password=request.json.get("password")
        )
        nuevo_usuario.id_rol = 2
        nuevo_usuario.password = request.json["password"]
        token_de_acceso = create_access_token(identity=request.json['username'])
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return {'mensaje': 'Usuario creado exitosamente', 'token_de_acceso': token_de_acceso}

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            # Crear el token de acceso
            token = create_access_token(identity=nuevo_usuario.id_usuario)
            return {'mensaje': 'Usuario creado exitosamente', 'token': token}, 201
        except IntegrityError:
            db.session.rollback()
            return {'mensaje': 'Error al crear el usuario'}, 500


class VistaLogIn(Resource):
    def post(self):
        u_email = request.json["email"]
        u_contrasena = request.json["password"]
        
        email = Usuario.query.filter_by(email=u_email).first()
        if email and email.verificar_password(u_contrasena):
            return {'mensaje': 'Inicio de sesión exitoso'}, 200
        else:
            return {'mensaje': 'Email o contraseña incorrectos'}, 401




# ----------------------- Gestión de usuarios


class VistaUsuario(Resource):

    def get(self, id_usuario):
        try:
            usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
            if not usuario:
                return {"mensaje": "usuario no encontrado o no válido."}, 404

            # Serializar los datos del usuario
            usuario_serializado = {
                "id_usuario": usuario.id_usuario,
                "username": usuario.username,
                "email": usuario.email
            }
            return jsonify({"usuario": usuario_serializado})

        except Exception as e:
            return {"mensaje": f"Error al obtener el usuario: {str(e)}"}, 500
    


    # Modificar usuario
    def put(self, id_usuario):
        try:
            # Buscar el usuario por ID
            usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
            if not usuario:
                return {"mensaje": "usuario no encontrado o no válido."}, 404

            # Actualizar los campos del usuario si están presentes en la solicitud
            usuario.username = request.json.get("username", usuario.username)
            usuario.email = request.json.get("email", usuario.email)

            # Actualizar la contraseña si está presente
            if request.json.get("contrasena"):
                usuario.contrasena = request.json["contrasena"]

            db.session.commit()

            return {
                "mensaje": "usuario actualizado exitosamente.",
                "usuario": {
                    "id_usuario": usuario.id_usuario,
                    "username": usuario.username,
                    "email": usuario.email
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el usuario: {str(e)}"}, 500

    # Desactivar usuario
def patch(self, id_usuario):
    try:
        # Buscar el usuario por ID
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        if not usuario:
            return {"mensaje": "usuario no encontr ado o no válido."}, 404

        # Cambiar estado a inactivo
        usuario.estado = "inactivo"
        db.session.commit()

        return {"mensaje": "usuario desactivado exitosamente."}, 200
    except Exception as e:
        return {"mensaje": f"Error al desactivar el usuario: {str(e)}"}, 500

# ----------------------- Gestion de noticias

class VistaNoticias(Resource): 

    # Obtener noticias
    def get(self):
        try:
            noticias = Noticias.query.all()
            noticias_serializados = [
                {
                    "id_noticia": noticias.id_noticia,
                    "titulo": noticias.titulo,
                    "descripcion": noticias.descripcion,
                    "diapublicacion": noticias.diapublicacion
                }
                for noticias in noticias
            ]

            return jsonify({"noticias": noticias_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los noticias: {str(e)}"}, 500

    # Agregar noticias
    def post(self):
        try:
            # Validar que los campos necesarios estén presentes
            if not request.json.get("titulo") or not request.json.get("descripcion"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            # Crear una nueva noticia
            nueva_noticia = Noticias(
                titulo=request.json["titulo"],
                descripcion=request.json["descripcion"],
                diapublicacion=request.json.get("diapublicacion")
            )
            db.session.add(nueva_noticia)
            db.session.commit()

            return {
                "mensaje": "Noticia agregada exitosamente.",
                "noticia": {
                    "id_noticia": nueva_noticia.id_noticia,
                    "titulo": nueva_noticia.titulo,
                    "descripcion": nueva_noticia.descripcion,
                    "diapublicacion": nueva_noticia.diapublicacion
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar la noticia: {str(e)}"}, 500

# ----------------------- Gestión de comentarios


class VistaComentarios(Resource): 
    def get(self, id_comentario):
        try:
            comentario = Comentarios.query.filter_by(id_comentario=id_comentario).first()
            if not comentario:
                return {"mensaje": "comentario no encontrado o no válido."}, 404

            comentario_serializado = {
                "id_comentario": comentario.id_comentario,
                "id_usuario": comentario.id_usuario,
                "comentario": comentario.comentario,
                "comnot": comentario.comnot
            }
            return jsonify({"comentario": comentario_serializado})
        except Exception as e:
            return {"mensaje": f"Error al obtener el comentario: {str(e)}"}, 500

    def patch(self, id_comentario):
        try:
            comentario = Comentarios.query.filter_by(id_comentario=id_comentario).first()
            if not comentario:
                return {"mensaje": "Comentario no encontrado o no válido."}, 404
            return {"mensaje": "Comentario modificado exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al modificar el comentario: {str(e)}"}, 500


# ----------------------- Gestión de calificaciones


class VistaCalificacion(Resource): 

    def get(self, id_calificacion):
        try:
            # Buscar al usuario con id_usuario y con rol 3 (empleado)
            calificacion = calificacion.query.filter_by(id_calificacion=id_calificacion,).first()

            if not calificacion:
                return {"mensaje": "calificacion no encontrada o no válida."}, 404

            # Serializar los datos del calificacion
            calificacion_serializado = {
                "id_calificacion": calificacion.id_calificacion,
                "numerodecalificacion": calificacion.numerodecalificacion,
                "id_usuario": calificacion.id_usuario,
                "calinoti": calificacion.calinoti
            }

            return jsonify({"calificacion": calificacion_serializado})

        except Exception as e:
            return {"mensaje": f"Error al obtener el calificacion: {str(e)}"}, 500

    # Modificar calificacion
def patch(self, id_calificacion):
    try:
        calificacion = Calificacion.query.filter_by(id_calificacion=id_calificacion).first()

        if not calificacion:
            return {"mensaje": "Calificacion no encontrada o no válida."}, 404

        return {"mensaje": "Calificacion modificada exitosamente."}, 200
    except Exception as e:
        return {"mensaje": f"Error al modificar la calificacion: {str(e)}"}, 500

# ----------------------- Gestión de admin


# Modificar admin
    def put(self, id_admin):
        try:
            # Buscar el admin por ID
            admin = Admin.query.filter_by(id_admin=id_admin).first()
            if not admin:
                return {"mensaje": "admin no encontrado o no válido."}, 404

            # Actualizar los campos del admin si están presentes en la solicitud
            admin.nombre = request.json.get("nombre", admin.nombre)
            admin.correo = request.json.get("correo", admin.correo)

            # Actualizar la contraseña si está presente
            if request.json.get("contrasena"):
                admin.contrasena = request.json["contrasena"]

            db.session.commit()

            return {
                "mensaje": "admin actualizado exitosamente.",
                "admin": {
                    "id_admin": admin.id_admin,
                    "nombre": admin.nombre,
                    "correo": admin.correo
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el admin: {str(e)}"}, 500

