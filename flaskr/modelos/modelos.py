from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column('password', db.String(255), nullable=False)  # Almacena el hash de la contraseña

    # Propiedad para el setter de la contraseña
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # Setter para asignar la contraseña
    @password.setter
    def password(self, password):
        self.password = generate_password_hash(password)

    # Método para verificar la contraseña
    def verify_password(self, password):
        return check_password_hash(self.password, password)
        


class Noticias(db.Model):
    id_noticia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    diapublicacion = db.Column(db.Date)

class Comentarios(db.Model):
    id_comentario = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(50))
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))  # Match the type to Integer
    usuario = db.relationship('Usuario', backref='comentarios')

class Calificacion(db.Model):
    id_calificacion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_noticia = db.Column(db.Integer, db.ForeignKey('noticias.id_noticia'))
    numero_de_calificacion = db.Column(db.Integer)
    calinoti = db.relationship('Noticias', backref='calificaciones')

class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15))
    correo = db.Column(db.String(20))
    contrasena_hash = db.Column(db.String(50))

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class NoticiasSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Noticias
        include_relationships = True
        load_instance = True

class ComentariosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comentarios
        include_relationships = True
        load_instance = True

class CalificacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Calificacion
        include_relationships = True
        load_instance = True

class AdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        include_relationships = True
        load_instance = True