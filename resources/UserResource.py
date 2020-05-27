import sqlite3
from flask_restful import Resource,reqparse
from models.UserModel import UserModel
from services.MailService import MailService

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
    parser.add_argument("favorite",
        type=str,
        help="favorite field of the user"
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
            subject = "No-Reply: ExpenseHandler - Account creation successful."
            keyWord = "register"
            MailService.sendEmail(data["emailId"], subject, data["firstname"], keyWord, data["password"])
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

            subject = "No-Reply: ExpenseHandler - Account updation successful."
            keyWord = "update"  
            MailService.sendEmail(data["emailId"], subject, data["firstname"], keyWord, data["password"])
        else:
            return {"error": "failed", "reason": "User not found"}
           # user = UserModel(**data)
    
        return user.json(), 201 if user else 401
        

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            subject = "No-Reply: ExpenseHandler - Account deletion successful."
            keyWord = "delete"  
            MailService.sendEmail(user.emailId, subject, user.firstname, keyWord, user.password)
            user.delete_from_db()
            return {"deletion": "success"}
        else:
            return {"deletion": "user not found"}


class forgetPass(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="Username field can not be empty"
    )
    parser.add_argument("favorite",
        type=str,
        required=True,
        help="favorite field can not be empty"
    )

    def post(self):
        data = forgetPass.parser.parse_args()
        user = UserModel.find_by_userfav(data["username"], data["favorite"])

        if user:
            subject = "No-Reply: ExpenseHandler - User password details."
            keyWord = "passchange"  
            MailService.sendEmail(user.email_id, subject, user.firstname, keyWord, user.password)
            return {"link": "sent"}
        else:
            return {"link": "error"}


