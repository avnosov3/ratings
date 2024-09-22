
DATA-SERVICE := ./data-service/docker-compose.yml

SCORING-SERVICE := ./scoring-service/docker-compose.yml

DR = docker

compose_v2_not_supported = $(shell command docker compose 2> /dev/null)
ifeq (,$(compose_v2_not_supported))
  DOCKER_COMPOSE_COMMAND = docker-compose
else
  DOCKER_COMPOSE_COMMAND = docker compose
endif


cnet:  ## create nginx network
	${DR} network create ratings

rnet:
	${DR} network rm ratings

up:  ## up all services
	@make cnet
	@make dsup
	@make ssup
	@make migrate
	@make import

downv:  ## down all services
	@make dsdownv
	@make ssupdownv
	@make rnet

dsup:
	$(DOCKER_COMPOSE_COMMAND) -f ${DATA-SERVICE} up -d --build

ssup:
	$(DOCKER_COMPOSE_COMMAND) -f ${SCORING-SERVICE} up -d --build

dsdownv:
	$(DOCKER_COMPOSE_COMMAND) -f ${DATA-SERVICE} down -v

ssupdownv:
	$(DOCKER_COMPOSE_COMMAND) -f ${SCORING-SERVICE} down -v

migrate:
	$(DOCKER_COMPOSE_COMMAND) -f ${DATA-SERVICE} exec data-service alembic upgrade head

import:
	$(DOCKER_COMPOSE_COMMAND) -f ${DATA-SERVICE} exec data-service python -m src.upload accommodations.json reviews.json

tests:
	$(DOCKER_COMPOSE_COMMAND) -f ${SCORING-SERVICE} exec scoring-service pytest
