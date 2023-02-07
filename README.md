# Studying Web Crawling

Reason: I wanted to buy a car but the olx and mercado livre view didn't help me too much to see the cars prices. So I made this Crawler to get those cars infos and turn them into a chart with a dot for each car and then see the car by price. It turns out to be easier to check wich is the cheapest car from olx.

## Required:
Python 3 and Mongodb on localhost:27017 (or change the url on the constants file to your mongoUrl)

## Needed:
Download chromedrive.exe compatible with your google chrome version on their website

After everything configured you will need to run:

pip install -r requirements.txt

and to run the project API execute this in the terminal at the project folder:

python -m flask -A app.py --debug run

If you just want to run the webcrawler just run the:

python updateDatabase.py