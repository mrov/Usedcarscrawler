import pymongo
import time
from datetime import datetime, timedelta
from . import crawler
from . systemVariables import connectionString, databaseName, pageLimit
from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps

def get_database():
    client = MongoClient(connectionString)

    return client[databaseName]

def get_cars_info(carBrand="", page=1):
    driver = crawler.configure_driver()
    cars = crawler.getCars(driver, carBrand, page)
    driver.close()

    return cars

def update_database(cars, page):
    
    try:
        dbname = get_database()
        collection_name = dbname["cars"]
        collection_name.insert_many(cars, ordered=False, bypass_document_validation=True)
        
        print(f"Zero duplicates on page {page}")

        return 0

    except pymongo.errors.BulkWriteError as e:
        panic_list = list(filter(lambda x: x['code'] == 11000, e.details['writeErrors']))
        print(f"Tried to insert '{len(panic_list)}' duplicates")
        return len(panic_list)

def db_get_cars(request):
    query = {}

    #Parameters
    startDate = request.args.get('startDate', '')
    endDate = request.args.get('endDate', '')

    ## TODO try to update this to postDate
    query["created"] = {}
    query["created"]["$gte"] = datetime.strptime(startDate, "%d-%m-%Y").replace(hour=0, minute=0)  if bool(startDate) else (datetime.now() - timedelta(days=30)).replace(hour=0, minute=0)
    query["created"]["$lte"] = datetime.strptime(endDate, "%d-%m-%Y").replace(hour=23, minute=59)  if bool(endDate) else (datetime.now() + timedelta(days=30)).replace(hour=23, minute=59) 

    dbname = get_database()

    list_cur = list(dbname["cars"].find(query).sort("created",pymongo.ASCENDING))
    return dumps(list_cur)

def craw_website():
    page = 1
    duplicates = 0

    while duplicates == 0 and page <= pageLimit:
        duplicates = update_database(get_cars_info("", page), page)
        page = page + 1
        if (duplicates == 0 and page <= pageLimit):
            time.sleep(20)

    return { "status": "200", "message": f"Banco atualizado com sucesso {duplicates}"}
