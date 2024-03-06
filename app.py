#Importar base de datos y sistema operativo
from db import db
import os

#Importar flask y flask_smorest
from flask import Flask	
from flask_smorest import APISpecMixin
from flask_smorest import Api	
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_migrate import Migrate

#Importar modelos
import models
from models.jwtModel import JwtModel

#Importar recursos
from resources.storeResource import blp as storeBlueprint
from resources.itemResource import blp as itemBlueprint
from resources.tagResource import blp as tagBlueprint
from resources.userResource import blp as userBlueprint

#importar blocklist

from blocklist import BLOCKLIST


#CREAR APP DENTRO DE UNA FUNCION

def create_app(db_url=None):

#Esta instancia de Flask se utiliza para crear servidores web, REST APIs y otras aplicaciones web utilizando el framework Flask.
        app= Flask(__name__) 

        #configurando la REST API
        app.config["PROPAGATE_EXCEPTIONS"] = True    # Configuración para propagar excepciones no manejadas por defecto
        app.config["API_TITLE"] = "Stores REST API"  # Título de la API
        app.config["API_VERSION"] = "v1"             # Versión de la API
        app.config["OPENAPI_VERSION"] = "3.0.3"      # Versión de OpenAPI


        # Configuración para la documentación OpenAPI
        app.config["OPENAPI_URL_PREFIX"] = "/"                      # Prefijo de la URL para la documentación OpenAPI
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"       # Ruta para la interfaz de usuario de Swagger
        app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # URL de Swagger UI

        # Configuración de la base de datos
        app.config["SQLALCHEMY_DATABASE_URI"]=  db_url or os.getenv("DATABASE_URL","sqlite:///data.db")  # Configuración de la URI de la base de datos
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False                                              # Desactivación del seguimiento de modificaciones de SQLAlchemy
        db.init_app(app)                                                                                 # Inicialización de la bade de datos

        #Configuracion de migraciones
        migrate=Migrate()
        migrate.init_app(app,db)

        # Api es una clase que la provee flask_smorest, esta permite traer todos los blueprints y registrarlos en la API
        api= Api(app)

        # Configuración de JWT y manejo de errores
        app.config["JWT_SECRET_KEY"] = "super-secret"  # Clave secreta para crear JWT desde el servidor, Sirve para firmar los tokens
        jwt = JWTManager(app)                         # Inicialización de JWT


        #sobre logout y blocklist:
        #Las lineas de codigo sigueintes son importantes, ya que se utiliza blocklist por si un usuario cierra sesion antes que su JWT expire
        #se manda el token a  lista de token que no pueden ser usados.Se manda el id del token a la lista de bloqueo
        
        #Se verifica si el token esta en la lista  de bloqueo (ha sido revocado)\


        @jwt.token_in_blocklist_loader
        def chek_if_token_in_blockTable(jwt_header: dict , jwt_payload:dict)->bool:

                get_jti=jwt_payload["jti"]

                
                token= models.JwtModel.query.filter(models.JwtModel.jti==get_jti).first()

                return token is not None


        #Se maneja el error cuando el token ha sido revocado
        @jwt.revoked_token_loader
        def revoked_token_callback(jwt_header, jwt_payload):

                # Respuesta indicando que el token ha sido revocado
                return(
                        jsonify(
                        {
                                "message":"The token has been revoked.", 
                                "error":"token_revoked"
                        }
                        )
                ), 401
        

        @jwt.needs_fresh_token_loader
        def token_not_fresh_callback(jwt_header, jwt_payload):
                return(
                        jsonify(
                        {
                                "message":"The token is not fresh.", 
                                "error":"fresh_token_required"
                        }
                        )
                ), 401
        
        #Se maneja el error cuando el token ha expirado
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
                return(
                        jsonify(
                        {
                                "message":"The token has expired.", 
                                "error":"token_expired"
                        }
                        )
                ), 401

        #Se maneja el error cuando el token es invalido
        @jwt.invalid_token_loader
        def invalid_token_callback(error):

                return(
                        jsonify(
                        {
                                "message":"Signature verifications failed.", 
                                "error":"invalid_token"
                        }
                        )
                ), 401
        
        #Se maneja el error cuando el token no esta presente
        @jwt.unauthorized_loader
        def missing_toke_callback(error):
                return(
                        jsonify(
                                {
                                        "mesage":"Request does not contain an access token.", 
                                        "error":"authorization_required"
                                }
                        )
                ),401


        # # Crear la base de datos si no existe
        # with app.app_context():
        #         db.create_all()
                

        # Registrar blueprints (patrones de rutas) para diferentes partes de la API
        api.register_blueprint(storeBlueprint)  # Blueprint para el manejo de tiendas
        api.register_blueprint(itemBlueprint)   # Blueprint para el manejo de items
        api.register_blueprint(tagBlueprint)    # Blueprint para el manejo de tags
        api.register_blueprint(userBlueprint)   # Blueprint para el manejo de usuarios

        return app