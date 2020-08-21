import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type = str,
        required= True,
        help="This field is requierd"
        )

    parser.add_argument("password",
        type = str,
        required= True,
        help="This field is requierd"
        )


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message":"username already exists"}
        user = UserModel(**data)
        user.save_to_db()

        return {"message":"User has been created Succesfully"}
