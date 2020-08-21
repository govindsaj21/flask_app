from flask_restful import reqparse,Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type = float,
        required = True,
        help = "This is a required field")
    parser.add_argument("store_id",
        type = int,
        required = True,
        help = "This is a required field")

    @jwt_required()
    def get(self,name):
        item =ItemModel.get_by_name(name)
        if item:
            return item.json()
        return {"message":"No items found with the given name"},404

    def post(self,name):
        if ItemModel.get_by_name(name):
            return {"message":f"An item with the {name} already exists"}
        data = Item.parser.parse_args()
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {"message":"An error occured while insertion"},500 ## internal server occured
        return item.json(),201

    def delete(self,name):
        item = ItemModel.get_by_name(name)
        if item:
            item.delete_from_db()
        return {"message" : "Deletion succesfull"}

    @jwt_required()
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.get_by_name(name)
        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data["price"]
        item.save_to_db()

        return item.json()



class Items(Resource):

    def get(self):
        return {"items":[item.json() for item in ItemModel.query.all()]}
