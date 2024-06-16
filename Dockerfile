# pull official base image
FROM python:3.11-slim-buster

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update 
RUN apt-get install gcc default-libmysqlclient-dev -y

# install python dependencies
RUN pip install --upgrade pip setuptools wheel

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# install project dependencies
COPY pyproject.toml poetry.lock* /usr/src/app/

# Handle mysqlclient as a special case if necessary
# RUN pip wheel --no-cache-dir --use-pep517 "mysqlclient (==2.2.4)"
RUN poetry install --no-dev --no-interaction --no-ansi

# copy entrypoint.sh
COPY ./app/entrypoint.sh /usr/src/app/entrypoint.sh

# ensure entrypoint.sh is executable
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY ./app/ /usr/src/app/

# run entrypoint.sh
CMD ["sh", "/usr/src/app/entrypoint.sh"]