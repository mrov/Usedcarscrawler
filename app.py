from flask import Flask
from flask import request

app = Flask(__name__)

app.FLASK_APP = "app.py"
app.FLASK_ENV = "development"
app.FLASK_DEBUG = 1

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/updateDB')
def index():
  return "hello"
  

# params startDate
# params endDate
@app.route('/getCars')
def say_hello():
  return "hello world"
