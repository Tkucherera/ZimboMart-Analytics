"""
Author: Tinashe Kucherera
Date: 2024-10-01
Description: A web scraper to extract property listings from a real estate website and save them to a CSV file.

"""

import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime 



class Property:    
    def __init__(self, date, title, price, neighbourhood, city, building_area, land_area, bedrooms, bathrooms):
        self.date = date
        self.title = title
        self.price = price
        self.neighbourhood = neighbourhood
        self.city = city
        self.building_area = building_area
        self.land_area = land_area
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms

def get_property_details(soup) -> list[Property]:
    properties = []
    listings = soup.find_all('div', class_='MainBody')

    for listing in listings:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = listing.find('h2', class_='mb-0.5').text.strip()
        price = listing.find('div', class_='result-price').text.strip()

        # Location is Neighbourhood and City separated by a comma
        location_div = listing.find('div', class_='text-graypurpledark')
        location = location_div.text.strip() if location_div else None
        neighbourhood, city = (location.split(',') + [None])[:2]

        # ammenities
        buiding_area = listing.find('span', class_='building-area').text.strip() if listing.find('span', class_='building-area') else None
        land_area = listing.find('span', class_='land-area').text.strip() if listing.find('span', class_='land-area') else None
        bedrooms = listing.find('span', class_='bed').text.strip() if listing.find('span', class_='bedrooms') else None
        bathrooms = listing.find('span', class_='bath').text.strip() if listing.find('span', class_='bathrooms') else None

        details = Property(date, title, price, neighbourhood, city, buiding_area, land_area, bedrooms, bathrooms)
        properties.append(details)


    return properties



def get_next_page(soup) -> str:
    next_page = soup.find('link', rel='next')
    if next_page:
        return next_page['href']
    return None


def get_properties_from_site(url) -> list[Property]:
    properties = []
    while url:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        properties.extend(get_property_details(soup))
        url = get_next_page(soup)
    return properties


def save_properties_to_file(properties, filename='./data/properties.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Neighbourhood', 'City', 'Building Area', 'Land Area', 'Bedrooms', 'Bathrooms'])
        for prop in properties:
            writer.writerow([prop.title, prop.price, prop.neighbourhood, prop.city, prop.building_area, prop.land_area, prop.bedrooms, prop.bathrooms])


if __name__ == '__main__':
    url = 'https://www.property.co.zw/property-for-sale'
    properties = get_properties_from_site(url)
    save_properties_to_file(properties)

