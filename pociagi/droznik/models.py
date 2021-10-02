from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:////droznikdb"
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
    station = db.relationship("Stacja", backref=db.backref("szlaban", lazy=True))

    def __repr__(self):
        return "<Szlaban id %i>" % self.id