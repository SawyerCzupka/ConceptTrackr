from celery import Celery
from celery.app import task
from dotenv import load_dotenv

from utils import gef_from_env
from gef_analyzr import GEFAnalyzer
import os

celery = Celery(
    "celery_tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)


class GEFTask(celery.Task):
    _gef: None | GEFAnalyzer = None
    _increment: None | int = None

    @property
    def gef(self) -> GEFAnalyzer:
        if self._gef is None:
            self._initGEF()
        return self._gef

    @property
    def increment(self):
        if self._increment is None:
            self._increment = 1
            return self._increment

        self._increment += 1
        return self._increment

    def _initGEF(self):
        print(f"-- DIRECTORY: {os.listdir(os.getcwd())}")
        self._gef = gef_from_env()


@celery.task(name="add")
def add(x=1, y=5):
    return x + y


@celery.task(base=GEFTask, bind=True, name="GEF Test")
def gefTest(self: task):
    self.gef.countOccurrences()
    return self.increment


if __name__ == "__main__":
    worker = celery.Worker(
        include=['']
    )
    celery.start(['worker', '-A', 'celery_tasks'])
