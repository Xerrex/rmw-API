# [RIDE MY WAY](https://rmw-api-xerrex.herokuapp.com/#)
![license](https://img.shields.io/github/license/mashape/apistatus.svg) 
* It is a REST Application Programming Interface(API) for sharing a ride if persons are traveling in the same direction.
* Ride - This is a vehicle with passenger space.
* Driver - The Creator of the ride is assuemed to me the driver.

* The API is developed in Python/Flask. Consuming the API can be done with any other tech stack that can process JSON endpoints.

## Tools used:
* Python/Flask
* Object Relation Mapper(ORM)

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
    pip install -r requirements/dev.txt
    ```
* Create environment variables.
    *   ```
        touch .env
        ```
    * Add this lines to .env & edit values.
        ```
        export API_TITLE="RMW-API"
        export API_VERSION="1.0"
        export API_DESCRIPTION="Ride sharing API if you have extra seats"
        export SECRET_KEY="welcome home"
        export API_CONF="development"
        export FLASK_APP="run.py"
        export FLASK_ENV="development"
        ```


## Running and Testing the app.
### Running
* Export the environment variables to the system.
    ```
    source .env
    ```
* Activate the virtual environment.
    ```
    source venv/bin/activate
    ```
* Run the App.
    ```
    flask run
    ```
* View the App.
    * Head over to the Address provided at the terminal

### Testing
* use all the steps from [Running](#running) up to activating the environment:
    ```
    python3 -m unittest discover -s tests
    ```
