# ConceptTrackr

This repository aims to be an all-in-one tool to index and search a
document database for the occurrence frequency and relevant context of
different concepts such as socioeconomic issues in a database of
environmental projects.

## Main Sub-problems:

1. Creation of vector database optimally from document store
2. Efficient search for conceptual occurrences
    1. Caching / Storing this information for later use in 3.)
3. Extracting most common contexts for a given concept
    1. Aggregating all individual document contexts into one all encompassing context

## Commands

- Run Backend: `python run_backend.py`
- Run Celery Worker: `celery --app=backend.tasks.celery worker --loglevel=INFO`
- Run Flower (celery): `celery --app=backend.tasks.celery flower --loglevel=INFO`
- Run frontend (from frontend directory): `npm run dev`