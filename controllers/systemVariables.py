# -*- coding: utf-8 -*-
# Must have google chrome installed or change drive config for edge

connectionString = "mongodb://localhost:27017"

databaseName = "py"

pageLimit = 2

chromeDriveLocation = r"C:\Users\Moabe\Documents\studyingWebCrawling\chromedriver.exe"

def formattedURL(carBrand, page):
    return f"https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-pe?o={page}&q={carBrand}"
    