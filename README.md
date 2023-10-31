# Scope-ML

This repository contains all the relevant code for the machine learning pipeline in scope. This includes a *Qdrant* database, a *FastAPI* server with *Celery* workers using *Redis*, and a worker dashboard using *Flower*.

## Deployment

All the required services can be started using the provided `docker-compose.yml` file in the project root. This uses persistant volumes for the Qdrant database by default.

## Fetching Data

To grab the data from the GEF project database, use the `download_files.py` script in the `data` directory. Updating `projects.csv` with a more recent version from the [gef website](https://www.thegef.org/projects-operations/database).

By default, this downloads all available PDF files to `/data/dumps/`.

## Loading data to Qdrant

At the moment, this functionality is only singlethreaded and would benefit greatly from parallelism. However, attempts to utilize frameworks like Dask give issues with pickling objects between workers.

After the documents are downloaded, use the `import_documents.py` script to import them to Qdrant.