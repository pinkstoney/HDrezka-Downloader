import requests
import re
from bs4 import BeautifulSoup

def find_films_list(film_name, headers):
    formatted_film_name = '+'.join(film_name.split())
    url = f"https://rezka.ag/search/?do=search&subaction=search&q={formatted_film_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    films = []

    for title_element in soup.find_all('div', class_='b-content__inline_item-link'):
        url = title_element.find('a')['href'].strip()
        films.append({'url': url})
        if len(films) == 5:
            break
    return films

def get_film_title(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('div', class_='b-post__origtitle', itemprop='alternativeHeadline')
    title = title_element.text.strip() if title_element else "Title not found"
    return title

def find_films_with_titles(film_name, headers):
    films = find_films_list(film_name, headers)
    for film in films:
        film['title'] = get_film_title(film['url'], headers)
    return films

def get_translators(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    translator_elements = soup.select('.b-translator__item[data-translator_id]')
    options = []
    if translator_elements:
        for i, element in enumerate(translator_elements):
            translator_id = element.get('data-translator_id')
            title = element.get('title')
            options.append((title, translator_id))
    return options

def get_seasons(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    season_elements = soup.select('.b-simple_season__item')
    seasons = []
    if season_elements:
        for element in season_elements:
            season = element.text
            seasons.append(season)
    return seasons

def get_episodes(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    episode_elements = soup.select('.b-simple_episode__item')
    episodes = []
    if episode_elements:
        for element in episode_elements:
            episode = element.text
            episodes.append(episode)
    return episodes

def find_source_with_hash(film_url, headers):
    response = requests.get(film_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if 'sof.tv.initCDNSeriesEvents' in script.text or 'sof.tv.initCDNMoviesEvents' in script.text:
            match = re.search(r'"streams":\s*"#([^"]*)', script.text)
            if match:
                return match.group(1)[1:]
    return None