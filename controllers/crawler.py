from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
from . systemVariables import chromeDriveLocation, formattedURL


def translate_date(date, hour):
    translated_date = ""
    if (date.upper() == "HOJE"):
        translated_date = datetime.now().strftime("%Y %b %d")
        translated_date = datetime.strptime(translated_date + " " + hour, "%Y %b %d %H:%M")
    elif (date.upper() == "ONTEM"):
        translated_date = datetime.now() - timedelta(days=1)
        translated_date = datetime.strptime(translated_date + " " + hour, "%Y %b %d %H:%M")
    # TODO para fazer com datas maiores que "ontem"
    # else:
    #     datetime.strptime(date + " " + hour, " %H:%M")
    return translated_date

def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
    # driver = webdriver.Chrome(options = chrome_options)
    # For windows
    driver = webdriver.Chrome(executable_path=chromeDriveLocation, options = chrome_options)
    return driver

def getCars(driver, carBrand="", page=1):
    cars = []

    driver.get(formattedURL(carBrand, page))

    try:
        WebDriverWait(driver, 10).until(lambda s: s.find_element(By.CSS_SELECTOR, "#ad-list").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None

    entirePage = BeautifulSoup(driver.page_source, "lxml")

    for carLink in entirePage.select('li a[data-lurker-detail="list_id"]'):
        textList = carLink.select("span[color='--color-neutral-130']")
        price = checkPrice(carLink.select_one("span[color='--color-neutral-130']"))
        #DEBUG
        # for index, node in enumerate(carLink.select("span[color='--color-neutral-130']"), start=0):
        #     print(f"{index}  {node.text}")
        kilometer = textList[1].text
        year = textList[2].text
        shiftType = textList[3].text
        gasType = textList[4].text
        post_date = textList[-1].text
        post_location = textList[-2].text

        # Update this method to translate the new date format (Hoje, 13:45)
        # translated_date = translate_date(post_date, post_hour)

        if price:
            cars.append({ "announceName": carLink.select_one("h2").text,
                    "formattedPrice": textList[0].text,
                    "price": int(price),
                    "kilometer": kilometer,
                    "year": year,
                    "shiftType": shiftType,
                    "gasType": gasType,
                    "_id": carLink.attrs['data-lurker_list_id'],
                    "link": carLink.attrs['href'],
                    "img": carLink.select_one("img").attrs["src"],
                    "location": post_location,
                    # TODO format postDate
                    "postDate": post_date,
                    "created": datetime.now() })
    print("Crawler OK")
    return cars

def checkPrice (priceText):
    if priceText:
        return priceText.text.replace("R$", "").replace(".", "").strip()
    else:
        return ""

if __name__ == "__main__":

    # create the driver object.
    driver = configure_driver()

    getCars(driver)

    # close the driver.
    driver.close()