# Tech Assessment Property Data Scraping

## Technical Specs for QA
* Python 3.10* or later
* postgresql 12.6.* or later

## Backend Setup
### Setting up a virtual environment with Python and pip
* clone the repo
* install a virtual env and activate it: `python -m venv env; env/Scripts/activate`[Windows]
* install a virtual env and activate it: `virtualenv --no-site-packages env; source env/bin/activate`[Linux/iOS]
* install requirements: `pip install -r requirements.txt`
* copy the configuration file: `cp main/config/example.development.cfg > main/config/development.cfg`.


### Setting up the Database with PostgreSQL
Setup the PostgreSQL database (minimum version 12.*)
```
psql -U postgres
=# CREATE USER postgres WITH PASSWORD 'database-name';
=# CREATE DATABASE database-name;
=# GRANT ALL PRIVILEGES ON DATABASE database-name TO postgres;
=# \q
```
Or you can use the Graphic interface on windows


### Deploying database changes
* App uses Flask-Migrate (which uses Alembic) to handle database migrations.
* Intialize db `flask db init`
* This will autogenerate a change. Double check that it make sense. To apply it on your machine, run
`flask db migrate`
* To upgrade all versions, this ultimately delete all tables
`flask db upgrade`
  

### Pytest
- Powershell Run: `$ENV:PYTHONPATH = "<name-of-project>"`
- Linux/Mac to set the environment path `export PYTOHNPATH=<name-of-project>`

Then run `pytest` for simple test summary or `pytest -vv` for detailed test summary

### Redis Setup
Redis is required for caching and background task management.

Install Redis:

1. On Mac OS X: `brew install redis`
2. On Windows: Use the Redis [MSI installer](https://github.com/microsoftarchive/redis/releases)
3. On Ubuntu: `sudo apt-get update && sudo apt-get install redis-server`
4. Update your `development.cfg` to include Redis configuration: `REDIS_URL = "redis://<redis-host>"`

## Deployment
### Scheduling Tasks
- You can use the [Astronomer](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart)
To get started:
 1. Initialize an Astronomer project by running `astro dev init`
 2. Start Airflow locally by running `astro dev start`
 3. Navigate to localhost:8080 in your browser and you should see the tutorial DAGs there
 4. To stop the containers run `astro dev stop` alternatively to destroy the container and images run `astro dev kill`

### Framework
- For the API I used [flask-Restful](https://flask-restful.readthedocs.io/en/latest/index.html) to intall `pip install flask-restful` 
which runs on [Flask](https://flask.palletsprojects.com/en/3.0.x/). 
Flask is a micro web framework written in Python. to install `pip install flask`

To access the api-docs `http://localhost:5000/swagger`

