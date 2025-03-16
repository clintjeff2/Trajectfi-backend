# Contributing Guideline

We appreciate your interest in contributing to our project amd We welcome contributions from everyone.


## First Steps

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-github-username/spherre.git
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/Trajectfi/Trajectfi-backend.git
   ```

## Installation

### Prerequisites
- Python 3.12 or higher
- Make
- Docker

### Using Docker

1. Copy the environment variables
    ```bash
        cp .env.example .env
    ```
2. Build the project
    ```bash
        docker compose build # alternatively, you can run `make docker-build`
    ```
3. Install pre-commit hooks
    ```bash
        pip install pre-commit
        pre-commit install
    ```
4. Start the application
    ```bash
        docker compose up # alternatively, you can run `make docker-start`
    ```
5. Migrate models to DB
    ```bash
        make docker-migrate
    ```

### Alternative Process

1. Run the make build command to build the project
    ```bash
        make build # alternatively, you can run `./build.sh`
    ```
2. Start the database server
    ```bash
        make database-up
    ```
3. Edit the .env file and change DB_HOST=trajectfi_db to DB_HOST=localhost
4. Start the application
    ```bash
        make start # alternatively, you can run `./start.sh`
    ```
5. Migrate models to DB
    ```bash
        make migrate
    ```

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or 
   ```bash
   git checkout -b fix/issue-number
   ```


2. Make your changes

3. Make migrations if db model change is included in your changes
     ```bash
        make docker-migrations # alternratively, run `make migrations` if not using docker
    ```

4. Format the codebase
     ```bash
        make docker-format # alternratively, run `make format` if not using docker
    ```

5. Commit your changes:
   ```bash
   git commit -m "(prefix): Description of changes"
   ```

6. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```
   or
   ```bash
   git push origin fix/issue-number
   ```

6. Open a Pull Request


### Commit Messages

Use these prefixes for commits:

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Non-functional code changes (e.g., formatting)
- **refactor:** Code structure improvements
- **perf:** Performance enhancements
- **test:** Adding or updating tests
- **build:** Build-related changes
- **ci:** CI configuration updates
- **chore:** Non-code changes (e.g., config files)
- **revert:** Reverting a commit

Example:
```
feat: add new component
fix: resolve button click issue
docs: update README
```

**If you have any questions, feel free to reach out to us**
