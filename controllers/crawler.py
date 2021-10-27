from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
from . systemVariables import chromeDriveLocation, formattedURL


def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
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
        WebDriverWait(driver, 10).until(lambda s: s.find_element_by_css_selector("#ad-list").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None

    entirePage = BeautifulSoup(driver.page_source, "lxml")

    for carLink in entirePage.select("li a[data-lurker-detail='list_id']"):
        price = carLink.select_one("span[color='graphite']").text.replace("R$", "").replace(".", "").strip()

        if price:
            cars.append({ "announceName": carLink.select_one("h2").text,
                    "formattedPrice": carLink.select_one("span[color='graphite']").text,
                    "price": int(price),
                    "technicalFeatures": carLink.select_one("span[color='dark']").text,
                    "_id": carLink.attrs['data-lurker_list_id'],
                    "link": carLink.attrs['href'],
                    "img": carLink.select_one("img").attrs["src"],
                    "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z") })
    return cars

if __name__ == "__main__":

    # create the driver object.
    driver = configure_driver()

    getCars(driver)

    # close the driver.
    driver.close()