FROM python:3.11-slim as dev

ARG APP_USER=sobesity\
    APP_GROUP=sobesity\
    CODE_FOLDER=/code

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH=$CODE_FOLDER \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1

RUN apt-get update && \
    apt-get install -y --no-install-recommends\
    netcat \
    libpq-dev python-dev gcc && \
    rm -rf /var/lib/apt/lists/*

ENV APP_HOME=/home/$APP_USER

WORKDIR $CODE_FOLDER

RUN groupadd $APP_GROUP && \
    useradd -m -s /bin/bash -g $APP_GROUP $APP_USER && \
    chown -R $APP_USER:$APP_GROUP $APP_HOME && \
    chown -R $APP_USER:$APP_GROUP $CODE_FOLDER

USER $APP_USER
ENV PATH="$PATH:$APP_HOME/.local/bin"

RUN pip install -U pip && pip install "poetry==$POETRY_VERSION"


COPY --chown=$APP_USER ./poetry.lock ./pyproject.toml ./tox.ini ./
RUN poetry config virtualenvs.in-project true && poetry install

COPY ./etc/backend/wait-for-it.sh ./etc/backend/entrypoint.sh  /entr/

COPY --chown=$APP_USER ./src ./

ENTRYPOINT ["/entr/entrypoint.sh"]

CMD ["gunicorn", "--reload", "-b", "0.0.0.0:5150", "--timeout", "120", "sobesity.webapp:create_app()"]

FROM dev as migrator

CMD ["alembic", "upgrade", "head"]
