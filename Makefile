.PHONY: dev release push publish

PROJECT_NAME := kglstm_recommender
DEV_NAME = $(PROJECT_NAME)-$(USER)

all: dev

run:
	cd docker && docker-compose -p "$(DEV_NAME)" down && docker-compose -p "$(DEV_NAME)" up --force-recreate