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

def get_film_url(film_name, headers):
    formatted_film_name = '+'.join(film_name.split())
    url = f"https://rezka.ag/search/?do=search&subaction=search&q={formatted_film_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    films = []
    for title_element in soup.find_all('div', class_='b-content__inline_item-link'):
        url = title_element.find('a')['href'].strip()
        films.append({'url': url})    
    return films[0]['url']

def get_film_title(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('div', class_='b-post__origtitle', itemprop='alternativeHeadline')
    title = title_element.text.strip() if title_element else "Title not found"
    return title

def get_film_image(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    image_element = soup.find('div', class_='b-sidecover').find('a')
    image_url = image_element['href'].strip() if image_element else "Image not found"
    return image_url

def save_film_image(film_url, headers, image_path):
    image_url = get_film_image(film_url, headers)
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(image_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def download_video(chosen_log, video_path):
    video_url = chosen_log.split(' ', 1)[1]
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with open(video_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def get_translator_options(driver):
    translator_elements = driver.find_elements(By.CSS_SELECTOR, '.b-translator__item[data-translator_id]')
    options = []
    if translator_elements:
        for i, element in enumerate(translator_elements):
            translator_id = element.get_attribute('data-translator_id')
            title = element.get_attribute('title')
            options.append((title, translator_id))
    return options

def modify_js_code(options, choice, original_js_code):
    chosen_option = options[choice]
    modified_js_code = original_js_code.replace('data-translator_id="ID"', f'data-translator_id="{chosen_option[1]}"')
    return modified_js_code, chosen_option

def get_quality_keywords(logs, quality_keywords):
    quality_logs = []
    for log in logs:
        log_str = ' '.join(str(x) for x in log)
        for keyword in quality_keywords:
            if keyword in log_str:
                match = re.search(f'{re.escape(keyword)}(.*?).mp4', log_str)
                if match:
                    quality_logs.append(f'{keyword} {match.group(1)}.mp4')
    return quality_logs

def create_urls_file(title, quality_logs):
    with open(f'data/selected/{title}_url.txt', 'w') as file:
        for log in quality_logs:
            file.write(f'{log}\n')

def scrape_hdrezka_film():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    while True: 
        try:
            film_name = input("Enter film name: ")
            film_url = get_film_url(film_name, headers)
            title = get_film_title(film_url, headers)
            print('\n'+ title)
            film_found = input("Is this the film you were looking for? (1/0): ")
            if film_found == '1':
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = os.getenv('CHROME_BINARY_LOCATION')
    service = Service(os.getenv('CHROMEDRIVER_LOCATION'))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(film_url)
    driver.execute_script("console.log = function() {window.log.push(Array.from(arguments))}; window.log = [];")
    options = get_translator_options(driver)

    if options:
        print('\n')
        for i, option in enumerate(options):
            print(f'{i+1}. {option[0]}')
    else:
        print("\nNo translations found. Available options:")
    
    if options:
        choice = int(input("Choose translation: ")) - 1
    
    original_js_code = read_js_code_from_file('script.js')
    
    if options:
        modified_js_code, chosen_option = modify_js_code(options, choice, original_js_code)
        print(f"You chose: {chosen_option[0]}\n")
        write_js_code_to_file('script.js', modified_js_code)
        driver.execute_script(modified_js_code)
        
    time.sleep(1)
    logs = driver.execute_script("return window.log")
    quality_keywords = ["[360p]", "[480p]", "[720p]", "[1080p]", "[1080p Ultra]", "[1440p]", "[2160p]"]
    quality_logs = get_quality_keywords(logs, quality_keywords)
    driver.quit()

    write_js_code_to_file('script.js', original_js_code)

    if quality_logs:
        for i, log in enumerate(quality_logs):
            print(f'{i+1}. {log}')
        choice = int(input("Choose quality: ")) - 1
        chosen_log = quality_logs[choice]
        print(f"Downloading: {chosen_log}")
        create_urls_file(title, [chosen_log])
    else:
        print("No quality options found.")

    image_path = f"data/selected/images/{title}.jpg"
    save_film_image(film_url, headers, image_path)

    video_path = f"data/selected/videos/{title}.mp4"
    download_video(chosen_log, video_path)

def get_film_url(film_name, headers):
    formatted_film_name = '+'.join(film_name.split())
    url = f"https://rezka.ag/search/?do=search&subaction=search&q={formatted_film_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    films = []
    for title_element in soup.find_all('div', class_='b-content__inline_item-link'):
        url = title_element.find('a')['href'].strip()
        films.append({'url': url})    
    return films[0]['url']

def get_film_title(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('div', class_='b-post__origtitle', itemprop='alternativeHeadline')
    title = title_element.text.strip() if title_element else "Title not found"
    return title

def get_translator_options(driver):
    translator_elements = driver.find_elements(By.CSS_SELECTOR, '.b-translator__item[data-translator_id]')
    options = []
    if translator_elements:
        for i, element in enumerate(translator_elements):
            translator_id = element.get_attribute('data-translator_id')
            title = element.get_attribute('title')
            options.append((title, translator_id))
    return options

def modify_js_code(options, choice, original_js_code):
    chosen_option = options[choice]
    modified_js_code = original_js_code.replace('data-translator_id="ID"', f'data-translator_id="{chosen_option[1]}"')
    return modified_js_code, chosen_option

def get_quality_keywords(logs, quality_keywords):
    quality_logs = []
    for log in logs:
        log_str = ' '.join(str(x) for x in log)
        for keyword in quality_keywords:
            if keyword in log_str:
                match = re.search(f'{re.escape(keyword)}(.*?).mp4', log_str)
                if match:
                    quality_logs.append(f'{keyword} {match.group(1)}.mp4')
    return quality_logs

def create_urls_file(title, quality_logs):
    with open(f'data/selected/{title}_url.txt', 'w') as file:
        for log in quality_logs:
            file.write(f'{log}\n')

def read_js_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_js_code_to_file(file_path, js_code):
    with open(file_path, 'w') as file:
        file.write(js_code)

def download_video(chosen_log, video_path):
    video_url = chosen_log.split(' ', 1)[1]
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with open(video_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def save_film_image(film_url, headers, image_path):
    image_url = get_film_image(film_url, headers)
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(image_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def get_film_image(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    image_element = soup.find('div', class_='b-sidecover').find('a')
    image_url = image_element['href'].strip() if image_element else "Image not found"
    return image_url

scrape_hdrezka_film()
