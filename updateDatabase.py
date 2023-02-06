from datetime import datetime
import pymongo
import utils.crawlerCore
import time
from pymongo import MongoClient
from pprint import pprint
from utils.constants import collectionName, connectionString, pageLimit

def get_database():

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(connectionString)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[collectionName]

def get_cars_info(carBrand="", page=1):

    # create the driver object.
    driver = utils.crawlerCore.configure_driver()

    cars = utils.crawlerCore.getCars(driver, carBrand, page)

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

def populate_db(cars):

    # Get the database
    dbname = get_database()

    collection_name = dbname["cars"]

    for car in cars:
        collection_name.replace_one({'_id': car['_id']}, car, True)

    return 0
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    while True:
        print("started")
        page = 1
        duplicates = 0

        while duplicates == 0 and page < pageLimit:
            # duplicates = update_database(get_cars_info("", page))
            duplicates = populate_db(get_cars_info("", page))
            print(f"##########################   {page}    ###########################################")
            page = page + 1
            if (duplicates == 0 and page < pageLimit):
                time.sleep(60)
        
        print(f"slept at: " + datetime.now().strftime("%H:%M"))
        time.sleep(180)