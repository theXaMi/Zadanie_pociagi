from celery import Celery

app = Celery('db',broker='amqp://localhost')

if __name__=="__main__":
    print("123124214346457564353464574646")