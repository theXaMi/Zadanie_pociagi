import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Pociag(db.Model):
    __tablename__ = "pociagi"
    id = db.Column(db.Integer,primary_key=True)
    predkosc = db.Column(db.Float)
    stacja = db.Column(db.String(100))

class Szlaban(db.Model):
    __tablename__ = "szlabany"
    id = db.Column(db.Integer,primary_key=True)
    stan = db.Column(db.Boolean)
    ostatnio = db.Column(db.DateTime)