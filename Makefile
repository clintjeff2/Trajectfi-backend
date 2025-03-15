# to format the codebase
format:
	poetry run black .
	poetry run ruff check . --fix --select I

# to lint the codebase
lint:
	poetry run ruff check .

# isort 
isort:
	poetry run isort .

# build the project
build:
	./build

# build with docker
docker-build:
	cp .env.example .env
	docker compose build


# start the application
start:
	./start

# start the application with docker
docker-start:
	docker compose up

# make database migrations
makemigrations:
	poetry run python manage.py makemigrations

# migrate to database
migrate:
	poetry run python manage.py migrate

# start database
database-up:
	docker compose up trajectfi_db

# top database
database-down:
	docker compose down trajectfi_db

# run commands on docker container. $(command) specifies the command to be run
docker-run:
	docker compose run --rm trajecfi $(command)