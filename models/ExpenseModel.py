
import sqlite3
from dataFiles.dbFile import dataB
from sqlalchemy import cast, Date
from datetime import datetime, timedelta


class ExpenseModel(dataB.Model):

    __tablename__ = 'expenses'

    id = dataB.Column(dataB.Integer, primary_key=True)
    purchase_type = dataB.Column(dataB.String(100))
    entry_amount = dataB.Column(dataB.Float)
    description = dataB.Column(dataB.String(300))
    purchase_date = dataB.Column(dataB.String(20))
    purchase_day = dataB.Column(dataB.String(20))
    added_by = dataB.Column(dataB.String(20))
    curr_code = dataB.Column(dataB.String(10))
    user_id = dataB.Column(dataB.Integer, dataB.ForeignKey('users.id'))

    user = dataB.relationship('UserModel')

    def __init__(self, purchase_type, entry_amount, description, purchase_date, purchase_day, added_by, curr_code, user_id):
        self.purchase_type = purchase_type
        self.entry_amount = entry_amount
        self.description = description
        self.purchase_date = purchase_date
        self.purchase_day = purchase_day
        self.added_by = added_by
        self.curr_code = curr_code
        self.user_id = user_id


    def json(self):
        return {
            "id": self.id,
            "purchaseType": self.purchase_type, 
            "entryAmount": self.entry_amount, 
            "description": self.description, 
            "purchaseDate": self.purchase_date,
            "purchaseDay": self.purchase_day,
            "addedBy": self.added_by,
            "currCode": self.curr_code,
            "userId": self.user_id
        }

    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_userid(cls, userId):
        item_list = cls.query.filter_by(user_id=userId).all()
        return {"items": list(map(lambda x: x.json(), item_list))}


    @classmethod
    def find_by_type(cls, purchaseType, userId):
        item_list = cls.query.filter_by(purchase_type=purchaseType).filter_by(user_id=userId).all()
        return {"items": list(map(lambda x: x.json(), item_list))}

    @classmethod
    def find_by_date(cls, fromDate, toDate, userId):
        start_date = datetime.strptime(fromDate, '%Y-%m-%d').date()
        end_date = datetime.strptime(toDate, '%Y-%m-%d').date()
        end_date = end_date + timedelta(days=1)
        item_list = cls.query.filter_by(user_id=userId).filter(cls.purchase_date>=start_date).filter(cls.purchase_date<=end_date).all()
        return {"items": list(map(lambda x: x.json(), item_list))}


    def save_to_db(self):
        dataB.session.add(self)
        dataB.session.commit()


    def delete_from_db(self):
        dataB.session.delete(self)
        dataB.session.commit()

