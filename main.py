from film_finder import find_films_with_titles, find_source_with_hash, get_translators, get_seasons
from trash_cleaner import clear_trash, filter_output, clear_response
import requests
import re

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

            for i, film in enumerate(films):
                print(f'{i + 1}. {film["title"]} - {film["url"]}')

            choice = int(input("Choose a film: ")) - 1

            if 0 <= choice < len(films):
                chosen_film_url = films[choice]["url"]
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

                for i, translator in enumerate(translators):
                    print(f'{i + 1}. {translator}')

                translator_choice = int(input("Choose a translator: ")) - 1

                if 0 <= translator_choice < len(translators):
                    chosen_translator = translators[translator_choice][:2]
                    translator_id = chosen_translator[1]
                    print(f"You chose {chosen_translator}")

                    seasons = get_seasons(chosen_film_url, headers)

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
                            "season": "1",
                            "episode": "1"
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
                    print(filtered_output)


                else:
                    print("Invalid choice. Please choose a valid option.")
                break

                if seasons: print(seasons)
            else:
                print("Invalid choice. Please choose a valid option.")

