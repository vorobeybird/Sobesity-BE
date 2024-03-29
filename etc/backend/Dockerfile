FROM python:3.11-slim as builder
ARG CODE_FOLDER=/code

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1

RUN apt-get update && \
    apt-get upgrade -qqy && \
    apt-get install -qqy --no-install-recommends\
    libpq-dev gcc

WORKDIR $CODE_FOLDER

RUN pip install -U pip && pip install "poetry==$POETRY_VERSION"
COPY ./poetry.lock ./pyproject.toml  ./
RUN poetry config virtualenvs.in-project true && poetry install

FROM python:3.11-slim as dev

ARG APP_USER=sobesity\
    APP_GROUP=sobesity\
    CODE_FOLDER=/code

ENV PYTHONPATH=$CODE_FOLDER \
    VENV_FOLDER=$CODE_FOLDER/.venv

RUN apt-get update && \
    apt-get upgrade -qqy && \
    apt-get install -y\
    libpq-dev &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR $CODE_FOLDER
RUN groupadd $APP_GROUP && \
    useradd -s /bin/bash -g $APP_GROUP $APP_USER -d $CODE_FOLDER && \
    chown -R $APP_USER:$APP_GROUP $CODE_FOLDER

USER $APP_USER

COPY ./etc/backend/entrypoint.sh  /entr/

COPY --from=builder $VENV_FOLDER $VENV_FOLDER

COPY --chown=$APP_USER ./src ./tox.ini ./pyproject.toml ./etc/backend/run-server.sh ./
RUN chmod +x ./run-server.sh

ENTRYPOINT ["/entr/entrypoint.sh"]

CMD ["./run-server.sh"]

FROM dev as migrator

CMD ["alembic", "upgrade", "head"]
