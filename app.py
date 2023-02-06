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

@app.route('/updateDB')
def index():
  return carRepository.craw_website()

# params startDate
# params endDate
@app.route('/getCars')
@cross_origin()
def say_hello():
  return carRepository.db_get_cars(request)