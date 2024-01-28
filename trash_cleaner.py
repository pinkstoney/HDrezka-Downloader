import itertools
import re

from btoa import btoa, atob

def clear_trash(data):
    trash_list = ["@", "#", "!", "^", "$"]
    two = [''.join(i) for i in itertools.product(trash_list, repeat=2)]
    three = [''.join(i) for i in itertools.product(trash_list, repeat=3)]
    trash_codes_set = two + three

    arr = data.replace("#h", "").split("//_//")
    trash_string = ''.join(arr)

    for i in trash_codes_set:
        temp = btoa(i)
        trash_string = trash_string.replace(temp, '')

    final_string = atob(trash_string)

    final_string = re.sub(r'[^\x00-\x7F]+', '', final_string)

    return final_string


def filter_output(output):
    quality_keywords = ["[360p]", "[480p]", "[720p]", "[1080p]", "[1080p Ultra]", "[1440p]", "[2160p]"]
    lines = output.split(',')
    filtered_output = []
    for line in lines:
        for keyword in quality_keywords:
            if keyword in line:
                link = re.search(r'https?://\S+\.mp4', line)
                if link:
                    link = link.group()
                    if not link.startswith('https://stream.voidboost.cc/'):
                        link = re.sub(r'https?://\S+/', 'https://stream.voidboost.cc/', link)
                    filtered_output.append(f'{keyword} {link}')
                    break
    return '\n'.join(filtered_output)


def clear_response(data):
    start_index = data.find("#h")

    if start_index != -1:
        end_index = data.find('"', start_index)

        if end_index != -1:
            return data[start_index + 2:end_index]
        else:
            return "No double quote found after '#h'."

    else:
        return "No '#h' found in the input string."

def seasons_cleaner(seasons):
    cleaned_seasons = []
    last_season = 0
    for season in seasons:
        season_numbers = re.findall(r'\d+', season)
        for number in season_numbers:
            number = int(number)
            if number > last_season:
                cleaned_seasons.append(number)
                last_season = number
            else:
                return cleaned_seasons
    return cleaned_seasons

def episodes_cleaner(episodes):
    cleaned_episodes = []
    last_episode = 0
    for episode in episodes:
        episode_numbers = re.findall(r'\d+', episode)  # Find all numbers in the string
        for number in episode_numbers:
            number = int(number)
            if number > last_episode:
                cleaned_episodes.append(number)
                last_episode = number
            else:
                return cleaned_episodes 
    return cleaned_episodes

def translator_cleaner(translators):
    cleaned_translators = []
    for translator in translators:
        name = translator[0].split('(')[0].strip()
        if "Украинский дубляж" in name:
            name = name.replace("Украинский", "Український") + " (ua)"
        elif "Украинский многоголосый" in name:
            name = name.replace("Украинский многоголосый", "Український багатоголосий закадровий") + " (ua)"
        elif "Оригинал" in name:
            name = name.replace("Оригинал", "Original")
        else:
            name += " (ru)"
        cleaned_translators.append(name)
    return cleaned_translators

def subtitles_cleaner(subtitles_dict):
    cleaned_subtitles = ""

    for language, url in subtitles_dict.items():
        cleaned_subtitles += f"{language}: {url}\n"

    return cleaned_subtitles