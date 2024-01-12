from btoa import btoa, atob
import itertools
import re


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
