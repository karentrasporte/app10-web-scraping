import requests
import selectorlib
import datetime
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com"

connection = sqlite3.connect("../data.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    """"""
    extractor = selectorlib.Extractor.from_yaml_file("../extract.yaml")
    value = extractor.extract(source)["temp"]
    return value


def store(temp):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperature VALUES (?,?)", (now,temp))
    connection.commit()


if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        store(extracted)
        time.sleep(2)

