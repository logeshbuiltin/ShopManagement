from app import app
from dataFiles.dbFile import dataB
from flask_cors import cross_origin


dataB.init_app(app)


@cross_origin()
@app.before_first_request
def create_tables():
    dataB.create_all()