# Scope-ML

This repository contains all the relevant code for the machine learning pipeline in scope. This includes a *Qdrant* database, a *FastAPI* server with *Celery* workers using *Redis*, and a worker dashboard using *Flower*.

## Fetching Data
To grab the data from the GEF project database, use the `download_files.py` script in the `data` directory. Updating `projects.csv` with a more recent version from the [gef website](https://www.thegef.org/projects-operations/database)

