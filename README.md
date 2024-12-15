# Scrape Hotel Data



## Introduction

This documentation provides an overview of the process and tools used to scrape hotel data from Booking.com.



## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Dependency Management with Poetry](#dependency-management-with-poetry)
- [Project setup](#project-setup)
- [API Documentation](#api-documentation)
- [Testing the app](#testing)
- [Code Quality](#code-quality)
- [Continuous Integration](#continuous-integration)



## Project Overview

< add image here >



## Project Structure

The project is organized following this structure:

```
├── README.md
├── backend
|   ├── Dockerfile
|   ├── app
|   │   ├── api
|   │   │   └── endpoints
|   │   │       ├── hotels.py
|   │   │       └── main.py
|   │   |       └── services.py
|   │   |       └── logger.py
|   │   └── database
|   │       ├── crud.py
|   │       ├── database.py
|   │       ├── main.py
|   │       └── models.py
└── tests
    └── services
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── node_modules
│   ├── public
│   └── src
│       ├── App.css
│       ├── App.js
│       ├── App.test.js
│       ├── components
│       ├── index.css
│       ├── index.js
│       ├── logo.svg
│       ├── reportWebVitals.js
│       ├── services
│       └── setupTests.js
├── docker-compose.yaml
```

- `/backend`:
    - `Dockerfile`: Defines the backend container, specifying the base image, dependencies, and startup commands.
    - `app`: Contains the core backend application logic, including services, and endpoints.
    - `database`: Manages database interactions, including models, CRUD operations, and connections.
    - `tests`: Contains unit and integration tests for the backend application to ensure functionality and reliability.
- `/frontend`:
    - `Dockerfile`: Defines the frontend container, specifying the build environment for the React application.
    - `src`: Holds the source code for the frontend, including components, styles, and services for the user interface.
- `docker-compose.yaml`: Orchestrates multi-container applications,     defining how the backend, frontend, and database interact in a unified environment.



## Dependency Management with Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management. Poetry simplifies the process of managing dependencies and packaging Python projects.

Once installed, you can easily manage dependencies by running `poetry add <dependency>` to add the new dependency and `poetry install`, which installs all required packages listed in the [`pyproject.toml`](pyproject.toml)
 file.



## Project setup

To set up the project, you need to execute the following [docker compose](https://docs.docker.com/compose/) command:

```sh
docker compose up --build
```

Docker Compose is a tool for defining and running multi-container Docker applications. It allows you to use a YAML file to configure your application's services, networks, and volumes. By running the above command, Docker Compose will build the images and start the containers (backend / frontend / database) as specified in the `docker-compose.yaml` file.


After initializing Docker Compose, the backend, frontend, and database services will be available. You can access the web page by navigating to [http://localhost:3000/](http://localhost:3000/) in your web browser.



## API Documentation

You can find the API documentation at the following link: [API Documentation](http://localhost:8000/docs)



## Testing the app

### Searching and saving data

To use the API, you need to enter the name of a valid hotel and click on the search button. After retrieving the hotel data, click on the save button to store the information in the database.


### Database Information

This project uses PostgreSQL as the database. To check the data in the database, follow these steps:

1. Ensure the PostgreSQL service is running. You can start it using Docker Compose if it's not already running:
    ```sh
    docker compose up --build
    ```

2. Check the container ID that is running the database service:

```
docker ps
CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                    NAMES
<app-container-id>   ta-ast-api-app        "sh -c 'xvfb-run -a …"   12 minutes ago   Up 12 minutes   0.0.0.0:8000->8000/tcp   ta-ast-api-app-1
<frontend-container-id>  ta-ast-api-frontend   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:3000->3000/tcp   ta-ast-api-frontend-1
<db-container-id>   postgres:13           "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   5432/tcp                 ta-ast-api-db-1
```

3. Access the container using the iteractive mode (`-it`)

`docker exec -it <db-container-id> psql -U postgres -d postgres -c "SELECT * FROM hotels;"

```
 id |           name            |                                                                                                          address                                                                                                          |   description    | review
----+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------+--------
  1 | Catalonia Barcelona Plaza | Plaza España, 6-8, Sants-Montjuïc, 08014 Barcelona, EspañaUbicación excelente, ¡puntuada con 9.3/10!(puntuación basada en 3226 comentarios)Valorado por los clientes después de alojarse en el Catalonia Barcelona Plaza. | some description |    8.6
(1 row)
```



## Code Quality

This project uses several tools to maintain code quality and enforce coding standards:

- **[black](https://black.readthedocs.io/)**: A code formatter that ensures consistent code style.
- **[pylint](https://pylint.pycqa.org/)**: A static code analysis tool to enforce coding standards and detect errors.
- **[isort](https://pycqa.github.io/isort/)**: A tool to sort and format imports automatically.
- **[mypy](http://mypy-lang.org/)**: A static type checker to ensure type safety in Python code.

These tools are integrated with [pre-commit](https://pre-commit.com/), ensuring that they are automatically run before each commit to maintain code quality.

To manually run these tools, you can use the following commands:

`pre-commit run --all-files` or `poetry run pre-commit run --all-files`



## Unit Tests

[WIP: https://github.com/renatoramossilva/ta-ast-api/pull/23]



## Continuous Integration

This project uses GitHub Actions to automate code quality checks and testing before merging into the master branch. The tools  included in the workflow are described in [Code Quality](#code-quality) session.



### Integration Workflow

Whenever a pull request is opened, the GitHub Actions workflow will trigger and perform the following checks:

- Code Formatting: Run `black` and `isort` to format the code.
- Static Analysis: Execute `pylint` and `mypy` to ensure code quality.
- Unit Testing [WIP]: Run `pytest` to execute the unit tests and check for coverage. (specifically 3.9, 3.10, 3.11, and 3.12)

This setup ensures that only code that passes all checks is merged into the master branch, maintaining a high standard of code quality throughout the development process.
