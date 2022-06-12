import requests
from bs4 import BeautifulSoup
import json
import re


def get_json_from_site():
    """
    The function receives the json and deserializes it.
    """
    try:
        url = 'https://www.ziko.pl/wp-admin/' \
              'admin-ajax.php?action=get_pharmacies'
        response = requests.get(url)
        soup = response.text
        js = json.loads(soup)
        return js
    except Exception as e:
        print(f'Error when requesting "https://www.ziko.pl" is {e}')


def get_list_of_ziko():
    try:
        js = get_json_from_site()
    except Exception as e:
        return ['No data']
    list_of_shops = []
    for item in js:
        address = js[item]['address']
        latlon = [float(js[item]['lat']), float(js[item]['lng'])]
        name = js[item]['title']
        working_hours = js[item]['mp_pharmacy_hours']
        working_hours_unformating = re.split(r'<br>', working_hours)
        working_hours = working_hours_formatting(working_hours_unformating)
        list_of_shops.append(
            {
                'address': address,
                'latlon': latlon,
                'name': name,
                'working_hours': working_hours,
            }
        )
    print('The list of ziko shops is formed.')
    return list_of_shops


def working_hours_formatting(data: list) -> list:
    """
    The function takes a list with working hours strings
     and returns a list with formatted strings
    """
    new_data = []
    for i in range(len(data)):
        if not data[i]:
            continue
        if data[i] in ('niedziela handlowa', 'niedziela niehandlowa'):
            new_data.append(f'{data[i]} - {data[i + 1]}')
        elif data[i].startswith('pon') or data[i].startswith('sb'):
            new_data.append(data[i])
    return new_data

