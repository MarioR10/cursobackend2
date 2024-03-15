import email
from db import db

#los modelos nos ayudaban a mapear la base de datos a objetos de python, para poder manipular
#la base de datos como si fueran objetos de python


#Modelo de la tabla ususario
class UserModel(db.Model):
    __table__name = "users"

    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(80), unique=True, nullable=False)
    email= db.Column(db.String, unique=True, nullable=False)
    password= db.Column(db.String(300), unique=True, nullable=False)