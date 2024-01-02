import os
import re
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

load_dotenv()

def scrape_hdrezka_film():
    
    while True: 
        try:
            film_name = input("Enter film name: ")
            formatted_film_name = '+'.join(film_name.split())
            url = f"https://rezka.ag/search/?do=search&subaction=search&q={formatted_film_name}"

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            films = []

            for title_element in soup.find_all('div', class_='b-content__inline_item-link'):
                url = title_element.find('a')['href'].strip()
                films.append({'url': url})    

            response = requests.get(films[0]['url'], headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            title_element = soup.find('div', class_='b-post__origtitle', itemprop='alternativeHeadline')
            title = title_element.text.strip() if title_element else "Title not found"
            print(title)

            film_found = input("Is this the film you were looking for? (1/0): ")
            if film_found == '1':
                break
        except Exception as e:
            print(f"An error occurred: {e}")
     

    film_url = url

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = os.getenv('CHROME_BINARY_LOCATION')

    service = Service(os.getenv('CHROMEDRIVER_LOCATION'))

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(film_url)

    driver.execute_script("console.log = function() {window.log.push(Array.from(arguments))}; window.log = [];")

    translator_elements = driver.find_elements(By.CSS_SELECTOR, '.b-translator__item[data-translator_id]')


    options = []
    if translator_elements:
        for i, element in enumerate(translator_elements):
            translator_id = element.get_attribute('data-translator_id')
            title = element.get_attribute('title')
            options.append((title, translator_id))
            print(f'{i+1}. {title}')
    else:
        print("No translators found. Available options:")

    if translator_elements:
        choice = int(input("Enter the number of your choice: ")) - 1
        chosen_option = options[choice]
        print(f"You chose: {chosen_option[0]} {chosen_option[1]}")

    with open('script.js', 'r') as file:
        original_js_code = file.read()

    if translator_elements:
        modified_js_code = original_js_code.replace('data-translator_id="ID"', f'data-translator_id="{chosen_option[1]}"')
    else:
        modified_js_code = original_js_code

    if translator_elements:
        with open('script.js', 'w') as file:
            file.write(modified_js_code)

    driver.execute_script(modified_js_code)

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