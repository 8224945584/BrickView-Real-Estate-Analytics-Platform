# %%
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="700234OMk#",
    database="real_estate"
)

cursor = conn.cursor()
# %%
# Property & Pricing Analysis
#1. What is the average listing price by city?


#Coding

query = """
SELECT
    city,
    ROUND(AVG(price), 2) AS average_listing_price
FROM listings
GROUP BY city
ORDER BY average_listing_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

#Display

import pandas as pd

query = """
SELECT
    city,
    ROUND(AVG(price), 2) AS average_listing_price
FROM listings
GROUP BY city
ORDER BY average_listing_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

avg_price_df = pd.DataFrame(
    rows,
    columns=["City", "Average Listing Price"]
)

avg_price_df


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.bar(avg_price_df["City"], avg_price_df["Average Listing Price"])
plt.title("Average Listing Price by City")
plt.xlabel("City")
plt.ylabel("Average Listing Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# %%
# Property & Pricing Analysis
#2. What is the average price per square foot by property type?


#Coding

query = """
SELECT
    property_type,
    ROUND(AVG(price / sqft), 2) AS avg_price_per_sqft
FROM listings
WHERE sqft > 0
GROUP BY property_type
ORDER BY avg_price_per_sqft DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

query = """
SELECT
    property_type,
    ROUND(AVG(price / sqft), 2) AS avg_price_per_sqft
FROM listings
WHERE sqft > 0
GROUP BY property_type
ORDER BY avg_price_per_sqft DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

price_sqft_df = pd.DataFrame(
    rows,
    columns=["Property Type", "Average Price per Sq. Ft."]
)

print(price_sqft_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.bar(price_sqft_df["Property Type"], price_sqft_df["Average Price per Sq. Ft."])

plt.title("Average Price per Square Foot by Property Type")
plt.xlabel("Property Type")
plt.ylabel("Average Price per Sq. Ft.")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# %%
# Property & Pricing Analysis
#3. How does furnishing status impact property prices?


#Coding

query = """
SELECT
    pa.furnishing_status,
    ROUND(AVG(l.price), 2) AS average_property_price,
    COUNT(*) AS total_properties
FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id
GROUP BY pa.furnishing_status
ORDER BY average_property_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

query = """
SELECT
    pa.furnishing_status,
    ROUND(AVG(l.price), 2) AS average_property_price,
    COUNT(*) AS total_properties
FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id
GROUP BY pa.furnishing_status
ORDER BY average_property_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

furnishing_df = pd.DataFrame(
    rows,
    columns=[
        "Furnishing Status",
        "Average Property Price",
        "Number of Properties"
    ]
)

print(furnishing_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

plt.bar(
    furnishing_df["Furnishing Status"],
    furnishing_df["Average Property Price"]
)

plt.title("Average Property Price by Furnishing Status")
plt.xlabel("Furnishing Status")
plt.ylabel("Average Property Price")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()

# %%
# Property & Pricing Analysis
#4. Do properties closer to metro stations command higher prices?


# Coding

query = """
SELECT
    CASE
        WHEN pa.metro_distance_km <= 1 THEN '0-1 km'
        WHEN pa.metro_distance_km <= 3 THEN '1-3 km'
        WHEN pa.metro_distance_km <= 5 THEN '3-5 km'
        ELSE 'Above 5 km'
    END AS metro_distance_range,

    ROUND(AVG(l.price),2) AS average_price,
    COUNT(*) AS total_properties

FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id

GROUP BY metro_distance_range

ORDER BY
CASE
    WHEN metro_distance_range='0-1 km' THEN 1
    WHEN metro_distance_range='1-3 km' THEN 2
    WHEN metro_distance_range='3-5 km' THEN 3
    ELSE 4
END;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

metro_df = pd.DataFrame(
    rows,
    columns=[
        "Metro Distance",
        "Average Price",
        "Number of Properties"
    ]
)

print(metro_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

plt.bar(
    metro_df["Metro Distance"],
    metro_df["Average Price"]
)

plt.title("Average Property Price by Distance from Metro")
plt.xlabel("Distance from Metro")
plt.ylabel("Average Property Price")

plt.tight_layout()
plt.show()
# %%
#Property & Pricing Analysis
#5. Are rented properties priced differently from non-rented ones?
query = """
SELECT
    CASE
        WHEN pa.is_rented = 1 THEN 'Rented'
        ELSE 'Not Rented'
    END AS rental_status,

    ROUND(AVG(l.price), 2) AS average_price,
    COUNT(*) AS total_properties

FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id

GROUP BY pa.is_rented

ORDER BY average_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

rented_df = pd.DataFrame(
    rows,
    columns=[
        "Rental Status",
        "Average Price",
        "Number of Properties"
    ]
)

print(rented_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(6,5))

plt.bar(
    rented_df["Rental Status"],
    rented_df["Average Price"]
)

plt.title("Average Property Price: Rented vs Non-Rented")
plt.xlabel("Rental Status")
plt.ylabel("Average Property Price")

plt.tight_layout()
plt.show()
# %%





# %%
#Property & Pricing Analysis
#6. How do bedrooms and bathrooms affect pricing?


#Average Price by Bedrooms AND Bathrooms


#Average Price by Number of Bedrooms
query = """
SELECT
    pa.bedrooms,
    COUNT(*) AS total_properties,
    ROUND(AVG(l.price),2) AS average_price
FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id
GROUP BY pa.bedrooms
ORDER BY pa.bedrooms;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

import pandas as pd

bedroom_df = pd.DataFrame(
    rows,
    columns=[
        "Bedrooms",
        "Total Properties",
        "Average Price"
    ]
)

print(bedroom_df)


#Average Price by Number of Bathrooms
query = """
SELECT
    pa.bathrooms,
    COUNT(*) AS total_properties,
    ROUND(AVG(l.price),2) AS average_price
FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id
GROUP BY pa.bathrooms
ORDER BY pa.bathrooms;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

bathroom_df = pd.DataFrame(
    rows,
    columns=[
        "Bathrooms",
        "Total Properties",
        "Average Price"
    ]
)

print(bathroom_df)


# Visualization (Bathrooms vs Average Price)
plt.figure(figsize=(8,5))

plt.bar(
    bathroom_df["Bathrooms"],
    bathroom_df["Average Price"]
)

plt.title("Average Property Price by Number of Bathrooms")
plt.xlabel("Bathrooms")
plt.ylabel("Average Price")

plt.tight_layout()
plt.show()


#Visualization (Bedrooms vs Average Price)

import matplotlib.pyplot as plt

plt.figure

plt.bar(
    bedroom_df["Bedrooms"],
    bedroom_df["Average Price"]
)

plt.title("Average Property Price by Number of Bedrooms")
plt.xlabel("Bedrooms")
plt.ylabel("Average Price")

plt.tight_layout()
plt.show()
# %%
#Property & Pricing Analysis
#7. Do properties with parking and power backup sell at higher prices?


#Compare Average Price by Parking & Power Backup

query = """
SELECT
    CASE
        WHEN pa.parking_available = 1 AND pa.power_backup = 1 THEN 'Parking + Power Backup'
        WHEN pa.parking_available = 1 AND pa.power_backup = 0 THEN 'Parking Only'
        WHEN pa.parking_available = 0 AND pa.power_backup = 1 THEN 'Power Backup Only'
        ELSE 'Neither Available'
    END AS amenities,

    COUNT(*) AS total_properties,
    ROUND(AVG(l.price), 2) AS average_price

FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id

GROUP BY amenities

ORDER BY average_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

amenities_df = pd.DataFrame(
    rows,
    columns=[
        "Amenities",
        "Total Properties",
        "Average Price"
    ]
)

print(amenities_df)


#Visualisation

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

plt.bar(
    amenities_df["Amenities"],
    amenities_df["Average Price"]
)

plt.title("Impact of Parking & Power Backup on Property Prices")
plt.xlabel("Amenities")
plt.ylabel("Average Property Price")

plt.xticks(rotation=15)

plt.tight_layout()
plt.show()


#Analyze Parking and Power Backup Separately

query = """
SELECT
    pa.parking_available,
    pa.power_backup,
    COUNT(*) AS total_properties,
    ROUND(AVG(l.price), 2) AS average_price

FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id

GROUP BY pa.parking_available, pa.power_backup

ORDER BY average_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)
# %%
#Property & Pricing Analysis
#8. How does year built influence listing price?


#Average Listing Price by Year Built

query = """
SELECT
    pa.year_built,
    COUNT(*) AS total_properties,
    ROUND(AVG(l.price), 2) AS average_listing_price
FROM listings l
JOIN property_attributes pa
ON l.listing_id = pa.listing_id
GROUP BY pa.year_built
ORDER BY pa.year_built;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

year_price_df = pd.DataFrame(
    rows,
    columns=[
        "Year Built",
        "Total Properties",
        "Average Listing Price"
    ]
)

print(year_price_df)
# %%
#Property & Pricing Analysis
#9. Which cities have the highest average property prices?
query = """
SELECT
    city,
    COUNT(*) AS total_properties,
    ROUND(AVG(price), 2) AS average_property_price
FROM listings
GROUP BY city
ORDER BY average_property_price DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


import pandas as pd

city_price_df = pd.DataFrame(
    rows,
    columns=[
        "City",
        "Total Properties",
        "Average Property Price"
    ]
)

print(city_price_df)
# %%
#Property & Pricing Analysis
#10. How are properties distributed across price buckets?


#Coding

query = """
SELECT
    CASE
        WHEN price < 500000 THEN 'Below 500K'
        WHEN price BETWEEN 500000 AND 999999 THEN '500K - 999K'
        WHEN price BETWEEN 1000000 AND 1499999 THEN '1M - 1.49M'
        WHEN price BETWEEN 1500000 AND 1999999 THEN '1.5M - 1.99M'
        ELSE '2M and Above'
    END AS price_bucket,

    COUNT(*) AS total_properties,
    ROUND(AVG(price), 2) AS average_price

FROM listings

GROUP BY price_bucket

ORDER BY
CASE
    WHEN price_bucket = 'Below 500K' THEN 1
    WHEN price_bucket = '500K - 999K' THEN 2
    WHEN price_bucket = '1M - 1.49M' THEN 3
    WHEN price_bucket = '1.5M - 1.99M' THEN 4
    ELSE 5
END;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

price_bucket_df = pd.DataFrame(
    rows,
    columns=[
        "Price Bucket",
        "Total Properties",
        "Average Price"
    ]
)

print(price_bucket_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))

plt.bar(
    price_bucket_df["Price Bucket"],
    price_bucket_df["Total Properties"]
)

plt.title("Distribution of Properties Across Price Buckets")
plt.xlabel("Price Bucket")
plt.ylabel("Number of Properties")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()
# %%
#Sales & Market Performance
#11. What is the average days on market by city?
query = """
SELECT
    l.city,
    COUNT(*) AS total_properties_sold,
    ROUND(AVG(s.days_on_market), 2) AS avg_days_on_market,
    MIN(s.days_on_market) AS min_days_on_market,
    MAX(s.days_on_market) AS max_days_on_market
FROM listings l
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY l.city
ORDER BY avg_days_on_market DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

market_df = pd.DataFrame(
    rows,
    columns=[
        "City",
        "Properties Sold",
        "Average Days on Market",
        "Minimum Days on Market",
        "Maximum Days on Market"
    ]
)

print(market_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

plt.bar(
    market_df["City"],
    market_df["Average Days on Market"],
)

plt.title("Average Days on Market by City")
plt.xlabel("City")
plt.ylabel("Average Days on Market")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# %%
#property & Pricing analysis
#12. Which property types sell the fastest?
query = """
SELECT
    l.property_type,
    COUNT(*) AS total_properties_sold,
    ROUND(AVG(s.days_on_market), 2) AS avg_days_on_market,
    MIN(s.days_on_market) AS fastest_sale,
    MAX(s.days_on_market) AS slowest_sale
FROM listings l
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY l.property_type
ORDER BY avg_days_on_market ASC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display

import pandas as pd

property_sales_df = pd.DataFrame(
    rows,
    columns=[
        "Property Type",
        "Properties Sold",
        "Average Days on Market",
        "Fastest Sale (Days)",
        "Slowest Sale (Days)"
    ]
)

print(property_sales_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.bar(
    property_sales_df["Property Type"],
    property_sales_df["Average Days on Market"]
)

plt.title("Average Days on Market by Property Type")
plt.xlabel("Property Type")
plt.ylabel("Average Days on Market")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()
# %%
#Sales & Market Performance
#13 What percentage of properties are sold above listing price?


#coding

query = """
SELECT
    COUNT(*) AS total_properties_sold,

    SUM(CASE
            WHEN s.sale_price > l.price THEN 1
            ELSE 0
        END) AS sold_above_listing,

    SUM(CASE
            WHEN s.sale_price = l.price THEN 1
            ELSE 0
        END) AS sold_at_listing,

    SUM(CASE
            WHEN s.sale_price < l.price THEN 1
            ELSE 0
        END) AS sold_below_listing,

    ROUND(
        (SUM(CASE
                WHEN s.sale_price > l.price THEN 1
                ELSE 0
            END) * 100.0) / COUNT(*),
        2
    ) AS percentage_above_listing

FROM listings l
JOIN sales s
ON l.listing_id = s.listing_id;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display as a DataFrame

import pandas as pd

sales_summary_df = pd.DataFrame(
    rows,
    columns=[
        "Total Properties Sold",
        "Sold Above Listing",
        "Sold At Listing",
        "Sold Below Listing",
        "Percentage Above Listing (%)"
    ]
)

print(sales_summary_df)


#Visualize the Distribution

import matplotlib.pyplot as plt

labels = [
    "Above Listing",
    "At Listing",
    "Below Listing"
]

sizes = sales_summary_df.loc[
    0,
    ["Sold Above Listing", "Sold At Listing", "Sold Below Listing"]
].astype(float).tolist()

plt.figure(figsize=(6,6))

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Distribution of Sale Prices vs Listing Prices")

plt.show()
# %%
#Sales & Market Performance
#14. What is the sale-to-list price ratio by city?
#coding
query = """
SELECT
    l.city,
    COUNT(*) AS total_properties_sold,
    ROUND(AVG(l.price), 2) AS avg_listing_price,
    ROUND(AVG(s.sale_price), 2) AS avg_sale_price,
    ROUND(AVG((s.sale_price / l.price) * 100), 2) AS sale_to_list_ratio
FROM listings l
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY l.city
ORDER BY sale_to_list_ratio DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame
import pandas as pd

ratio_df = pd.DataFrame(
    rows,
    columns=[
        "City",
        "Properties Sold",
        "Average Listing Price",
        "Average Sale Price",
        "Sale-to-List Ratio (%)"
    ]
)

print(ratio_df)

#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

plt.bar(
    ratio_df["City"],
    ratio_df["Sale-to-List Ratio (%)"]
)

plt.title("Sale-to-List Price Ratio by City")
plt.xlabel("City")
plt.ylabel("Sale-to-List Price Ratio (%)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# %%
#Sales & Market Performance
#15. Which listings took more than 90 days to sell?


#coding

query = """
SELECT
    l.listing_id,
    l.city,
    l.property_type,
    ROUND(l.price, 2) AS listing_price,
    ROUND(s.sale_price, 2) AS sale_price,
    s.days_on_market,
    s.date_sold
FROM listings l
JOIN sales s
ON l.listing_id = s.listing_id
WHERE s.days_on_market > 90
ORDER BY s.days_on_market DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

slow_sales_df = pd.DataFrame(
    rows,
    columns=[
        "Listing ID",
        "City",
        "Property Type",
        "Listing Price",
        "Sale Price",
        "Days on Market",
        "Date Sold"
    ]
)

print(slow_sales_df)
# %%
#Sales & Market Performance
#16.How does metro distance affect time on market?


#coding

query = """
SELECT
    CASE
        WHEN pa.metro_distance_km <= 1 THEN '0-1 km'
        WHEN pa.metro_distance_km <= 3 THEN '1-3 km'
        WHEN pa.metro_distance_km <= 5 THEN '3-5 km'
        ELSE 'Above 5 km'
    END AS metro_distance,

    COUNT(*) AS total_properties,

    ROUND(AVG(s.days_on_market),2) AS avg_days_on_market,

    MIN(s.days_on_market) AS minimum_days,

    MAX(s.days_on_market) AS maximum_days

FROM property_attributes pa
JOIN sales s
ON pa.listing_id = s.listing_id

GROUP BY metro_distance

ORDER BY
CASE
    WHEN metro_distance = '0-1 km' THEN 1
    WHEN metro_distance = '1-3 km' THEN 2
    WHEN metro_distance = '3-5 km' THEN 3
    ELSE 4
END;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

metro_market_df = pd.DataFrame(
    rows,
    columns=[
        "Metro Distance",
        "Total Properties",
        "Average Days on Market",
        "Minimum Days",
        "Maximum Days"
    ]
)

print(metro_market_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(9,5))

plt.bar(
    metro_market_df["Metro Distance"],
    metro_market_df["Average Days on Market"]
)

plt.title("Average Time on Market by Distance to Metro")
plt.xlabel("Distance to Metro")
plt.ylabel("Average Days on Market")

plt.tight_layout()
plt.show()
# %%
#Sales & Market Performance
#17. What is the monthly sales trend?


#coding

query = """
SELECT
    DATE_FORMAT(date_sold, '%Y-%m') AS sales_month,
    COUNT(*) AS total_properties_sold
FROM sales
GROUP BY DATE_FORMAT(date_sold, '%Y-%m')
ORDER BY sales_month;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

monthly_sales_df = pd.DataFrame(
    rows,
    columns=[
        "Sales Month",
        "Properties Sold"
    ]
)

print(monthly_sales_df)


#Visualization- Line Chart
import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))

plt.plot(
    monthly_sales_df["Sales Month"],
    monthly_sales_df["Properties Sold"],
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Number of Properties Sold")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()
plt.show()
# %%
#Sales & Market Performance
#18. Which properties are currently unsold?


#coding

query = """
SELECT
    l.listing_id,
    l.city,
    l.property_type,
    l.price,
    l.sqft,
    l.listed_date,
    l.agent_id
FROM listings l
LEFT JOIN sales s
ON l.listing_id = s.listing_id
WHERE s.listing_id IS NULL
ORDER BY l.listed_date DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

unsold_df = pd.DataFrame(
    rows,
    columns=[
        "Listing ID",
        "City",
        "Property Type",
        "Listing Price",
        "Area (Sq. Ft.)",
        "Listed Date",
        "Agent ID"
    ]
)

print(unsold_df)


#Count the Number of Unsold Properties

query = """
SELECT COUNT(*) AS total_unsold_properties
FROM listings l
LEFT JOIN sales s
ON l.listing_id = s.listing_id
WHERE s.listing_id IS NULL;
"""

cursor.execute(query)

result = cursor.fetchone()

print("Total Unsold Properties:", result[0])


#Visualize Unsold Properties by City

query = """
SELECT
    l.city,
    COUNT(*) AS unsold_properties
FROM listings l
LEFT JOIN sales s
ON l.listing_id = s.listing_id
WHERE s.listing_id IS NULL
GROUP BY l.city
ORDER BY unsold_properties DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

city_unsold_df = pd.DataFrame(
    rows,
    columns=[
        "City",
        "Unsold Properties"
    ]
)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

plt.bar(
    city_unsold_df["City"],
    city_unsold_df["Unsold Properties"]
)

plt.title("Unsold Properties by City")
plt.xlabel("City")
plt.ylabel("Number of Unsold Properties")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# %%
#Agent Performance
#19. Which agents have closed the most sales?

#coding

query = """
SELECT
    a.agent_id,
    a.name,
    COUNT(s.listing_id) AS total_sales_closed,
    ROUND(SUM(s.sale_price), 2) AS total_sales_value,
    ROUND(AVG(s.sale_price), 2) AS average_sale_price
FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY a.agent_id, a.name
ORDER BY total_sales_closed DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

agent_sales_df = pd.DataFrame(
    rows,
    columns=[
        "Agent ID",
        "Agent Name",
        "Total Sales Closed",
        "Total Sales Value",
        "Average Sale Price"
    ]
)

print(agent_sales_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.bar(
    agent_sales_df["Agent Name"],
    agent_sales_df["Total Sales Closed"]
)

plt.title("Top Agents by Number of Sales Closed")
plt.xlabel("Agent")
plt.ylabel("Sales Closed")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()
# %%
#Agent Performance
#20. Who are the top agents by total sales revenue?

#coding

query = """
SELECT
    a.agent_id,
    a.name,
    COUNT(s.listing_id) AS total_properties_sold,
    ROUND(SUM(s.sale_price), 2) AS total_sales_revenue,
    ROUND(AVG(s.sale_price), 2) AS average_sale_price
FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY a.agent_id, a.name
ORDER BY total_sales_revenue DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

agent_revenue_df = pd.DataFrame(
    rows,
    columns=[
        "Agent ID",
        "Agent Name",
        "Properties Sold",
        "Total Sales Revenue",
        "Average Sale Price"
    ]
)

print(agent_revenue_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.bar(
    agent_revenue_df["Agent Name"],
    agent_revenue_df["Total Sales Revenue"]
)

plt.title("Top Agents by Total Sales Revenue")
plt.xlabel("Agent")
plt.ylabel("Total Sales Revenue")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()
# %%
#Agent Performance
#21. Which agents close deals fastest?

#coding

query = """
SELECT
    a.agent_id,
    a.name,
    COUNT(s.listing_id) AS total_sales_closed,
    ROUND(AVG(s.days_on_market), 2) AS avg_days_to_close,
    MIN(s.days_on_market) AS fastest_sale_days,
    MAX(s.days_on_market) AS slowest_sale_days
FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY a.agent_id, a.name
ORDER BY avg_days_to_close ASC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

agent_speed_df = pd.DataFrame(
    rows,
    columns=[
        "Agent ID",
        "Agent Name",
        "Sales Closed",
        "Average Days to Close",
        "Fastest Sale (Days)",
        "Slowest Sale (Days)"
    ]
)

print(agent_speed_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.bar(
    agent_speed_df["Agent Name"],
    agent_speed_df["Average Days to Close"]
)

plt.title("Average Days to Close Deals by Agent")
plt.xlabel("Agent")
plt.ylabel("Average Days to Close")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


#Top 10 Fastest Agents

query = """
SELECT
    a.agent_id,
    a.name,
    COUNT(s.listing_id) AS total_sales_closed,
    ROUND(AVG(s.days_on_market), 2) AS avg_days_to_close
FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY a.agent_id, a.name
ORDER BY avg_days_to_close ASC
LIMIT 10;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)
# %%
#Agent Performance
#22. Does experience correlate with deals closed?

#coding

query = """
SELECT
    agent_id,
    name,
    experience_years,
    deals_closed
FROM agents
ORDER BY experience_years ASC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

experience_df = pd.DataFrame(
    rows,
    columns=[
        "Agent ID",
        "Agent Name",
        "Experience (Years)",
        "Deals Closed"
    ]
)

print(experience_df)


#Calculate Correlation

correlation = experience_df["Experience (Years)"].corr(
    experience_df["Deals Closed"]
)

print("Correlation between Experience and Deals Closed:", round(correlation, 3))

#Interpretation
#Correlation ﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿ +1 ﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿ Strong positive relationship (more experience, more deals closed).
#Correlation ﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿ 0 ﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿ Little or no relationship.
#Correlation ﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿ -1 ﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿﷿ Negative relationship.


#Scatter Plot (Best Visualization)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))

plt.scatter(
    experience_df["Experience (Years)"],
    experience_df["Deals Closed"]
)

plt.title("Experience vs Deals Closed")
plt.xlabel("Experience (Years)")
plt.ylabel("Deals Closed")

plt.grid(True)

plt.tight_layout()
plt.show()


#Summary Analysis by Experience Group

query = """
SELECT
    CASE
        WHEN experience_years < 3 THEN '0-2 Years'
        WHEN experience_years BETWEEN 3 AND 5 THEN '3-5 Years'
        WHEN experience_years BETWEEN 6 AND 10 THEN '6-10 Years'
        ELSE '10+ Years'
    END AS experience_group,

    COUNT(*) AS total_agents,
    ROUND(AVG(deals_closed), 2) AS avg_deals_closed

FROM agents

GROUP BY experience_group

ORDER BY
CASE
    WHEN experience_group = '0-2 Years' THEN 1
    WHEN experience_group = '3-5 Years' THEN 2
    WHEN experience_group = '6-10 Years' THEN 3
    ELSE 4
END;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Summary

experience_group_df = pd.DataFrame(
    rows,
    columns=[
        "Experience Group",
        "Total Agents",
        "Average Deals Closed"
    ]
)

print(experience_group_df)


#Visualization- Bar Chart

plt.figure(figsize=(8,5))

plt.bar(
    experience_group_df["Experience Group"],
    experience_group_df["Average Deals Closed"]
)

plt.title("Average Deals Closed by Experience Group")
plt.xlabel("Experience Group")
plt.ylabel("Average Deals Closed")

plt.tight_layout()
plt.show()
# %%
#Agent Performance
#23. Do agents with higher ratings close deals faster?


#coding

query = """
SELECT
    a.agent_id,
    a.name,
    a.rating,
    COUNT(s.listing_id) AS total_sales,
    ROUND(AVG(s.days_on_market), 2) AS avg_days_to_close
FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY a.agent_id, a.name, a.rating
ORDER BY a.rating DESC, avg_days_to_close ASC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

rating_df = pd.DataFrame(
    rows,
    columns=[
        "Agent ID",
        "Agent Name",
        "Rating",
        "Total Sales",
        "Average Days to Close"
    ]
)

print(rating_df)


#Calculate Correlation

correlation = rating_df["Rating"].corr(
    rating_df["Average Days to Close"]
)

print("Correlation:", round(correlation, 3))

#Interpretation
#Negative correlation (< 0): Higher-rated agents generally close deals faster.
#Positive correlation (> 0): Higher-rated agents tend to take longer to close deals.
#Near 0: Little or no relationship between ratings and closing speed.


#Scatter Plot

import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))

plt.scatter(
    rating_df["Rating"],
    rating_df["Average Days to Close"]
)

plt.title("Agent Rating vs Average Days to Close")
plt.xlabel("Agent Rating")
plt.ylabel("Average Days to Close")

plt.grid(True)

plt.tight_layout()
plt.show()


#Group Ratings into Categories

query = """
SELECT
    CASE
        WHEN rating >= 4.5 THEN 'Excellent (4.5-5.0)'
        WHEN rating >= 4.0 THEN 'Good (4.0-4.49)'
        WHEN rating >= 3.5 THEN 'Average (3.5-3.99)'
        ELSE 'Below Average (<3.5)'
    END AS rating_category,

    COUNT(*) AS total_agents,
    ROUND(AVG(s.days_on_market), 2) AS avg_days_to_close

FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id

GROUP BY rating_category

ORDER BY
CASE
    WHEN rating_category = 'Excellent (4.5-5.0)' THEN 1
    WHEN rating_category = 'Good (4.0-4.49)' THEN 2
    WHEN rating_category = 'Average (3.5-3.99)' THEN 3
    ELSE 4
END;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Grouped Results

rating_group_df = pd.DataFrame(
    rows,
    columns=[
        "Rating Category",
        "Total Agents",
        "Average Days to Close"
    ]
)

print(rating_group_df)


#Visualization

plt.figure(figsize=(8,5))

plt.bar(
    rating_group_df["Rating Category"],
    rating_group_df["Average Days to Close"]
)

plt.title("Average Days to Close by Agent Rating")
plt.xlabel("Agent Rating Category")
plt.ylabel("Average Days to Close")

plt.tight_layout()
plt.show()
# %%
#Agent Performance
#24. What is the average commission earned by each agent?

#coding

query = """
SELECT
    a.agent_id,
    a.name,
    a.commission_rate,
    COUNT(s.listing_id) AS total_sales_closed,
    ROUND(AVG(s.sale_price), 2) AS average_sale_price,
    ROUND(AVG(s.sale_price * (a.commission_rate / 100)), 2) AS average_commission_earned
FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY
    a.agent_id,
    a.name,
    a.commission_rate
ORDER BY average_commission_earned DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

commission_df = pd.DataFrame(
    rows,
    columns=[
        "Agent ID",
        "Agent Name",
        "Commission Rate (%)",
        "Total Sales Closed",
        "Average Sale Price",
        "Average Commission Earned"
    ]
)

print(commission_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.bar(
    commission_df["Agent Name"],
    commission_df["Average Commission Earned"]
)

plt.title("Average Commission Earned by Agent")
plt.xlabel("Agent")
plt.ylabel("Average Commission Earned")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


#Total Commission Earned by Each Agent- total commission instead of the average, use:(additional part)

query = """
SELECT
    a.agent_id,
    a.name,
    COUNT(s.listing_id) AS total_sales_closed,
    ROUND(SUM(s.sale_price * (a.commission_rate / 100)), 2) AS total_commission_earned
FROM agents a
JOIN listings l
ON a.agent_id = l.agent_id
JOIN sales s
ON l.listing_id = s.listing_id
GROUP BY
    a.agent_id,
    a.name
ORDER BY total_commission_earned DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)
# %%
#Agent Performance
#25. Which agents currently have the most active listings?


# coding

query = """
SELECT
    a.agent_id,
    a.name,
    COUNT(l.listing_id) AS active_listings
FROM agents a
JOIN listings l
    ON a.agent_id = l.agent_id
LEFT JOIN sales s
    ON l.listing_id = s.listing_id
WHERE s.listing_id IS NULL
GROUP BY
    a.agent_id,
    a.name
ORDER BY active_listings DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

active_listing_df = pd.DataFrame(
    rows,
    columns=[
        "Agent ID",
        "Agent Name",
        "Active Listings"
    ]
)

print(active_listing_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.bar(
    active_listing_df["Agent Name"],
    active_listing_df["Active Listings"]
)

plt.title("Active Listings by Agent")
plt.xlabel("Agent")
plt.ylabel("Number of Active Listings")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


#Top 10 Agents with the Most Active Listings

query = """
SELECT
    a.agent_id,
    a.name,
    COUNT(l.listing_id) AS active_listings
FROM agents a
JOIN listings l
    ON a.agent_id = l.agent_id
LEFT JOIN sales s
    ON l.listing_id = s.listing_id
WHERE s.listing_id IS NULL
GROUP BY
    a.agent_id,
    a.name
ORDER BY active_listings DESC
LIMIT 10;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)
# %%
# Buyer & Financing Behavior
# 26. What percentage of buyers are investors vs end users?

#Coding

query = """
SELECT
    buyer_type,
    COUNT(*) AS total_buyers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM buyers), 2) AS percentage
FROM buyers
GROUP BY buyer_type
ORDER BY percentage DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results in a Pandas DataFrame

import pandas as pd

buyer_type_df = pd.DataFrame(
    rows,
    columns=[
        "Buyer Type",
        "Total Buyers",
        "Percentage (%)"
    ]
)

print(buyer_type_df)


#Visualization (Pie Chart)

import matplotlib.pyplot as plt

plt.figure(figsize=(7,7))

plt.pie(
    buyer_type_df["Total Buyers"],
    labels=buyer_type_df["Buyer Type"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Investor vs End User Distribution")

plt.show()


#Visualization (Bar Chart)

plt.figure(figsize=(7,5))

plt.bar(
    buyer_type_df["Buyer Type"],
    buyer_type_df["Percentage (%)"]
)

plt.title("Percentage of Buyers by Buyer Type")
plt.xlabel("Buyer Type")
plt.ylabel("Percentage (%)")

plt.tight_layout()
plt.show()
# %%
# Buyer & Financing Behavior
# 27. Which cities have the highest loan uptake rate?


#coding

query = """
SELECT
    l.city,
    COUNT(b.buyer_id) AS total_buyers,
    SUM(CASE
            WHEN b.loan_taken = TRUE THEN 1
            ELSE 0
        END) AS buyers_with_loan,
    ROUND(
        SUM(CASE
                WHEN b.loan_taken = TRUE THEN 1
                ELSE 0
            END) * 100.0 / COUNT(b.buyer_id),
        2
    ) AS loan_uptake_rate
FROM buyers b
JOIN sales s
    ON b.sale_id = b.sale_id
JOIN listings l
    ON s.listing_id = l.listing_id
GROUP BY l.city
ORDER BY loan_uptake_rate DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results Using Pandas

import pandas as pd

loan_city_df = pd.DataFrame(
    rows,
    columns=[
        "City",
        "Total Buyers",
        "Buyers with Loan",
        "Loan Uptake Rate (%)"
    ]
)

print(loan_city_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

plt.bar(
    loan_city_df["City"],
    loan_city_df["Loan Uptake Rate (%)"]
)

plt.title("Loan Uptake Rate by City")
plt.xlabel("City")
plt.ylabel("Loan Uptake Rate (%)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# %%
# Buyer & Financing Behavior
# 28. What is the average loan amount by buyer type?



#coding

query = """
SELECT
    buyer_type,
    COUNT(*) AS total_buyers,
    COUNT(loan_amount) AS buyers_with_loan,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount
FROM buyers
WHERE loan_amount IS NOT NULL
GROUP BY buyer_type
ORDER BY average_loan_amount DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results as a DataFrame

import pandas as pd

loan_df = pd.DataFrame(
    rows,
    columns=[
        "Buyer Type",
        "Total Buyers",
        "Buyers with Loan",
        "Average Loan Amount"
    ]
)

print(loan_df)


#Visualization (Bar Chart)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.bar(
    loan_df["Buyer Type"],
    loan_df["Average Loan Amount"]
)

plt.title("Average Loan Amount by Buyer Type")
plt.xlabel("Buyer Type")
plt.ylabel("Average Loan Amount")

plt.tight_layout()
plt.show()


#Include Buyer Types Without Loans - all buyer types (even those with no loans), use:

query = """
SELECT
    buyer_type,
    COUNT(*) AS total_buyers,
    SUM(CASE
            WHEN loan_taken = TRUE THEN 1
            ELSE 0
        END) AS buyers_with_loan,
    ROUND(AVG(
        CASE
            WHEN loan_taken = TRUE THEN loan_amount
            ELSE NULL
        END
    ), 2) AS average_loan_amount
FROM buyers
GROUP BY buyer_type
ORDER BY average_loan_amount DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)
# %%
#Buyer & Financing Behavior
# 29. Which payment mode is most commonly used?


#Coding

query = """
SELECT
    payment_mode,
    COUNT(*) AS total_transactions,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM buyers),
        2
    ) AS percentage
FROM buyers
GROUP BY payment_mode
ORDER BY total_transactions DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results as a DataFrame

import pandas as pd

payment_df = pd.DataFrame(
    rows,
    columns=[
        "Payment Mode",
        "Total Transactions",
        "Percentage (%)"
    ]
)

print(payment_df)


#Visualization (Bar Chart)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.bar(
    payment_df["Payment Mode"],
    payment_df["Total Transactions"]
)

plt.title("Most Commonly Used Payment Mode")
plt.xlabel("Payment Mode")
plt.ylabel("Number of Transactions")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# Visualization (Pie Chart)

import matplotlib.pyplot as plt

plt.figure(figsize=(7,7))

plt.pie(
    payment_df["Total Transactions"],
    labels=payment_df["Payment Mode"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Distribution of Payment Modes")

plt.show()


#Find Only the Most Common Payment Mode- the single most frequently used payment mode:

query = """
SELECT
    payment_mode,
    COUNT(*) AS total_transactions
FROM buyers
GROUP BY payment_mode
ORDER BY total_transactions DESC
LIMIT 1;
"""

cursor.execute(query)

result = cursor.fetchone()

print("Most Common Payment Mode:", result[0])
print("Number of Transactions:", result[1])
# %%
#Buyer & Financing Behavior
#30. Do loan-backed purchases take longer to close?

query = """
SELECT
    CASE
        WHEN b.loan_taken = TRUE THEN 'Loan Taken'
        ELSE 'No Loan'
    END AS loan_status,

    COUNT(*) AS total_purchases,

    ROUND(AVG(s.days_on_market), 2) AS avg_days_to_close

FROM buyers b
JOIN sales s
ON b.sale_id = b.sale_id

GROUP BY loan_status
ORDER BY avg_days_to_close DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


#Display Results as a DataFrame

import pandas as pd

loan_close_df = pd.DataFrame(
    rows,
    columns=[
        "Loan Status",
        "Total Purchases",
        "Average Days to Close"
    ]
)

print(loan_close_df)


#Visualization

import matplotlib.pyplot as plt

plt.figure(figsize=(7,5))

plt.bar(
    loan_close_df["Loan Status"],
    loan_close_df["Average Days to Close"]
)

plt.title("Average Time to Close: Loan vs Non-Loan Purchases")
plt.xlabel("Loan Status")
plt.ylabel("Average Days on Market")

plt.tight_layout()
plt.show()



import pandas as pd

def property_type_price():

    query = """
    SELECT property_type,
           ROUND(AVG(price/sqft),2)
    FROM listings
    GROUP BY property_type;
    """

    return pd.read_sql(query)


