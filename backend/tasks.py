from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"


@celery.task(name="add")
def add(x=1, y=5):
    return x + y
