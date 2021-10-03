import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from time import sleep

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
database = os.environ["POSTGRES_DB"]
port = os.environ["POSTGRES_PORT"]

sleep(3) # wait for db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 10
app.config["MAX_OVERFLOW"] = 20
db = SQLAlchemy(app)

class Stacja(db.Model):
    __tablename__ = "stacje"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Stacja %r>" % self.name
    
class Szlaban(db.Model):
    __tablename__ = "szlabany"
    id = db.Column(db.Integer,primary_key=True)
    open = db.Column(db.Boolean)
    last = db.Column(db.DateTime)
    #station = db.relationship("Stacja", backref=db.backref("szlaban", lazy=True))

    def __repr__(self):
        return "<Szlaban id %i>" % self.id