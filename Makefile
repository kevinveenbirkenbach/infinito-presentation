# Automatically regenerate `.env` before running any target
.PHONY: up build run clean link

install: link build

# Create a symbolic link to the cymais repository
link:
	@CYMAIS_REPOSITORY_PATH=$$(pkgmgr path cymais); \
	if [ -d $$CYMAIS_REPOSITORY_PATH ]; then \
		cp -rv $$CYMAIS_REPOSITORY_PATH cymais; \
		echo "Symbolic link created: cymais -> $$CYMAIS_REPOSITORY_PATH"; \
	else \
		echo "Error: Source directory does not exist!"; \
	fi

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