import sys
sys.path.append("~/site/wwwroot/__oryx_packages__")
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from repository import carRepository

app = Flask(__name__)

app.FLASK_APP = "app.py"
app.FLASK_ENV = "development"
app.FLASK_DEBUG = 1

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

# import declared routes
import controllers.carController