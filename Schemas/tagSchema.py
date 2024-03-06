# Este archivo contiene el esquema de etiquetas. Se utiliza para validar, serializar y deserializar


# importar el modulo Schema de marshmallow
from marshmallow import Schema, fields

#Esquema para etiquetas
#Contiene la información básica del Tag, sin incluir información adicional o relaciones complejas con otros modelos.

class PlainTagSchema(Schema):
    id= fields.Int(dump_only=True)
    name=fields.Str()

# Extiende PlainTagSchema para incluir información adicional y relaciones complejas con otros modelos, como la tienda a la que pertenece y los artículos asociados.

class TagSchema(PlainTagSchema):
    
    from Schemas.storeSchema import PlainStoreSchema
    from Schemas.itemSchema import PlainItemSchema
    store_id= fields.Int(load_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    

# Esquema para la relación entre etiquetas y elementos
    
class TagAndItemSchema(Schema):
    
    from Schemas.itemSchema import ItemSchema
    message= fields.Str()
    item=fields.Nested(ItemSchema)
    tag=fields.Nested(TagSchema)

