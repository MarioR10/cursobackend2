from db import db

#los modelos nos ayudaban a mapear la base de datos a objetos de python, para poder manipular
#la base de datos como si fueran objetos de python

#Modelo de la tabla items
class ItemModel(db.Model):

    #nombre de la tabla
    __tablename__="items"

    #columnas de la tabla

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)
    price=db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id=db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    descuento= db.Column(db.Float(precision=2), unique=False, nullable=True)

    #relacionar dos tablas, traerse toda la informacion de la otra tabla (como un join)
    store=db.relationship("StoreModel", back_populates="items")
    tags= db.relationship("TagModel",back_populates="items",secondary="item_tags")
