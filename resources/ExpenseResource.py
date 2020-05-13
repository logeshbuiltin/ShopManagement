
import sqlite3
import json
from datetime import datetime
from flask_restful import Resource,reqparse
from models.ExpenseModel import ExpenseModel

class ExpenseResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('purchaseType')
    parser.add_argument('entryAmount')
    parser.add_argument('description')
    parser.add_argument('purchaseDate')
    parser.add_argument('userId')

    def get(self, _id):
        item = ExpenseModel.find_by_id(_id)
        if item:
            return item.json()
        else:
            return {"item": "Not Found"}
    
    def post(self, _id):
        data = ExpenseResource.parser.parse_args()
        y, m, d = data['purchaseDate'].split('-')
        entryDate = datetime(int(y), int(m), int(d)).isoformat()
        item = ExpenseModel(
            data['purchaseType'],
            data['entryAmount'],
            data['description'],
            entryDate,
            data['userId']
        )
        try:
            item.save_to_db()
        except Exception as error:
            print (error)

        return item.json(), 201

    def put(self, _id):
        data = ExpenseResource.parser.parse_args()
        y, m, d = data['purchaseDate'].split('-')
        entryDate = datetime(int(y), int(m), int(d)).isoformat()
        item = ExpenseModel.find_by_id(_id)
        if item:
            item.purchase_date = entryDate
            item.purchase_type = data['purchaseType']
            item.entry_amount = data['entryAmount']
            item.description = data['description']
            item.user_id = data['userId']

            item.save_to_db()
        else:
            return {"item": "Not Found"}
        
        return item.json(), 201 if item else 404

    def delete(self, _id):
        item = ExpenseModel.find_by_id(_id)
        if item:
            item.delete_from_db()

        return {"item": "Deleted Successfully"}


class ItemsByUser(Resource):
    def get(self, userId):
        return ExpenseModel.find_by_userid(userId)

class ItemsByType(Resource):
    def get(self,  purchaseType, userId):
        return ExpenseModel.find_by_type(purchaseType, userId)

