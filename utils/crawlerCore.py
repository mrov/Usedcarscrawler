import logging
import pytz
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from utils.constants import chromeDriveLocation, formattedURL, monthsDictionary

# inputDate format "Hoje, 13:45"

utc_tz = pytz.timezone('Etc/GMT-3')


def translate_date(inputDate):
    translated_date = ""
    splitedDate = inputDate.split(", ")
    date = splitedDate[0]
    hour = splitedDate[1]
    if ("HOJE" in date.upper()):
        translated_date = datetime.now().strftime("%Y %b %d")
        translated_date = datetime.strptime(
            translated_date + " " + hour, "%Y %b %d %H:%M")
    elif ("ONTEM" in date.upper()):
        translated_date = datetime.now() - timedelta(days=1)
        translated_date = datetime.strptime(
            translated_date + " " + hour, "%Y %b %d %H:%M")
    else:
        day = date.split(" ")[0]
        # month in jan format
        month = date.split(" ")[0]
        translated_date = datetime.now()
        translated_date = datetime.strptime(
            f"{day} {monthsDictionary[month]} {datetime.now().year} {hour}", "%d %B %Y %H:%M")
    return utc_tz.localize(translated_date)


def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()

    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
    driver = webdriver.Chrome(options=chrome_options)
    # For windows
    # driver = webdriver.Chrome(executable_path=chromeDriveLocation, options = chrome_options)
    return driver


def getCars(driver, carBrand="", page=1):
    cars = []

    driver.get(formattedURL(carBrand, page))

    try:
        WebDriverWait(driver, 10).until(lambda s: s.find_element(
            By.CSS_SELECTOR, "#ad-list").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None

    entirePage = BeautifulSoup(driver.page_source, "lxml")

    for carCard in entirePage.select('li a[data-ds-component="DS-AdCardHorizontal"]'):
        second_div = carCard.select_one('div:nth-of-type(2)')
        labelGroup = second_div.select('span')
        formattedPrice = carCard.select_one(
            "span[color='--color-neutral-130']")
        price = checkPrice(formattedPrice)
        # DEBUG
        # for index, node in enumerate(labelGroup, start=0):
        #     print(f"{index}  {node.text}")
        kilometer = labelGroup[0].text
        year = labelGroup[1].text
        gasType = labelGroup[2].text
        shiftType = labelGroup[3].text
        post_date = labelGroup[-1].text
        post_location = labelGroup[-3].text

        translated_date = translate_date(post_date)

        if price and int(price) < 300000:
            cars.append({"announceName": carCard.select_one("h2").text,
                         "formattedPrice": formattedPrice.text,
                         "price": int(price),
                         "kilometer": kilometer,
                         "year": year,
                         "shiftType": shiftType,
                         "gasType": gasType,
                         "link": carCard.attrs['href'],
                         "img": carCard.select_one("img").attrs["src"],
                         "location": post_location,
                         "postDate": translated_date,
                         "created": datetime.now()})
    logging.info("Crawler OK")
    return cars


def checkPrice(priceText):
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
