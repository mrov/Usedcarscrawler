# -*- coding: utf-8 -*-
# Must have google chrome installed or change drive config for edge

connectionString = "mongodb://20.241.148.186:27017"

databaseName = "py"

pageLimit = 5

chromeDriveLocation = r"C:\Users\Moabe\Documents\studyingWebCrawling\chromedriver.exe"

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
    