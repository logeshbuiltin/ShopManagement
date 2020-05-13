import sqlite3
from dataFiles.dbFile import dataB


class UserModel(dataB.Model):

    __tablename__ = 'users'

    id = dataB.Column(dataB.Integer, primary_key=True)
    username = dataB.Column(dataB.String(80))
    password = dataB.Column(dataB.String(80))
    firstname = dataB.Column(dataB.String(80))
    lastname = dataB.Column(dataB.String(80))
    email_id = dataB.Column(dataB.String(80))
    phone_no = dataB.Column(dataB.Integer)
    shop_id = dataB.Column(dataB.Integer)
    is_admin = dataB.Column(dataB.Boolean, default=False)
    is_active = dataB.Column(dataB.Boolean, default=True)

    def __init__(self, username, password, firstname, lastname, emailId, phoneNo):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email_id = emailId
        self.phone_no = phoneNo


    def json(self):
        return {
            "id": self.id,
            "username": self.username, 
            "password": self.password, 
            "firstname": self.firstname, 
            "lastname": self.lastname, 
            "emailId": self.email_id, 
            "phoneNo": self.phone_no
        }

    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    

    @classmethod
    def find_by_uerid(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def save_to_db(self):
        dataB.session.add(self)
        dataB.session.commit()

    def delete_from_db(self):
        dataB.session.delete(self)
        dataB.session.commit()