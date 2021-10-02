from flask import Flask
from celery import Celery
from werkzeug.debug import DebuggedApplication


CELERY_TASK_LIST: list[str] = [
    "pociagi.droznik.tasks",
    "pociagi.droznik.droznik",
    "pociagi.centrala.centrala",
    "pociagi.pociag.pociag",
]

def create_app() -> Flask:
    app = Flask(__name__,static_folder="../public",static_url_path="")
    app.config.from_object("config.settings")

    # register pages here


    app.app_context().push()

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app

def create_celery_app(app: Flask=None) -> Celery:
    app = app or create_app()
    celery=Celery(app.import_name,broker=app.config["CELERY_BROKER_URL"],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self,*args,**kwargs):
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)

    celery.Task = ContextTask
    return celery