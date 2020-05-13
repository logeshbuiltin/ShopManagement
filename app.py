from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS, cross_origin
from security import authenticate, identity
from dataFiles.dbFile import dataB
from resources.UserResource import UserResource
from resources.ExpenseResource import ExpenseResource, ItemsByType, ItemsByUser


app = Flask(__name__)
cors = CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DataFile.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = "shopApp"

@cross_origin()
@app.before_first_request
def create_tables():
    dataB.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(UserResource, "/register/user/<string:username>")

api.add_resource(ExpenseResource, "/item/<string:_id>")

api.add_resource(ItemsByType, "/items/type/<string:purchaseType>/<string:userId>")

api.add_resource(ItemsByUser, "/items/user/<string:userId>")

if __name__ == '__main__':
    dataB.init_app(app)
    app.run(port=5000, debug=True)