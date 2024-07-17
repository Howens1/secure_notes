## Secure Notes app

## Description
Sample Backend Application written with FastAPI Framework to authenticate users and and store encrypted notes in database

Work in Progress to be tested on fresh db

## Installation
- pip install -r requirements.txt
- Alembic db
    - alembic init alembic
    - edit generated alembi.ini for sql connection
    - alembic revision --autogenerate -m "Initial migration"
    - alembic upgrade head
- uvicorn main:app --reload

