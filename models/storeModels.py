from db import db

#los modelos nos ayudaban a mapear la base de datos a objetos de python, para poder manipular
#la base de datos como si fueran objetos de python

#Modelo de la tabla stores
class StoreModel(db.Model):

    #nombre de la tabla
    __tablename__="stores"

    #columnas de la tabla

    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)

    #relacionar dos tablas, traerse toda la informacion de la otra
    items= db.relationship("ItemModel",back_populates="store",lazy="dynamic", cascade="all, delete")  
    tags= db.relationship("TagModel",back_populates="store",lazy="dynamic")  


    