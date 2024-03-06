#Este archivo contiene los recursos para manejar las etiquetas.

#Las etiquetas son una forma de categorizar los elementos. Cada etiqueta está asociada con una tienda y puede estar vinculada a varios elementos.

#importar base de datos,modelos,esquemas,abort y Blueprint,MethodView y SQLAlchemyError
from db import db
from models import TagModel,StoreModel,ItemModel
from Schemas.tagSchema import TagSchema ,TagAndItemSchema
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError


#Crear un blueprint para manejar las rutas relacionadas con las etiquetas

blp=Blueprint("Tags", __name__, description="Operations on tags")


#Ruta para manejar operaciones para etiqueta asociada con una tienda
@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    
    #Obtener todas las etiquetas asociadas con una tienda
    @blp.response(200, TagSchema(many=True))
    def get(self,store_id):
        store= StoreModel.query.get_or_404(store_id)

        return store.tags.all()
    

    #Crear una nueva etiqueta asociada con una tienda
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        
        tag=TagModel(**tag_data,store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(500,description=str(e))

        return tag


# ruta para manejar operaciones para etiqueta asociada con un elemento
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):

    #Crear una etiqueta asociada con un elemento
    def post(self, item_id,tag_id):
        item= ItemModel.query.get_or_404(item_id)
        tag= TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,description="Error linking tags to item")


    #Eliminar una etiqueta asociada con un elemento
    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,description="Error unlinking tags to item")

        return {"message":"Tag unlinked from item","item":item,"tag":tag}



#ruta para manejar operaciones para una etiqueta
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):

    #Obtener una etiqueta
    def get(self,tag_id):
        tag= TagModel.query.get_or_404(tag_id)
        return tag 
    
    #eliminar una etiqueta
    def delete(self,tag_id):
        tag= TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted"}
        
        abort(400,description="Tag has items linked to it")