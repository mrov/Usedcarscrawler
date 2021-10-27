from flask import Flask
from controllers import dbController

app = Flask(__name__)

app.FLASK_APP = "app.py"
app.FLASK_ENV = "development"
app.FLASK_DEBUG = 1

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/getCars')
def say_hello():
  return dbController.db_get_cars()