# pull official base image
FROM python:3.11-slim

# set work directory
WORKDIR /usr/src/main

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ libpq-dev curl ncat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# install project dependencies
COPY pyproject.toml poetry.lock* /usr/src/main/
RUN poetry install --no-dev --no-interaction --no-ansi

# copy entrypoint.sh
COPY ./app/entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY ./app/ /usr/src/app/

# run entrypoint.sh
CMD sh /usr/src/app/entrypoint.sh