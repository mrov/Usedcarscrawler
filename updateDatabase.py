import logging
import pymongo
import utils.crawlerCore
import time
import datetime
from pymongo import MongoClient, UpdateOne
from pprint import pprint
from utils.constants import collectionName, databaseName, connectionString, pageLimit


class DuplicatedRegister(Exception):
    def __init__(self, message, registers):
        self.message = message
        self.registers = registers


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_database():

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(connectionString)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[databaseName]


def get_cars_info(carBrand="", page=1):

    # create the driver object.
    driver = utils.crawlerCore.configure_driver()

    cars = utils.crawlerCore.getCars(driver, carBrand, page)

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


def populate_db(cars):

    # Get the database
    dbname = get_database()

    collection_name = dbname[collectionName]

    for car in cars:
        collection_name.replace_one({'_id': car['_id']}, car, True)

    return 0


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    while True:
        logging.info("started")
        page = 1
        duplicates = 0

        while duplicates == 0 and page < pageLimit:
            duplicates = update_database(get_cars_info("", page), page)
            # duplicates = populate_db(get_cars_info("", page))
            logging.info(
                f"##########################   {page}    ###########################################")
            page = page + 1
            if (duplicates == 0 and page < pageLimit):
                time.sleep(60)

        logging.info(f"slept at: ")
        time.sleep(180)
