# Automatically regenerate `.env` before running any target
.PHONY: up build run clean env

install: env build

env:
	@if [ ! -f .env ] || ! grep -q "^PRESENTATION_SOURCE_PATH=" .env; then \
		echo -n "Please enter the path for PRESENTATION_SOURCE_PATH: "; \
		read path; \
		echo "PRESENTATION_SOURCE_PATH=$$path" >> .env; \
	fi

# Example: Start docker-compose
up: build
	docker-compose up

# Other Makefile targets
build: env
	docker-compose build

clean:
	rm -f .env