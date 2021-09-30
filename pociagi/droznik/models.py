import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Szlaban(db.Model):
    __tablename__ = "szlabany"
    id = db.Column(db.Integer,primary_key=True)
    stan = db.Column(db.Boolean)
    ostatnio = db.Column(db.DateTime)