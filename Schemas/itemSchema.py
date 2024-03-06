# Este archivo contiene el esquema para  items. Se utiliza para validar, serializar y deserializar

#Importar el modulo Schema de marshmallow
from marshmallow import Schema, fields





#Esquema para  items
#Contiene la información básica del modelo, sin incluir información adicional o relaciones complejas con otros modelos.
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name= fields.Str(required=True)
    price= fields.Float(required=True)

# Esquema para actualizar item
class ItemUpdateSchema(Schema):
    name= fields.Str()
    price= fields.Float()
    store_id= fields.Int()

# Extiende PlainItemSchema para incluir información adicional, como la tienda y las etiquetas asociadas con el elemento
class ItemSchema(PlainItemSchema):

    from Schemas.storeSchema import PlainStoreSchema
    from Schemas.tagSchema import PlainTagSchema

    store_id=fields.Int(required=True, load_only=True)
    store= fields.Nested(PlainStoreSchema(),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)
