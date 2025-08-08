SHELL := /bin/bash

PROFILE ?= dev
SERVICE := $(if $(filter $(PROFILE),prod),api,api-dev)

.PHONY: up down logs ps sh alembic-rev alembic-up alembic-down alembic-hist

up:
	COMPOSE_PROFILES=$(PROFILE) docker compose up --build -d

down:
	COMPOSE_PROFILES=$(PROFILE) docker compose down -v

logs:
	COMPOSE_PROFILES=$(PROFILE) docker compose logs -f --tail=200 $(SERVICE)

ps:
	COMPOSE_PROFILES=$(PROFILE) docker compose ps

sh:
	COMPOSE_PROFILES=$(PROFILE) docker compose exec -it $(SERVICE) /bin/bash || COMPOSE_PROFILES=$(PROFILE) docker compose exec -it $(SERVICE) /bin/sh

alembic-rev:
	COMPOSE_PROFILES=$(PROFILE) docker compose exec -it $(SERVICE) alembic revision --autogenerate -m "$(m)"

alembic-up:
	COMPOSE_PROFILES=$(PROFILE) docker compose exec -it $(SERVICE) alembic upgrade head

alembic-down:
	COMPOSE_PROFILES=$(PROFILE) docker compose exec -it $(SERVICE) alembic downgrade -1

alembic-hist:
	COMPOSE_PROFILES=$(PROFILE) docker compose exec -it $(SERVICE) alembic history --verbose
