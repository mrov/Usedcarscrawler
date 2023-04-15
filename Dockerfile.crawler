FROM python:3.8-slim

WORKDIR /usedcarscrawler

RUN apt-get update

RUN apt-get install wget -y

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

RUN google-chrome --version

RUN apt-get install unzip

RUN wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip

RUN unzip chromedriver_linux64.zip

RUN rm google-chrome-stable_current_amd64.deb

RUN rm chromedriver_linux64.zip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV MONGO_URI=${MONGO_URI}

ENV CHROME_DRIVE_LOCATION=${CHROME_DRIVE_LOCATION}

RUN ls

CMD ["python", "./updateDatabase.py"]