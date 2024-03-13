from db import db

#los modelos nos ayudaban a mapear la base de datos a objetos de python, para poder manipular
#la base de datos como si fueran objetos de python


#Modelo de la tabla tags
class TagModel(db.Model):

    #nombre de la tabla
    __tablename__="tags"

    #columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)
    store_id=db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    #relacionar dos tablas, traerse toda la informacion de la otra tabla (como un join)
    store=db.relationship("StoreModel", back_populates="tags")
    items= db.relationship("ItemModel",back_populates="tags",secondary="item_tags")
