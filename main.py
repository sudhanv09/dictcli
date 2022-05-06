#!/usr/bin/env python3

import json
import requests
import rich
import argparse

api_url =  "https://api.dictionaryapi.dev/api/v2/entries/en/"
keywords = ['word', 'partOfSpeech', 'definition']
parser = argparse.ArgumentParser()
parser.add_argument('word', type=str)
args = parser.parse_args()


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k in key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

response = requests.get(api_url + args.word).json()
out = json_extract(response, keywords)

rich.print(f'[sea_green2]Word[/sea_green2]: [bright_yellow]{out[0]}[/bright_yellow]')
rich.print(f'[sea_green2]Part of Speech[/sea_green2]: [dark_turquoise]{out[1]}[/dark_turquoise]')
for i in out[2:]:
    rich.print(f'[sea_green2]Definition[/sea_green2]: [gold3]{i}[/gold3]\n')
