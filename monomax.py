import json
import re
import requests
from bs4 import BeautifulSoup
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


def get_html():
    try:
        url = 'https://monomax.by/map'
        response = requests.get(url)
        soup = response.text
        with open('MONOMAX.html', "w", encoding="utf-8") as file:
            file.write(soup)
    except Exception as e:
        print(f'Error when requesting "https://monomax.by/map" is {e}')


def get_list_of_monomax():
    get_html()
    try:
        with open('MONOMAX.html', encoding='utf-8') as file:
            f = file.read()
        soup = BeautifulSoup(f, 'lxml')
        script = soup.find_all('script')[-1]
    except Exception as e:
        print(f'[ERROR] {e}')
        return ['No data']

    data_from_html = []
    parser = Parser()
    tree = parser.parse(script.text)
    for node in nodevisitor.visit(tree):
        if isinstance(node, ast.Assign):
            value = getattr(node.right, 'value', '')
            if value:
                data_from_html.append(value)

    phones = [data_from_html[i].replace('Телефон: ', '').replace(' ', '')
              for i in range(0, len(data_from_html), 3)][1:]
    addresses = [data_from_html[i]
                 for i in range(1, len(data_from_html), 3)][1:]

    coordinates = re.findall(r'Placemark\(\s*\[(\d+\.?\d+),\s*(\d+\.?\d+)]', script.string)

    list_of_monomax = []
    for i in range(len(phones)):
        phone = [phones[i]]
        address = addresses[i]
        latlon = list(map(lambda x: float(x), coordinates[i]))
        list_of_monomax.append({
            'adress': address,
            'latlon': latlon,
            'name': 'Мономах',
            'phones': phone
        })
    print('The list of monomax shops is formed.')
    return list_of_monomax


