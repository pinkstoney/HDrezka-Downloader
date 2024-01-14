import re
import requests
from tabulate import tabulate

from film_finder import find_films_with_titles, find_source_with_hash, get_translators, get_seasons, get_episodes, get_subtitles
from trash_cleaner import clear_trash, filter_output, clear_response, seasons_cleaner, episodes_cleaner, subtitles_cleaner, translator_cleaner

def choose_film(films):
    film_table = []
    for i, film in enumerate(films):
        film_table.append([i + 1, film["title"], film["url"]])

    print(tabulate(film_table, headers=["#", "Film Title", "URL"], tablefmt="fancy_grid"))

    choice = int(input("Choose a film: ")) - 1

    if 0 <= choice < len(films):
        return films[choice]["url"]
    else:
        print("Invalid choice. Please choose a valid option.")
        return None

def choose_season(seasons):
    cleaned_seasons = seasons_cleaner(seasons)
    season_table = []
    for i, season in enumerate(cleaned_seasons):
        season_table.append([i + 1, f"Season {season}"])

    print(tabulate(season_table, headers=["#", "Season"], tablefmt="fancy_grid"))

    season_choice = int(input("Choose a season: "))
    return season_choice

def choose_episode(episodes):
    cleaned_episodes = episodes_cleaner(episodes)
    episode_table = []
    for i, episode in enumerate(cleaned_episodes):
        episode_table.append([i + 1, f"Episode {episode}"])

    print(tabulate(episode_table, headers=["#", "Episode"], tablefmt="fancy_grid"))

    episode_choice = int(input("Choose an episode: "))
    return episode_choice

def choose_translator(translators):
    cleaned_translators = translator_cleaner(translators)

    translator_table = []
    for i, translator in enumerate(cleaned_translators):
        translator_table.append([i + 1, translator])

    print(tabulate(translator_table, headers=["#", "Translator"], tablefmt="fancy_grid"))

    translator_choice = int(input("Choose a translator: ")) - 1

    if 0 <= translator_choice < len(translators):
        chosen_translator = translators[translator_choice][:2]
        translator_id = chosen_translator[1]
        return translator_id
    else:
        print("Invalid choice. Please choose a valid option.")
        return None

if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    while True:
        film_name = input("Enter film name: ")
        films = find_films_with_titles(film_name, headers)

        if not films:
            print("No films found. Try a different search term.")
            continue

        chosen_film_url = choose_film(films)

        if chosen_film_url is None:
            continue

        seasons = get_seasons(chosen_film_url, headers)
        episodes = get_episodes(chosen_film_url, headers)

        if seasons:
            season_choice = choose_season(seasons)
            episode_choice = choose_episode(episodes)

        translators = get_translators(chosen_film_url, headers)

        if not translators:
            source_with_hash = find_source_with_hash(chosen_film_url, headers)
            if source_with_hash is not None:
                cleaned_source = clear_trash(source_with_hash)
                filtered_output = filter_output(cleaned_source)
                print(filtered_output)
            else:
                print("No source found for the chosen film.")
            break

        translator_id = choose_translator(translators)

        if translator_id is None:
            continue

        s = requests.Session()

        url = "https://rezka.ag/ajax/get_cdn_series/"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://rezka.ag",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
            "X-Requested-With": "XMLHttpRequest"
        }

        id = re.findall(r'/(\d+)-', chosen_film_url)[0]

        if seasons:
            get_film = "get_season"

            data = {
                "id": id,
                "translator_id": translator_id,
                "action": "get_stream",
                "season": season_choice,
                "episode": episode_choice
            }
        else:
            get_film = "get_movie"

            data = {
                "id": id,
                "translator_id": translator_id,
                "action": get_film
            }

        response = s.post("https://rezka.ag/ajax/get_cdn_series/", headers=headers, data=data)

        clean_response = clear_trash(clear_response(response.text))
        filtered_output = filter_output(clean_response)

        if translator_id == "238":
            clean_subtitles = subtitles_cleaner(get_subtitles(response.text))

            subtitle_entries = clean_subtitles.split('\n')

            subtitle_table = []
            for entry in subtitle_entries:
                if entry: 
                    language, url = entry.split(': ', 1)  
                    subtitle_table.append([language, url])

            print(tabulate(subtitle_table, headers=["Language", "URL"], tablefmt="fancy_grid"))
                

        output_entries = filtered_output.split('\n')

        output_table = []
        for entry in output_entries:
            if entry:
                quality, url = entry.split('] ', 1)
                quality = quality.replace('[', '')
                output_table.append([quality, url])

        print(tabulate(output_table, headers=["Qaulity", "URL"], tablefmt="fancy_grid"))

