service = trajectfi

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
	chmod +x ./build.sh
	./build.sh

# start the application
start:
	chmod +x ./start.sh
	./start.sh

# make database migrations
migrations:
	poetry run python manage.py makemigrations

# migrate to database
migrate:
	poetry run python manage.py migrate

#  run test
test:
	poetry run python manage.py test

# start database
database-up:
	docker compose up trajectfi_db -d

# top database
database-down:
	docker compose down trajectfi_db

# start the application with docker
docker-start:
	docker compose up

# build with docker
docker-build:
	cp .env.example .env
	docker compose build

# run commands in docker container. $(command) specifies the command to be run
docker-run:
	docker compose run --rm ${service} $(command)

# make migrations with docker
docker-migrations:
	docker compose run --rm ${service} python manage.py makemigrations

# migrate to db with docker
docker-migrate:
	docker compose run --rm ${service} python manage.py migrate

# run tests with docker
docker-test:
	docker compose run --rm ${service} python manage.py test

# to format the codebase with docker
docker-format:
	docker compose run --rm ${service} black .
	docker compose run --rm ${service} ruff check . --fix --select I

# to lint the codebase with docker
docker-lint:
	docker compose run --rm ${service} ruff check .

# isort with docker
docker-isort:
	docker compose run --rm ${service}isort .