# Backend

## Project setup

### Venv
Create virtual environment and then install requirements
```
pip install -r requirements.txt
```

### Perform migrations
```
python manage.py db init
```
```
python manage.py db migrate
```
```
python manage.py db upgrade
```


### Run server
Use this command inside your venv
```
flask run
```
