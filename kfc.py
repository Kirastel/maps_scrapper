import requests
import json


def get_data_from_api():
    try:
        url = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
        response = requests.get(url)
        data_json = response.json()
        print('')
    except Exception as e:
        print(f'Error when requesting "https://api.kfc.com" is {e}')
        data_json = None

    return data_json


def get_list_of_kfc():
    data = get_data_from_api()
    if data is None:
        return f'Failed to collect data'

    list_of_restaurants = []
    for value in data.get('searchResults'):
        value = value['storePublic']

        try:
            adress = value['contacts']['streetAddress']['ru']
        except KeyError:
            adress = ''

        try:
            latlon = value['contacts']['coordinates']['geometry']['coordinates']
        except KeyError:
            latlon = ''

        try:
            name = value['title']['ru']
        except KeyError:
            name = ''

        try:
            phones = value['contacts']['phoneNumber']
        except KeyError:
            phones = []

        if value['status'] == 'closed':
            working_hours = 'closed'
        else:
            open_at = value['openingHours']['regular']['startTimeLocal']
            closed_at = value['openingHours']['regular']['endTimeLocal']
            working_hours = [
                f'пн-пт {open_at} - {closed_at}',
                f'сб-вс {open_at} - {closed_at}'
            ]

        list_of_restaurants.append({
            'adress': adress,
            'latlong': latlon,
            'name': name,
            'phones': phones,
            'working_hours': working_hours
        })
    print('The list of restaurants is formed.')
    return list_of_restaurants




