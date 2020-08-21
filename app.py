from flask import Flask
from flask import request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
from resources.user import UserRegister
from resources.item import Item,Items
from security import authenticate,identity
from resources.store import Store,Stores

app  = Flask(__name__)
app.secret_key = 'govind'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app,authenticate,identity)

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Stores,'/stores')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(Items,'/items')
api.add_resource(UserRegister,"/register")


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug = True)
