# [RIDE MY WAY](https://rmw-api-xerrex.herokuapp.com/#)
![license](https://img.shields.io/github/license/mashape/apistatus.svg) 
* It is a REST Application Programming Interface(API) for sharing a ride if persons are traveling in the same direction.
* Ride - This is a vehicle with passenger space.
* Driver - The Creator of the ride is assumed to be the driver.

* The API is developed in Python/Flask. Consuming the API can be done with any other tech stack that can process JSON endpoints.


## Technologies/Tools used & needed.
* **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments
* **[SQLITE](https://www.sqlite.org/index.html)** - Small, fast, self-contained, high-reliability, full-featured, SQL DB.
* **[Docker](https://www.docker.com/) / [Docker-compose](https://docs.docker.com/compose/)** - Set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.
* **[Alembic](https://alembic.sqlalchemy.org/en/latest/index.html)** is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit.


## Table of Contents
|#||
|-|---------|
|*| [Installation & Running](#installation)|
|*| [Testing](#testing)|

## Installation
```
The commands are from a bash terminal
```

### Locally
* Clone the repository.
```
git clone https://github.com/Xerrex/rmw-API.git
```

* Change into cloned folder.
```
cd rmw-API
```

* Create a virtual environment & activate it.
```
python3 -m venv venv && source venv/bin/activate
```

* Install dependancies
```
pip install -r requirements.txt
```

* Create and edit environment variables.
```
touch cp envExample .env
```


## Running and Testing the app.
### Running
* Run the App.
```
fastapi dev main.py
```

* View the App serving [here](http://127.0.0.1:8000 )

* View API docs [here](ttp://127.0.0.1:8000/docs)


### Testing
* Coming soon.

