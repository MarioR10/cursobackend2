#Este archivo contiene los recursos para manejar las tiendas.

#importar db,modelos,esquemas,abort y Blueprint,MethodView,sqalchemyError,IntegrityError
from db import db
from models.storeModels import StoreModel
from Schemas.storeSchema import StoreSchema
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError



#Crear un blueprint para manejar las rutas relacionadas con las tiendas
blp= Blueprint("store",__name__, description="Operations on stores")


#ruta para manejar las operaciones relacionadas con una tienda
@blp.route("/store/<int:store_id>")
class Store(MethodView):

    #Obtener una tienda por su id
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store= StoreModel.query.get_or_404(store_id)
        return store
    
    #eliminar una tienda por su id
    def delete(self,store_id):
        store= StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}



#ruta para manejar las operaciones relacionadas con todas las tiendas 
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):

        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):

        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        
        except IntegrityError:
            abort(400,description="The store already exists")

        except SQLAlchemyError:
            abort(500,description="Error in the database")
        
        
        return store,201
