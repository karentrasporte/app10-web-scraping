import requests
import selectorlib
import smtplib, ssl
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    """"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "traspo811@gmail.com"
    password = ""

    receiver = "traspo811@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email sent!")


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events where band=? and city=? and date=?", (band, city,date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        print(extracted)
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="Subject: New Tours! \n Hey, new event was found!")
        time.sleep(2)
