# Data processing

## About
This service allows analyzing user's data for project feature improvements.

## Project setup
### Venv
Create virtual environment and then install requirements
```
pip install -r requirements.txt
```

## Run server
```
uvicorn web.server:app --reload
```

## Helpers
### Dump creating

Run this SQL from Postgres

`COPY users TO '<path>\test_users.csv' DELIMITER ',' CSV HEADER;
`