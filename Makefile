PROJECT_CODE_PATH=/code
DOCKER_COMPOSE=COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose
TEST_DOCKER_COMPOSE=${DOCKER_COMPOSE} -p test_sobesity -f docker-compose.test.yml


.PHONY: build
build:
	${DOCKER_COMPOSE} build

.PHONY: db-bash
db-bash:
	${DOCKER_COMPOSE} exec db bash

.PHONY: db-shell
db-shell:
	${DOCKER_COMPOSE} exec db psql -U sobesity -d sobesity_db

.PHONY: app-bash
app-bash:
	${DOCKER_COMPOSE} run --rm app bash

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
	${DOCKER_COMPOSE} up migrator

.PHONY: create-migration
create-migration:
	${DOCKER_COMPOSE} run --rm migrator alembic revision -m "$(message)"

.PHONY: lint
lint: flake8 import-check format-check

.PHONY: format-all
format-all: format fix-imports

.PHONY: run
run:
	${DOCKER_COMPOSE} up -d

.PHONY: build-test
build-test:
	${TEST_DOCKER_COMPOSE} build

.PHONY: test-unit
test-unit:
	${TEST_DOCKER_COMPOSE} run --rm app pytest -s tests/unit

.PHONY: test-integration
test-integration:
	${TEST_DOCKER_COMPOSE} run --rm app pytest -s tests/intergration/

.PHONY: up-test
up-test:
	${TEST_DOCKER_COMPOSE} up -d

.PHONY: reset-test
reset-test:
	${TEST_DOCKER_COMPOSE} down -v


.PHONY: tests
tests: build-test up-test test-unit test-integration
