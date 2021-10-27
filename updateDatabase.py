import pymongo
import controllers.crawler
import time
from pymongo import MongoClient
from pprint import pprint
from controllers.systemVariables import databaseName, connectionString, pageLimit

def get_database():

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(connectionString)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[databaseName]

def get_cars_info(carBrand="", page=1):

    # create the driver object.
    driver = controllers.crawler.configure_driver()

    cars = controllers.crawler.getCars(driver, carBrand, page)

    driver.close()

    return cars

def update_database(cars):
    
    try:
        # Get the database
        dbname = get_database()

        collection_name = dbname["cars"]

        collection_name.insert_many(cars, ordered=False, bypass_document_validation=True)
        
        return 0

    except pymongo.errors.BulkWriteError as e:
        panic_list = list(filter(lambda x: x['code'] == 11000, e.details['writeErrors']))
        print(f"tried to insert '{len(panic_list)}' duplicates")
        return len(panic_list)
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    page = 1
    duplicates = 0

    while duplicates == 0 and page < pageLimit:
        duplicates = update_database(get_cars_info("", page))
        page = page + 1
        if (duplicates == 0 and page < pageLimit):
            time.sleep(20)