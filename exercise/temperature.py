import requests
import selectorlib
import datetime
import time

URL = "http://programmer100.pythonanywhere.com"


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


def store(extracted):
    now = datetime.datetime.now()
    line = f"{now.strftime("%Y-%m-%d-%H-%M-%S")},{extracted}"
    with open("data.txt", "a") as file:
        file.write(line + "\n")


if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        store(extracted)
        time.sleep(2)

