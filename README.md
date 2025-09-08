## Data Analytics Housing Market in Zimbambwe


## Problem

The housing market in Zimbabwe is hard to understand how it is trending and how valuations are being done. There are several problems l have encountered as someone in the diaspora trying to find investment opportunities in Zimbabwe. In Zimbabwe data is not easily accessible online and insights and analytics are even more difficult to come by. 

## Goals 
 - Scrap Real Estate Marketplace Sites to get the data l need 
 - Create a database to store this data
 - Get some simple data like mean, median, distribution etc from the data 
 - Visualize the Data 
 - Classify the Data
 - Draw insights from data 
 - Build inference, and AI models 

### SCRAPPING 
For the property.co.zw site it was easy just used the requests library and was able to scrap with ease 

The classifieds.co.zw site not so much it had cloudflare blocking automated software so had to try urllib and selenium to no success had to make some of the process manual. l am sure with some effort l would have made it work but learning scrapping is not the goal here 

- requests 
- beautifulSoup4
- python 
- csv 

### Saving Data to Database 
l already had the postgres13 database and pgAdmin4 on my local machine so l just used postgres SQL server as my database of choice. The SQL QUERY for the import into Postgres
managed to get 2814 rows. A bit on the low side but l will scrap more with time to get a more 
robust dataset

```
        CREATE TABLE properties
    (
        id serial PRIMARY KEY, 
        created_at TIMESTAMP,
        title character varying(255),
        price bigint,
        neighbourhood character varying(100),
        city character varying(100),
        building_area bigint,
        land_area bigint,
        bedrooms int,
        bathrooms int
    );

    COPY properties(created_at, title, price, neighbourhood, city, building_area, land_area, bedrooms, bathrooms)
    FROM '/home/tinashe/Desktop/Graduate_School/CSE_704_Data_Processing./projects/zimbabwe_housing/data/cleaned-properties.csv' DELIMITER ',' CSV HEADER;
```


### Some Simple Aggregate Stats 
Now that our data is in the database we now get some aggregate statistics to understand our data

|   PRICE       |    Value        |
|---------------|-----------------|
|  Mean Price   |    403 179      |
|  Max Price    |    45 000 000   |
|  Min Price    |    13           |
|   Count       |    2 798        |

|   Land Size   |    Value        |
|---------------|-----------------|
|  Mean Land    |    762 003      |
|  Max Land     |    266 380 000  |
|  Min Land     |    1            |
|   Count       |    733          |


From Just this we can tell that they are some details that seems weird but we will be able to see more are are dig deeper and visualize the data 

```
SELECT bedrooms, CAST(AVG(price) AS DECIMAL(10,2)) AS price
from properties
GROUP BY bedrooms
ORDER BY price DESC;
```

Did some more quiries to check the average price for number of bedrooms, land_area etc 

### Power BI 
1. Imported the CSV Data (model in Power BI) into Power BI. 
    - If l had a live SQL Database l would want to connect and get real live changing data 

2. Started a Report
    - The total Number of Properties that have a city associated with them in the data 
    - The average price on a Listing in the data 
    - The Average price of properties per city 
    - the number of listings per city 
    - From the Data what comes with an average home (beds, baths and land size)
3. Make Visuals for this and published to Power BI service 

4. Noted and what l learned
    - The Model is small, need to grab more data that when l start filtering l am not left with small set
    - Need more data from other areas cities 
    - Need Regional Data to be able to gain more Insights 

## Whats Next 

### Python 
1. We have some insights but l need to get more especially the distribution of the data
2. Need to make classifiers for the data 
3. Reggression model mostly for Valuation etc 








