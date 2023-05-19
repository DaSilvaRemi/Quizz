# API QUIZ

This is the API service for the QUIZ application backend, developed using the Flask framework in Python and an SQLite database.

## Project Setup

### Without docker

#### venv creation and dependencies installation
```sh
python -m venv 
```

```sh
pip install -r requirements.txt
```

#### Lauch the server

```sh
python  app.py
```

The application will be available at
```
http://localhost:5000/
```

### With docker

``` sh
docker image build -t quiz-local-api .
```

``` sh
docker container run -it --rm -p 5000:5000 --name quiz-local-api quiz-local-api

```

## BDD Creation

Open Postman and import this file
```
Quiz TDD.postman_collection.json
```

Launch the collection "0 - Rebuild DB"

