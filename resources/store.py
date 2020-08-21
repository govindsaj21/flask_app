from flask_restful import reqparse,Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self,name):
        store =StoreModel.get_by_name(name)
        if store:
            return store.json()
        return {"message":"No stores found with the given name"},404

    def post(self,name):
        if StoreModel.get_by_name(name):
            return {"message":f"An store with the {name} already exists"}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"An error occured while insertion"},500 ## internal server occured
        return store.json(),201

    def delete(self,name):
        store = StoreModel.get_by_name(name)
        if store:
            store.delete_from_db()
        return {"message" : "Deletion succesfull"}

    @jwt_required()
    def put(self,name):
        store = StoreModel.get_by_name(name)
        if store is None:
            store = StoreModel(name)
        else:
            store.name = name
        store.save_to_db()

        return store.json()



class Stores(Resource):

    def get(self):
        return {"stores":[store.json() for store in StoreModel.query.all()]}
