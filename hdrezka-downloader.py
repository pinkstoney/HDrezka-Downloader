import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

load_dotenv()

def scrape_hdrezka_film():
    film_url = input("Enter HDrezka film URL: ")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = os.getenv('CHROME_BINARY_LOCATION')
    service = Service(os.getenv('CHROMEDRIVER_LOCATION'))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(film_url)

    driver.execute_script("console.log = function() {window.log.push(Array.from(arguments))}; window.log = [];")

    with open('script.js', 'r') as file:
        js_code = file.read()

    driver.execute_script(js_code)

    logs = driver.execute_script("return window.log")

    for log in logs:
        print(' '.join(str(x) for x in log))

    driver.quit()

scrape_hdrezka_film()
