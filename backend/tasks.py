from celery import Celery
from celery.app import task
from dotenv import load_dotenv
from gef_analyzr import GEFAnalyzer

celery = Celery(
    "tasks", broker="redis://redis:6379", backend="redis://redis:6379"
)


# celery.conf.broker_url = "redis://localhost:6379"
# celery.conf.result_backend = "redis://localhost:6379"

class GEFTask(celery.Task):
    _gef: None | GEFAnalyzer = None
    _increment: None | int = None

    @property
    def gef(self) -> GEFAnalyzer:
        if self._gef is None:
            self.initGEF()
        return self._gef

    @property
    def increment(self):
        if self._increment is None:
            self._increment = 1
            return self._increment

        self._increment += 1
        return self._increment

    def initGEF(self):
        from backend.app.utils.gef_loader import gef_from_env
        self._gef = gef_from_env()


@celery.task(name="add")
def add(x=1, y=5):
    return x + y


@celery.task(base=GEFTask, bind=True, name="GEF Test")
def gefTest(self: task):
    self.gef.countOccurrences()
    return self.increment
