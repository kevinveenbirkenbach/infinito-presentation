# Automatically regenerate `.env` before running any target
.PHONY: all env up build run clean

all: env up

# `.env` is always regenerated
env:
	@echo "CYMAIS_REPOSITORY_PATH=$$(pkgmgr path cymais)" >> .env
	@echo ".env file regenerated."

# Example: Start docker-compose
up: 
	docker-compose up --build

# Other Makefile targets
build: 
	docker-compose build

run: 
	docker-compose run app

clean:
	rm -f .env