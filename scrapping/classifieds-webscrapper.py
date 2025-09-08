from bs4 import BeautifulSoup as bs
from webscrapper import Property
import datetime
import os
import csv



def get_property_details(soup) -> list[Property]:
    properties = []
    for listing in soup.find_all('div', class_='details'):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = listing.find('h5', class_='listing-title').text.strip()
        price = listing.find('div', class_='usd-price-tooltip').text.strip()
        price = price.replace('\n', '').replace('$', '').replace(',', '').strip()

        # location 
        neihbourhood = title.split('-')[0].strip() if '-' in title else None
        amenities = listing.find_all('li', class_='property')
        bedrooms = bathrooms = land_area = None
        for li in amenities:
            if 'bedrooms' in li.text:
                bedrooms = li.text.strip().split(' ')[0]
            if 'bathrooms' in li.text:
                bathrooms = li.text.strip().split(' ')[0]
            if 'm²' in li.text:
                land_area = li.text.strip().split(' ')[0]
        city = amenities[-1].text.strip() if amenities else None
        details = Property(date, title, price, neihbourhood, city, None, land_area, bedrooms, bathrooms)
        properties.append(details)

    return properties

with open('../data/classifieds-properties.csv', mode='a', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file) 
    for file in os.listdir('./scraped_files'):
        if file.startswith('classifieds') and file.endswith('.html'):    
            file = os.path.join('./scraped_files', file)
            print(f"Processing file: {file}")
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = bs(content, 'html.parser')
                properties = get_property_details(soup)
            
                
                for prop in properties:
                    writer.writerow([prop.date, prop.title, prop.price, prop.neighbourhood, prop.city, prop.building_area, prop.land_area, prop.bedrooms, prop.bathrooms])