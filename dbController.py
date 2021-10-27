from pymongo import MongoClient
from pprint import pprint
from systemVariables import databaseName
import pymongo
import crawler

def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[databaseName]
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    # create the driver object.
    driver = crawler.configure_driver()

    cars = crawler.getCars(driver, "", 1)

    driver.close()
    
    try:
        # Get the database
        dbname = get_database()


        collection_name = dbname["cars"]

        collection_name.insert_many(cars, ordered=False, bypass_document_validation=True)
        

    # TODO if dont have duplicates try the next page
    except pymongo.errors.BulkWriteError as e:
        panic_list = list(filter(lambda x: x['code'] == 11000, e.details['writeErrors']))
        print(f"tried to insert '{len(panic_list)}' duplicates")
