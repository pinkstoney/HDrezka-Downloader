import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time

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

    translator_elements = driver.find_elements(By.CSS_SELECTOR, '.b-translator__item[data-translator_id]')
    options = []
    for i, element in enumerate(translator_elements):
       translator_id = element.get_attribute('data-translator_id')
       title = element.get_attribute('title')
       options.append((title, translator_id))
       print(f'{i+1}. {title} {translator_id}') 

    choice = int(input("Enter the number of your choice: ")) - 1
    chosen_option = options[choice]
    print(f"You chose: {chosen_option[0]} {chosen_option[1]}")

    with open('script.js', 'r') as file:
        original_js_code = file.read()

    # Replace the hardcoded translator_id with the chosen one
    modified_js_code = original_js_code.replace('data-translator_id="ID"', f'data-translator_id="{chosen_option[1]}"')

    with open('script.js', 'w') as file:
        file.write(modified_js_code)

    driver.execute_script(modified_js_code)

    # Write the original code back to the file
    with open('script.js', 'w') as file:
        file.write(original_js_code)

    time.sleep(1)

    logs = driver.execute_script("return window.log")

    quality_keywords = ["[360p]", "[480p]", "[720p]", "[1080p]", "[1080p Ultra]", "[1440p]", "[2160p]"]

    

    for log in logs:
        log_str = ' '.join(str(x) for x in log)
        for keyword in quality_keywords:
            if keyword in log_str:
                match = re.search(f'{re.escape(keyword)}(.*?).mp4', log_str)
                if match:
                    print(f'{keyword} {match.group(1)}.mp4') 

    driver.quit()

scrape_hdrezka_film()
