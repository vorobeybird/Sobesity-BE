PROJECT_CODE_PATH=/home/room_booking/room_booking
DOCKER_COMPOSE=COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose


.PHONY: build
build:
	${DOCKER_COMPOSE} build

.PHONY: db-bash
db-bash:
	${DOCKER_COMPOSE} exec db bash

.PHONY: db-shell
db-shell:
	${DOCKER_COMPOSE} exec db psql -U room_booking -d room_booking_db

.PHONY: app-bash
app-bash:
	${DOCKER_COMPOSE} exec app bash

.PHONY: format
format:
	${DOCKER_COMPOSE} run --rm app sh -c "black ${PROJECT_CODE_PATH}"

.PHONY: format-check
format-check:
	${DOCKER_COMPOSE} run --rm app sh -c "black --check ${PROJECT_CODE_PATH}"

.PHONY: import-check
import-check:
	${DOCKER_COMPOSE} run --rm app sh -c "isort --check ${PROJECT_CODE_PATH}"

.PHONY: fix-imports
fix-imports:
	${DOCKER_COMPOSE} run --rm app sh -c "autoflake -r --in-place --ignore-init-module-imports --remove-all-unused-imports ${PROJECT_CODE_PATH} && isort ${PROJECT_CODE_PATH}"

.PHONY: flake8
flake8:
	${DOCKER_COMPOSE} run --rm app flake8 ${PROJECT_CODE_PATH}

.PHONY: migrate
migrate:
	${DOCKER_COMPOSE} run --rm migrator

.PHONY: create-migration
create-migration:
	${DOCKER_COMPOSE} run --rm migrator 

.PHONY: lint
lint: flake8 import-check format-check

.PHONY: format-all
format-all: format fix-imports

.PHONY: run
run:
	${DOCKER_COMPOSE} up -d
	make migrate


