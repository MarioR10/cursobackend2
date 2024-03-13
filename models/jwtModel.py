from db import db

#los modelos nos ayudaban a mapear la base de datos a objetos de python, para poder manipular
#la base de datos como si fueran objetos de python

#Modelo de la tabla jwt

class JwtModel(db.Model):

    #nombre de la tabla

    __name__="BlockTable"

    #columnas de la tabla
    id= db.Column(db.Integer, primary_key=True)
    jti= db.Column(db.String(80),nullable=False)



