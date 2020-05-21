import sqlite3
from flask_restful import Resource,reqparse
from models.UserModel import UserModel

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="Username field can not be empty"
    )
    parser.add_argument("password",
        type=str,
        required=True,
        help="password field can not be empty"
    )
    parser.add_argument("firstname",
        type=str,
        help="user name is required"
    )
    parser.add_argument("lastname",
        type=str,
        help="user name is required"
    )
    parser.add_argument("emailId",
        type=str,
        help="email field of the user"
    )
    parser.add_argument("phoneNo",
        type=str,
        help="phone number field of the user"
    )
    parser.add_argument("currCode",
        type=str,
        help="Currency Code field of the user"
    )


    def get(self, username):
        user_data = UserModel.find_by_username(username)
        if user_data:
            return user_data.json()
        else:
            return ("message", f"{username} not found in the database"), 201


    def post(self, username):
        data = UserResource.parser.parse_args()
        user = UserModel.find_by_username(username)
        if user:
            return {"registration": "exists"}, 201
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {"registration": "success"}, 201


    def put(self, username):
        data = UserResource.parser.parse_args()
        user = UserModel.find_by_uerid(username)
        if user:
            user.username = data["username"]
            user.password = data["password"]
            user.firstname = data["firstname"]
            user.lastname = data["lastname"]
            user.email_id = data["emailId"]
            user.phone_no = data["phoneNo"]
            user.curr_code = data["currCode"]    

            user.save_to_db()       
        else:
            return {"error": "failed", "reason": "User not found"}
           # user = UserModel(**data)
    
        return user.json(), 201 if user else 401
        

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {"deletion": "success"}
        else:
            return {"deletion": "user not found"}
