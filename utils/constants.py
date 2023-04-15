# -*- coding: utf-8 -*-
# Must have google chrome installed or change drive config for edge

import os

mongo_uri = os.environ.get('MONGO_URI') if os.environ.get(
    'MONGO_URI') else "mongodb://localhost:27017"

connectionString = mongo_uri

databaseName = "py"

collectionName = "cars"

pageLimit = 10

chromeDriveLocation = os.environ.get('CHROME_DRIVE_LOCATION')

monthsDictionary = {
    "jan": "January",
    "fev": "February",
    "mar": "March",
    "abr": "April",
    "mai": "May",
    "jun": "June",
    "jul": "July",
    "ago": "August",
    "set": "September",
    "out": "October",
    "nov": "November",
    "dez": "December"
}


def formattedURL(carBrand, page):
    return f"https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-pe?o={page}&q={carBrand}"
