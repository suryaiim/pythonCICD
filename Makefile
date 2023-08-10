#!make
include default_env
export $(shell sed 's/.*//' default_env)
include .env
export $(shell sed 's/.*//' .env)

.EXPORT_ALL_VARIABLES:

build:
	docker build . -f Dockerfile -t ${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_VERSION}

rebuild: 
	docker build --no-cache latest/ -t ${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_VERSION}

up_traefik:
	docker-compose -f docker-compose.traefik.yml up

down_traefik:
	docker-compose -f docker-compose.traefik.yml down

up: build
	echo "Building app"
	docker-compose -f docker-compose.yml \
				   -f docker-compose.traefik.yml \
				-p ${STACK_NAME} up -d --remove-orphans --scale api=3
	docker-compose -f docker-compose.yml -p ${STACK_NAME} logs --follow

down:
	docker-compose -f docker-compose.yml \
				-f docker-compose.traefik.yml \
				-p ${STACK_NAME} down

unit_test_python:
	pytest -p no:cacheprovider src/test

unit_test_docker: build
	docker run -it ${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_VERSION} pytest -p no:cacheprovider ./test

