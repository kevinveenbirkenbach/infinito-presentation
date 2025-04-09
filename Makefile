# Automatically regenerate `.env` before running any target
.PHONY: up build run clean env

install: env build

env:
	@if [ ! -f .env ] || ! grep -q "^PRESENTATION_SOURCE_PATH=" .env; then \
		path=$$(pkgmgr path cymais); \
		echo "PRESENTATION_SOURCE_PATH=$$path" >> .env; \
	fi

# Example: Start docker-compose
up: build
	docker-compose up

# Other Makefile targets
build: env
	docker-compose build

clean:
	git clean -f -d -X

deinstall: clean