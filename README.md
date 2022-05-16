# family-budget-backend

[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Backend for managing family budget.

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

Dump database data
```bash
docker-compose exec postgres pg_dump -U family-budget family-budget > dump_data.dump
```

Load database data dump
```bash
docker-compose exec -T postgres psql -U family-budget family-budget < [directory to dump]/dump_data.dump
```
