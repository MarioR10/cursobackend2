# Este archivo contiene el esquema para ususarios. Se utiliza para validar, serializar y deserializar

#Importar el modulo Schema de marshmallow
from marshmallow import Schema, fields

class UserSchema(Schema):

    id= fields.Int(dump_only=True)
    username= fields.Str(required=True)
    password= fields.Str(required=True,load_only=True)
