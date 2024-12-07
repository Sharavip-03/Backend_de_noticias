from flaskr import create_app
from .modelos import db
from flask_restful import Api
from .vistas import (
    VistaSignIn,
    VistaLogIn,
    VistaUsuario,
    VistaNoticias,
    VistaComentarios,
    VistaCalificacion
)
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = create_app('default')
app_context = app.app_context()
app_context.push()

CORS(app)
db.init_app(app)
db.create_all()

api = Api(app)

# Auth routes
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')

# User routes
api.add_resource(VistaUsuario, '/usuarios/<int:id_usuario>')

# News routes
api.add_resource(VistaNoticias, '/noticias')

# Comments routes
api.add_resource(VistaComentarios, '/comentarios/<int:id_comentario>')

# Ratings routes
api.add_resource(VistaCalificacion, '/calificaciones/<int:id_calificacion>')

jwt = JWTManager(app)