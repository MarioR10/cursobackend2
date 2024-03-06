# Este archivo contiene el esquema para tiendas. Se utiliza para validar, serializar y deserializar

#Importar el modulo Schema de marshmallow
from marshmallow import Schema, fields

#Esquema para  tiendas
#Contiene la información básica de la tienda, sin incluir información adicional o relaciones complejas con otros modelos.

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name= fields.Str(required=True)


# Extiende PlainStoreSchema para incluir información adicional, como los artículos y etiquetas asociados con la tienda.
class StoreSchema(PlainStoreSchema):
    
    
    from Schemas.tagSchema import PlainTagSchema
    from Schemas.itemSchema import PlainItemSchema


    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)


