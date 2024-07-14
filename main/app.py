import os, redis
from flask import Flask, send_file, session
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api

app = Flask(
    __name__,
    static_folder='static')

app.secret_key = os.environ.get('SECRET_KEY', 'SECRET_KEY')

env = os.environ.get('FLASK_ENV', 'development')

app.config['ENV'] = env
app.config.from_pyfile(f'config/{env}.cfg')

# CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf_protect = CSRFProtect(app)

# Database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECURITY_REGISTERABLE'] = True

from flask_sslify import SSLify
ssl = SSLify(app)
app.config['WTF_CSRF_ENABLED'] = False

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_url = app.config['REDIS_URL']
redis_client = redis.StrictRedis.from_url(redis_url)

from flask_cors import CORS
CORS(app)
@app.route('/swagger.yaml')
def swagger_yaml():
    return send_file('swagger.yaml')

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Property API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

from main.api import PropertyListResource, PropertyListByTypeResource 
api = Api(app)

api.add_resource(PropertyListResource, '/api/v1/properties')
api.add_resource(PropertyListByTypeResource, '/api/v1/properties/<string:selected_option>')