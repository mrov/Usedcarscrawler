import logging
import pymongo
import time
from datetime import datetime, timedelta
from utils import crawlerCore
from utils.constants import connectionString, databaseName, collectionName, pageLimit
from pymongo import MongoClient, UpdateOne
from pprint import pprint
from bson.json_util import dumps


class DuplicatedRegister(Exception):
    def __init__(self, message, registers):
        self.message = message
        self.registers = registers


def get_database():
    client = MongoClient(connectionString)

    return client[databaseName]


def get_cars_info(carBrand="", page=1):
    driver = crawlerCore.configure_driver()
    cars = crawlerCore.getCars(driver, carBrand, page)
    driver.close()

    return cars


def update_database(cars, page):

    try:
        dbname = get_database()
        collection_name = dbname[collectionName]

        operations = []
        for car in cars:
            filter = {"announceName": car["announceName"]}
            update = {"$set": car}
            operation = UpdateOne(filter, update, upsert=True)
            operations.append(operation)

        result = collection_name.bulk_write(operations)

        if result.modified_count > 0:
            raise DuplicatedRegister(
                f"{result.modified_count} duplicates on page {page}", result.modified_count)

        logging.info(f"Zero duplicates on page {page}")

        return 0

    except DuplicatedRegister as e:
        logging.info(e.message)
        return e.registers


def db_get_cars(request):
    query = {}

    # Parameters
    startDate = request.args.get('startDate', '')
    endDate = request.args.get('endDate', '')

    query["postDate"] = {}
    query["postDate"]["$gte"] = datetime.strptime(startDate, "%d-%m-%Y").replace(hour=0, minute=0) if bool(
        startDate) else (datetime.now() - timedelta(days=30)).replace(hour=0, minute=0)
    query["postDate"]["$lte"] = datetime.strptime(endDate, "%d-%m-%Y").replace(hour=23, minute=59) if bool(
        endDate) else (datetime.now() + timedelta(days=30)).replace(hour=23, minute=59)

    dbname = get_database()

    list_cur = list(dbname[collectionName].find(query)
                    .sort("postDate", pymongo.ASCENDING))
    return dumps(list_cur)


def craw_website():
    page = 1
    duplicates = 0

    while duplicates == 0 and page <= pageLimit:
        duplicates = update_database(get_cars_info("", page), page)
        page = page + 1
        if (duplicates == 0 and page <= pageLimit):
            time.sleep(20)

    return {"status": "200", "message": f"Database update succeeded {duplicates}"}
