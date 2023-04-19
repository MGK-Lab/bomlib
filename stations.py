import requests
from bs4 import BeautifulSoup
import json
import re


def convert_url(url):
    base_url = 'http://reg.bom.gov.au/fwo'
    path_parts = url.split('/')
    station_id = path_parts[2]
    file_name = path_parts[3].replace('.shtml', '.axf')
    new_url = f'{base_url}/{station_id}/{file_name}'
    return new_url


class Stations:

    def __init__(self):
        self.stations = []

    def get_stations(self, url):
        # Make a request to the URL and get the HTML content
        response = requests.get(url)
        content = response.content

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')

        # Find all table rows with class "rowleftcolumn"
        rows = soup.find_all('tr', class_='rowleftcolumn')

        # Loop through the rows and extract the station information
        for row in rows:
            # Find the station name and URL
            name_link = row.find('th').find('a')
            name = name_link.string.strip()
            link = name_link['href']
            link = convert_url(link)

            # Create a dictionary to store the station information
            station = {'name': name, 'link': link}

            # Add the dictionary to the list of stations
            self.stations.append(station)

    def save_stations(self, output_file):
        with open(output_file, 'w') as f:
            json.dump(self.stations, f)

    def load_stations(self, input_file):
        with open(input_file, 'r') as f:
            self.stations = json.load(f)

    def station_names(self):
        names = [station['name'] for station in self.stations]
        return names

    def link_by_station_name(self, name):
        for station in self.stations:
            if station['name'] == name:
                return station['link']

        return None
