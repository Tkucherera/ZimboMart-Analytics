import csv 

# we intend to clean the data a bit to make it more usable and consistent
# e.g., remove currency symbols, standardize area units, etc.


classifieds = '../data/classifieds-properties.csv'
property = '../data/properties.csv'

def clean_data(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='a', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Skip header in input file
        next(reader, None)

        for row in reader:
            date, title, price, neighbourhood, city, building_area, land_area, bedrooms, bathrooms = row
            
            # Clean price
            if price:
                price = price.replace('USD', '').replace('$', '').replace(',', '').strip()
                price_digits = ''.join(filter(str.isdigit, price))
                price = price_digits if price_digits else None
            
            # Clean building area
            if building_area:
                building_area = building_area.replace('m²', '').replace('sqm', '').replace(',', '').strip()
                building_area = ''.join(filter(str.isdigit, building_area))
                building_area = building_area if building_area else None
            
            # Clean land area
            if land_area:
                land_area = land_area.replace('m²', '').replace('sqm', '').replace(',', '').strip()
                land_area = ''.join(filter(str.isdigit, land_area))
                land_area = land_area if land_area else None
            
            # Clean bedrooms and bathrooms
            if bedrooms:
                bedrooms = ''.join(filter(str.isdigit, bedrooms))
                bedrooms = bedrooms if bedrooms else None
            if bathrooms:
                bathrooms = ''.join(filter(str.isdigit, bathrooms))
                bathrooms = bathrooms if bathrooms else None
            
            writer.writerow([date, title, price, neighbourhood, city, building_area, land_area, bedrooms, bathrooms])

# Clean both files and save to a new consolidated file
cleaned_file = '../data/cleaned-properties.csv'
with open(cleaned_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Date','Title', 'Price (USD)', 'Neighbourhood', 'City', 'Building Area (sqm)', 'Land Area (sqm)', 'Bedrooms', 'Bathrooms'])
clean_data(classifieds, cleaned_file)
clean_data(property, cleaned_file)
        