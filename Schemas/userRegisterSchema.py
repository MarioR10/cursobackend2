# Este archivo contiene el esquema de registro. Se utiliza para validar, serializar y deserializar


# importar el modulo Schema de marshmallow
from marshmallow import Schema, fields
from   Schemas.userSchema import UserSchema

#Esquema para el registro de usuarios
class UserRegisterSchema(UserSchema):

    email= fields.Email(required=True)