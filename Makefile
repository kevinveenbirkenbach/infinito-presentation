# Automatically regenerate `.env` before running any target
.PHONY: up build run clean env

# Clone the latest version of colorgen package locally
update-vendor:
	rm -rf vendor/colorscheme-generator
	git clone --depth=1 https://github.com/kevinveenbirkenbach/colorscheme-generator.git vendor/colorscheme-generator

# Create virtualenv and install python dependencies
install: update-vendor
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

install: env build

env:
	@if [ ! -f .env ] || ! grep -q "^PRESENTATION_SOURCE_PATH=" .env; then \
		path=$$(pkgmgr path cymais); \
		echo "PRESENTATION_SOURCE_PATH=$$path" >> .env; \
	fi

# Example: Start docker-compose
up: build
	docker-compose up -d

# Other Makefile targets
build: env
	docker-compose build

clean:
	git clean -f -d -X

deinstall: clean