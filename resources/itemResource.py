

#importar db,modelos,esquemas,abort y Blueprint,MethodView,sqalchemyError y jwt_required
from db import db
from models.itemModels import ItemModel
from Schemas.itemSchema import ItemSchema, ItemUpdateSchema
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required


#Crear un blueprint para manejar las rutas relacionadas con los items
blp= Blueprint("item",__name__, description="Operations on items")


#ruta para manejar las operaciones relacionadas con un item
@blp.route("/item/<int:item_id>")

class Item(MethodView):

    #Obtener un item por su id
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,item_id):
    
        item= ItemModel.query.get_or_404(item_id)
        return item

    #eliminar un item por su id
    @jwt_required()
    def delete(self,item_id):
        item= ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
    
    #Actualizar un item por su id
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):

        item= ItemModel.query.get(item_id)
        if item:
            
            item.price=item_data["price"]
            item.name=item_data["name"]

        else: 
            item= ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item
    

#ruta para manejar las operaciones relacionadas con todos los items
@blp.route("/item")
class ItemList(MethodView):

    #Obtener todos los items
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    


    #Crear un nuevo item
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        item=ItemModel(**item_data)

        try: 
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500,description="An error occured while adding the item to the database")
            
        return item,201