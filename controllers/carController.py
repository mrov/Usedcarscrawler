import os
from app import app
from flask_cors import cross_origin
from repository import carRepository
from flask import request


@app.route('/updateDB')
def index():
    return carRepository.craw_website()

# params startDate
# params endDate


@app.route('/getCars')
@cross_origin()
def say_hello():
    return carRepository.db_get_cars(request)
