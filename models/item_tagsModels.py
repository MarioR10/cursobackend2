#Tabla intermedia entre items y tags rompe la relacion muchos a muchos

#los modelos nos ayudaban a mapear la base de datos a objetos de python, para poder manipular
#la base de datos como si fueran objetos de python


from db import db

#modelo de la tabla item_tags
class ItemTags(db.Model):
    
    __tablename__="item_tags"

    #Columnas de la tabla
    id=db.Column(db.Integer, primary_key=True)
    item_id=db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id=db.Column(db.Integer, db.ForeignKey("tags.id"))




