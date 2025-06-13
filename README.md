# PM Companies API

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-%3E=2.0-green.svg)
![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)
![CI](https://img.shields.io/github/actions/workflow/status/bengeek06/pm-companies-api/ci.yml?branch=main)
![Coverage](https://img.shields.io/badge/coverage-pytest-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

A minimalist, production-ready RESTful API to manage companies with hierarchical organization, import/export features, and configuration/version endpoints.  
This repository provides a solid foundation for your next business-oriented API project, with environment-based configuration, Docker support, migrations, and a full OpenAPI 3.0 specification.

---

## Features

- **Environment-based configuration**: Easily switch between development, testing, staging, and production using the `FLASK_ENV` environment variable.
- **RESTful API**: CRUD endpoints for the `Company` resource, plus endpoints for version, configuration, import/export.
- **OpenAPI 3.0 documentation**: See [`openapi.yml`](openapi.yml).
- **Docker-ready**: Includes a `Dockerfile` and healthcheck script.
- **Database migrations**: Managed with Alembic/Flask-Migrate.
- **Testing**: Pytest-based test suite.
- **Logging**: Colored logging for better readability.

---

## Environments

The application behavior is controlled by the `FLASK_ENV` environment variable.  
Depending on its value, different configuration classes and `.env` files are loaded:

- **development** (default):  
  Loads `.env.development` and uses `app.config.DevelopmentConfig`.  
  Debug mode is enabled.

- **testing**:  
  Loads `.env.test` and uses `app.config.TestingConfig`.  
  Testing mode is enabled.

- **staging**:  
  Loads `.env.staging` and uses `app.config.StagingConfig`.  
  Debug mode is enabled.

- **production**:  
  Loads `.env.production` and uses `app.config.ProductionConfig`.  
  Debug mode is disabled.

See `app/config.py` for details.  
You can use `env.example` as a template for your environment files.

---

## API Endpoints

The main endpoints are:

| Method | Path                | Description                           |
|--------|---------------------|---------------------------------------|
| GET    | /version            | Get API version                       |
| GET    | /config             | Get current app configuration         |
| GET    | /companies          | List all companies                    |
| POST   | /companies          | Create a new company                  |
| GET    | /companies/{id}     | Get a company by ID                   |
| PUT    | /companies/{id}     | Replace a company by ID               |
| PATCH  | /companies/{id}     | Partially update a company by ID      |
| DELETE | /companies/{id}     | Delete a company by ID                |
| GET    | /export/csv         | Export all companies as CSV           |
| POST   | /import/csv         | Import companies from a CSV file      |
| POST   | /import/json        | Import companies from a JSON file     |

See [`openapi.yml`](openapi.yml) for full documentation and schema details.

---

## Project Structure

```
.
├── app
│   ├── config.py
│   ├── __init__.py
│   ├── logger.py
│   ├── models.py
│   ├── resources
│   │   ├── companies.py
│   │   ├── config.py
│   │   ├── export_to.py
│   │   ├── import_from.py
│   │   ├── __init__.py
│   │   └── version.py
│   ├── routes.py
│   └── schemas.py
├── CODE_OF_CONDUCT.md
├── COMMERCIAL-LICENCE.txt
├── Dockerfile
├── env.example
├── instance
├── LICENCE.md
├── LICENSE
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── openapi.yml
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── run.py
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_config.py
│   ├── test_export_to.py
│   ├── test_import_from.py
│   ├── test_init.py
│   ├── test_run.py
│   ├── test_version.py
│   └── test_wsgi.py
├── wait-for-it.sh
└── wsgi.py
```

---

## Usage

### Local Development

1. Copy `env.example` to `.env.development` and set your variables.
2. Install dependencies:
   ```
   pip install -r requirements-dev.txt
   ```
3. Run database migrations:
   ```
   flask db upgrade
   ```
4. Start the server:
   ```
   FLASK_ENV=development python run.py
   ```

### Docker

Build and run the container:
```
docker build -t pm-companies-api .
docker run --env-file .env.development -p 5000:5000 pm-companies-api
```

### Testing

Run all tests with:
```
pytest
```

---

## License

This project is licensed under the GNU AGPLv3.  
See [LICENSE](LICENSE) and [COMMERCIAL-LICENCE.txt](COMMERCIAL-LICENCE.txt) for details.

---

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
