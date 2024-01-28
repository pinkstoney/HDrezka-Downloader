import os
import re
import requests

from colorama import Fore, Style
from art import *
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from pyshorteners import Shortener

from film_finder import (
    find_films_with_titles,
    find_source_with_hash,
    get_translators,
    get_seasons,
    get_episodes,
    get_subtitles,
)
from trash_cleaner import (
    clear_trash,
    filter_output,
    clear_response,
    seasons_cleaner,
    episodes_cleaner,
    subtitles_cleaner,
    translator_cleaner,
)

console = Console()


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def show_main_menu():
    console.clear()
    art = text2art("HDrezka-Downloader")
    console.print(Panel(art, style="violet"))

    console.print("[1] Search films")
    console.print("[2] GitHub")
    console.print("[3] Exit")


def choose_film(films):
    while True:
        table = Table(show_header=True, header_style="magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Film Title", style="green")

        for i, film in enumerate(films):
            table.add_row(str(i + 1), film["title"])

        console.clear()
        console.print(table)

        film_choice = int(input("Choose a film: ")) - 1
        if 0 <= film_choice < len(films):
            return films[film_choice]["url"]
        else:
            rprint("[red]Invalid choice. Please choose a valid option.[/red]")
            input("Press enter to try again...")


def choose_season(seasons):
    cleaned_seasons = seasons_cleaner(seasons)
    while True:
        table = Table(show_header=True, header_style="magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Season", style="green")

        for i, season in enumerate(cleaned_seasons):
            table.add_row(str(i + 1), f"Season {season}")

        console.clear()
        console.print(table)

        season_choice = int(input("Choose a season: "))
        if 0 < season_choice <= i + 1:
            return season_choice
        else:
            rprint("[red]Invalid choice. Please choose a valid option.[/red]")
            input("Press enter to try again...")


def choose_episode(episodes):
    cleaned_episodes = episodes_cleaner(episodes)
    while True:
        table = Table(show_header=True, header_style="magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Episode", style="green")

        for i, episode in enumerate(cleaned_episodes):
            table.add_row(str(i + 1), f"Episode {episode}")

        console.clear()
        console.print(table)

        episode_choice = int(input("Choose an episode: "))
        if 0 < episode_choice <= i + 1:
            return episode_choice
        else:
            rprint("[red]Invalid choice. Please choose a valid option.[/red]")
            input("Press enter to try again...")


def choose_translator(translators):
    cleaned_translators = translator_cleaner(translators)
    while True:
        table = Table(show_header=True, header_style="magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Translator", style="green")

        for i, translator in enumerate(cleaned_translators):
            table.add_row(str(i + 1), translator)

        console.clear()
        console.print(table)

        translator_choice = int(input("Choose a translator: ")) - 1
        if 0 <= translator_choice < len(translators):
            chosen_translator = translators[translator_choice][:2]
            translator_id = chosen_translator[1]
            return translator_id
        else:
            rprint("[red]Invalid choice. Please choose a valid option.[/red]")
            input("Press enter to try again...")


def search_films():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    while True:
        console_width = console.width
        console.print("\n" + "#" * console_width, style="dark_sea_green")
        film_name = input("Enter film name: ")
        films = find_films_with_titles(film_name, headers)

        if not films:
            print(Fore.YELLOW + "No films found. Try a different search term." + Style.RESET_ALL)
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
                print(Fore.YELLOW + "No source found for the chosen film." + Style.RESET_ALL)
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

            table = Table(show_header=True, header_style="magenta")
            table.add_column("Language", style="green")
            table.add_column("URL", style="green")

            for entry in subtitle_entries:
                if entry:
                    language, url = entry.split(': ', 1)
                    table.add_row(language, url)

            console.clear()
            console.print("Subtitles:", style="light_slate_blue")
            console.print(table)


        output_entries = filtered_output.split('\n')

        output_table = Table(show_header=True, header_style="magenta")
        output_table.add_column("Quality", style="green")
        output_table.add_column("URL", style="green")

        for entry in output_entries:
            if entry:
                quality, url = entry.split('] ', 1)
                quality = quality.replace('[', '')
                
                shortener = Shortener()
                short_url = shortener.tinyurl.short(url)

                url_text = Text(short_url, overflow="fold")
                output_table.add_row(quality, url_text)

        console.print("Video sources:", style="light_slate_blue")
        console.print(output_table)


if __name__ == "__main__":
    while True:
        show_main_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            search_films()
        elif choice == "2":
            console.clear()
            console.print('[light_steel_blue]GitHub Repository:[/light_steel_blue]')
            console.print('https://github.com/pinkstoney/HDrezka-Downloader.git')
            input("Press enter to go back to the main menu...")
            show_main_menu()

        elif choice == "3":
            break
        else:
            rprint("[red]Invalid choice. Please choose a valid option.[/red]")
            input("Press enter to try again...")
