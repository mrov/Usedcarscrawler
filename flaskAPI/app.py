from flask import Flask
from controllers import dbController

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/getCars')
def say_hello():
  return dbController.db_get_cars()
