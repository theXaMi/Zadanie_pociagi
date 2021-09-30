from celery import Celery

mq = Celery('db',broker='amqp://localhost')

def celery_listener():
    pass

if __name__=="__main__":
    celery_listener()


