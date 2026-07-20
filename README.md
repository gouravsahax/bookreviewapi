# Film Review API

A high-performance REST API for managing and reviewing films, fully configured for cloud deployment.

## Tech Stack

This project leverages the following technologies:

### Core Framework
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast, web framework for building APIs with Python.
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation and settings management using Python type hints.

### Database
- **[PostgreSQL](https://www.postgresql.org/)**: Powerful, open-source object-relational database system.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Python SQL toolkit and Object Relational Mapper (ORM).
- **[psycopg2](https://www.psycopg.org/)**: PostgreSQL database adapter for Python.

### Security & Authentication
- **[Passlib](https://passlib.readthedocs.io/) & bcrypt**: Secure password hashing.
- **[python-jose](https://pypi.org/project/python-jose/)**: JSON Object Signing and Encryption for JWT tokens.

### Deployment & Infrastructure
- **[Mangum](https://mangum.io/)**: Adapter to run FastAPI applications on AWS Lambda.
- **[Serverless Framework](https://www.serverless.com/)**: Infrastructure as Code (IaC) tool for deploying to AWS Lambda.
- **[Docker](https://www.docker.com/)**: Containerization via the included Dockerfile.
- **[GitHub Actions](https://github.com/features/actions)**: Automated CI/CD pipeline for deploying directly to AWS.

## Setup

1. Copy `env._ex.txt` to `.env` and configure your local or remote database URL (`DB_URL`).
2. Run `pip install -r requirements.txt`.
3. Run locally using Uvicorn: `uvicorn main:app --reload`
4. Deploy to AWS using: `serverless deploy`
