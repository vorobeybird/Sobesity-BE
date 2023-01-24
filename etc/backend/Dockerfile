FROM python:3.11-buster as dev

ARG APP_USER=sobesity\
    APP_GROUP=sobesity

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1

RUN apt-get update && \
    apt-get install -y \
    netcat \
    libpq-dev python-dev

RUN groupadd $APP_GROUP && useradd -m -s /bin/bash -g $APP_GROUP $APP_USER

ENV APP_HOME=/home/$APP_USER

RUN chown -R $APP_USER:$APP_GROUP $APP_HOME
USER $APP_USER
ENV PATH="$PATH:$APP_HOME/.local/bin"

RUN pip install -U pip && pip install "poetry==$POETRY_VERSION"

WORKDIR /code

COPY --chown=$APP_USER ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.in-project true && poetry install

COPY ./etc/backend/wait-for-it.sh ./etc/backend/entrypoint.sh  ./

COPY src tox.ini ./

ENTRYPOINT ["./entrypoint.sh"]

CMD ["uwsgi", "--py-autoreload", "1", "--http", "localhost:5150", "--master", "-p", "4", "-w", "sobesity.webapp:app"]

FROM dev as migrator

CMD ["echo", "works fine"]
