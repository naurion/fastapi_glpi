FROM python:3.11

RUN mkdir fastapi_glpi

WORKDIR /fastapi_glpi

COPY /pyproject.toml /fastapi_glpi

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN chmod a+x docker/*.sh