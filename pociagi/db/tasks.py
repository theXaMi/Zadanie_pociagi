from pociagi.app import create_celery_app
from flask_sqlalchemy import SQLAlchemy
from .models import db

celery = create_celery_app()

@celery.task()
def test():
    print("hello")

@celery.task()
def get_all(model: SQLAlchemy):
    data = model.query.all()
    return data

@celery.task()
def add_instance(model: SQLAlchemy, **kwargs) -> None:
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()

@celery.task()
def delete_instance(model: SQLAlchemy, id: int) -> None:
    model.query.filter_by(id=id).delete()
    commit_changes()

@celery.task()
def edit_instance(model: SQLAlchemy, id: int, **kwargs) -> None:
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs:
        setattr(instance, attr, new_value)
    commit_changes()

def commit_changes():
    db.session.commit()