#Este archivo contiene los recursos para manejar los usuarios.


#Importar base de datos,modelos,esquemas,abort y Blueprint,MethodView,pbkdf2_sha256 y create_access_token,jwt_required,get_jwt
#create_refresh_token,BLOCKLIST, get_jwt_identity

from db import db
from models import UserModel,JwtModel
from Schemas.userSchema import UserSchema
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt, get_jwt_identity
from blocklist import BLOCKLIST
# from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp=Blueprint("Users", __name__, description="Operations on users")

#Ruta para manejar operaciones para registrar un usuarios
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):

        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(409,description="The user already exists")

        user= UserModel(

            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created"},201
    

@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
            user= UserModel.query.filter(UserModel.username==user_data["username"]).first()

            if user and pbkdf2_sha256.verify(user_data["password"],user.password):

                # Cuando un usuario inicia sesión, se emiten dos tokens distintos:
                # 1. Token de Acceso (Access Token): Se utiliza para autenticar solicitudes del usuario.
                # 2. Refresh Token: Se utiliza exclusivamente para obtener un nuevo Access Token una vez que el original expire.
                access_token=create_access_token(identity=user.id)
                refresh_token= create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            
            abort(401,description="Invalid credentials")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user= get_jwt_identity()
        new_token=create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}











#Ruta para manejar operaciones para cerrar sesion
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):

        # Obtener el identificador único del token JWT actual
        get_jti= get_jwt()["jti"]
        jti_model= JwtModel(jti=get_jti)

        try:
            db.session.add(jti_model)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(500,description="Error logging out")

        # Respuesta indicando que el usuario ha cerrado sesión exitosamente
        return {"message": "User logged out"},200


#Ruta para obtener un usuario por su id y eliminar un usuario por su id
    @blp.route("/user/<int:user_id>")
    class User(MethodView):
        @blp.response(200,UserSchema)
        def get(self,user_id):
            user=UserModel.query.get_or_404(user_id)
            return user
        
        def delete(self,user_id):
            user= UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"},200