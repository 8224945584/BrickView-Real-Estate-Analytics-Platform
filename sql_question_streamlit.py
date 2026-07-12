import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm

# SQL query

st.sidebar.title("BrickView SQL Query Dashboard")

dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Property & Pricing",
        "Sales & Market Performance",
        "Agent Performance",
        "Buyer & Financing"
    ]
)

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="700234OMk#",
    database="real_estate"
)
cursor = conn.cursor()

# Property & Pricing

if dashboard == "Property & Pricing":
    st.title("📊 Property & Pricing Analysis")

    question = st.selectbox(
        "Select Analysis",
        [
            "1. What is the average listing price by city?",
            "2. What is the average price per square foot by property type?",
            "3. How does furnishing status impact property prices?",
            "4. Do properties closer to metro stations command higher prices?",
            "5. Are rented properties priced differently from non-rented properties?",
            "6. How do bedrooms and bathrooms affect pricing?",
            "7. Do properties with parking and power backup sell at higher prices?",
            "8. How does year built influence listing price?",
            "9. Which cities have the highest average property prices?",
            "10. How are properties distributed across price buckets?"
        ]
    )

# 1. What is the average listing price by city?    
    if question == "1. What is the average listing price by city?":
        query = """
        SELECT 
            city,
            ROUND(AVG(price),2) AS average_listing_price
        FROM listings
        GROUP BY city
        ORDER BY average_listing_price DESC;
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        import pandas as pd

        avg_price_df = pd.DataFrame(
            rows,
            columns=[
                "City",
                "Average Listing Price"
            ]
        )

        st.subheader("Average Listing Price by City")

        st.dataframe(avg_price_df)
     
    # Visualization

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            avg_price_df["City"],
            avg_price_df["Average Listing Price"]
        )

        ax.set_title("Average Listing Price by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Average Listing Price")

        plt.xticks(rotation=45)

        st.pyplot(fig)


    elif question == "2. What is the average price per square foot by property type?":
        
        query = """
        SELECT
            property_type,
            ROUND(AVG(price/sqft),2) AS avg_price_per_sqft
        FROM listings
        GROUP BY property_type;
        """

        df = pd.read_sql(query, conn)

        st.subheader("Average Price per Square Foot")

        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(
            df["property_type"], 
            df["avg_price_per_sqft"]
        )
        ax.set_title("Average Price per Square Foot by Property Type")
        ax.set_xlabel("Property Type")
        ax.set_ylabel("Average Price per Sq Ft")
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)



##------------------
# 3. How does furnishing status impact property prices?
# Furnishing Status Impact

    elif question == "3. How does furnishing status impact property prices?":

        query = """
        SELECT 
            p.furnishing_status,
            ROUND(AVG(price),2) AS avg_price
        FROM listings l
        JOIN property_attributes p
            ON l.listing_id=p.listing_id
        GROUP BY furnishing_status;
        """

        df = pd.read_sql(query, conn)

        st.subheader("Impact of Furnishing Status on Property Prices")
        st.dataframe(df)
        
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(
            df["furnishing_status"],
            df["avg_price"]
        )

        ax.set_title("Average Property Price by Furnishing Status")
        ax.set_xlabel("Furnishing Status")
        ax.set_ylabel("Average Price")

        plt.xticks(rotation=20)
        plt.tight_layout()

        st.pyplot(fig)


##---------------------------
# 4. Do properties closer to metro stations command higher prices?
# Metro Distance vs Price

    elif question == "4. Do properties closer to metro stations command higher prices?":

        query = """
        SELECT
            CASE
                WHEN metro_distance_km<=1 THEN '0-1 km'
                WHEN metro_distance_km<=3 THEN '1-3 km'
                WHEN metro_distance_km<=5 THEN '3-5 km'
                ELSE '>5 km'
            END AS metro_range,
            ROUND(AVG(price),2) avg_price
        FROM listings l
        JOIN property_attributes p
            ON l.listing_id=p.listing_id
        GROUP BY metro_range;
        """

        df = pd.read_sql(query, conn)

        st.dataframe(df)

        st.bar_chart(df.set_index("metro_range"))

    elif question == "5. Are rented properties priced differently from non-rented properties?":

        query = """
        SELECT
            p.is_rented,
            ROUND(AVG(l.price), 2) AS avg_price
        FROM listings l
        JOIN property_attributes p
            ON l.listing_id = p.listing_id
        GROUP BY p.is_rented;
        """

        df = pd.read_sql(query, conn)

        st.subheader("Average Property Price: Rented vs Non-Rented")

        st.dataframe(df)

        st.bar_chart(
            df.set_index("is_rented")
        )



    elif question == "5. Are rented properties priced differently from non-rented ones?":

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

        rented_df = pd.read_sql(query, conn)

        st.subheader("Average Property Price: Rented vs Non-Rented")

        st.dataframe(rented_df)

        fig, ax = plt.subplots(figsize=(6, 5))

        ax.bar(
            rented_df["rental_status"],
            rented_df["average_price"]
        )

        ax.set_title("Average Property Price: Rented vs Non-Rented")
        ax.set_xlabel("Rental Status")
        ax.set_ylabel("Average Property Price")

        plt.tight_layout()

        st.pyplot(fig)
 



    elif question == "6. How do bedrooms and bathrooms affect pricing?":

        st.subheader("Impact of Bedrooms and Bathrooms on Property Prices")

        # Average Price by Bedrooms
        bedroom_query = """
        SELECT
            pa.bedrooms,
            COUNT(*) AS total_properties,
            ROUND(AVG(l.price), 2) AS average_price
        FROM listings l
        JOIN property_attributes pa
            ON l.listing_id = pa.listing_id
        GROUP BY pa.bedrooms
        ORDER BY pa.bedrooms;
        """

        bedroom_df = pd.read_sql(bedroom_query, conn)

        st.markdown("Average Price by Number of Bedrooms")

        st.dataframe(bedroom_df)

        fig1, ax1 = plt.subplots(figsize=(8, 5))

        ax1.bar(
            bedroom_df["bedrooms"],
            bedroom_df["average_price"]
        )

        ax1.set_title("Average Property Price by Bedrooms")
        ax1.set_xlabel("Bedrooms")
        ax1.set_ylabel("Average Price")

        plt.tight_layout()

        st.pyplot(fig1)

        # Average Price by Bathrooms
        bathroom_query = """
        SELECT
            pa.bathrooms,
            COUNT(*) AS total_properties,
            ROUND(AVG(l.price), 2) AS average_price
        FROM listings l
        JOIN property_attributes pa
            ON l.listing_id = pa.listing_id
        GROUP BY pa.bathrooms
        ORDER BY pa.bathrooms;
        """

        bathroom_df = pd.read_sql(bathroom_query, conn)

        st.markdown("Average Price by Number of Bathrooms")

        st.dataframe(bathroom_df)

        fig2, ax2 = plt.subplots(figsize=(8, 5))

        ax2.bar(
            bathroom_df["bathrooms"],
            bathroom_df["average_price"]
        )

        ax2.set_title("Average Property Price by Bathrooms")
        ax2.set_xlabel("Bathrooms")
        ax2.set_ylabel("Average Price")

        plt.tight_layout()

        st.pyplot(fig2)

    elif question == "7. Do properties with parking and power backup sell at higher prices?":

        st.subheader("Impact of Parking & Power Backup on Property Prices")

        # Analysis 1: Combined Amenities
        query = """
        SELECT
            CASE
                WHEN pa.parking_available = 1 AND pa.power_backup = 1
                    THEN 'Parking + Power Backup'
                WHEN pa.parking_available = 1 AND pa.power_backup = 0
                    THEN 'Parking Only'
                WHEN pa.parking_available = 0 AND pa.power_backup = 1
                    THEN 'Power Backup Only'
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

        amenities_df = pd.read_sql(query, conn)

        st.markdown("### Combined Amenities")

        st.dataframe(amenities_df)

        fig1, ax1 = plt.subplots(figsize=(10, 5))

        ax1.bar(
            amenities_df["amenities"],
            amenities_df["average_price"]
        )

        ax1.set_title("Impact of Parking & Power Backup on Property Prices")
        ax1.set_xlabel("Amenities")
        ax1.set_ylabel("Average Property Price")

        plt.xticks(rotation=20)
        plt.tight_layout()

        st.pyplot(fig1)

        # Analysis 2: Parking & Power Backup Separately
        query = """
        SELECT
            pa.parking_available,
            pa.power_backup,
            COUNT(*) AS total_properties,
            ROUND(AVG(l.price), 2) AS average_price

        FROM listings l
        JOIN property_attributes pa
            ON l.listing_id = pa.listing_id

        GROUP BY
            pa.parking_available,
            pa.power_backup

        ORDER BY average_price DESC;
        """

        parking_df = pd.read_sql(query, conn)

        st.markdown("### Parking and Power Backup Analysis")

        st.dataframe(parking_df)

        parking_df["Combination"] = (
            "Parking: "
            + parking_df["parking_available"].astype(str)
            + " | Backup: "
            + parking_df["power_backup"].astype(str)
        )

        fig2, ax2 = plt.subplots(figsize=(10, 5))

        ax2.bar(
            parking_df["Combination"],
            parking_df["average_price"]
        )

        ax2.set_title("Average Price by Parking & Power Backup")
        ax2.set_xlabel("Parking / Power Backup")
        ax2.set_ylabel("Average Property Price")

        plt.xticks(rotation=20)
        plt.tight_layout()

        st.pyplot(fig2)

    
    
    
    elif question == "8. How does year built influence listing price?":

        st.subheader("How Year Built Influences Listing Price")

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

        year_price_df = pd.read_sql(query, conn)

        st.dataframe(year_price_df)

        fig = px.line(
            year_price_df,
            x="year_built",
            y="average_listing_price",
            markers=True,
            title="Average Listing Price by Year Built"
        )

        fig.update_layout(
            xaxis_title="Year Built",
            yaxis_title="Average Listing Price"
        )

        st.plotly_chart(fig, use_container_width=True)

    


    elif question == "9. Which cities have the highest average property prices?":

        st.subheader("Cities with the Highest Average Property Prices")

        query = """
        SELECT
            city,
            COUNT(*) AS total_properties,
            ROUND(AVG(price), 2) AS average_property_price
        FROM listings
        GROUP BY city
        ORDER BY average_property_price DESC;
        """

        city_price_df = pd.read_sql(query, conn)

        st.dataframe(city_price_df)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            city_price_df["city"],
            city_price_df["average_property_price"]
        )

        ax.set_title("Average Property Price by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Average Property Price")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
    


    elif question == "10. How are properties distributed across price buckets?":

        st.subheader("Distribution of Properties Across Price Buckets")

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

        price_bucket_df = pd.read_sql(query, conn)

        st.dataframe(price_bucket_df)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            price_bucket_df["price_bucket"],
            price_bucket_df["total_properties"]
        )

        ax.set_title("Distribution of Properties Across Price Buckets")
        ax.set_xlabel("Price Bucket")
        ax.set_ylabel("Number of Properties")

        plt.xticks(rotation=20)
        plt.tight_layout()

        st.pyplot(fig)

    

    # Sales & Market Performance

elif dashboard == "Sales & Market Performance":
    st.title("📊 Sales & Market Performance")

    question = st.selectbox(
        "Select Analysis",
        [
            "11. What is the average days on market by city?",
            "12. Which property types sell the fastest?",
            "13. What percentage of properties are sold above listing price?",
            "14. What is the sale-to-list price ratio by city?",
            "15. Which listings took more than 90 days to sell?",
            "16. How does metro distance affect time on market?",
            "17. What is the monthly sales trend?",
            "18. Which properties are currently unsold?"
        ]
    )
    if question == "11. What is the average days on market by city?":

        st.subheader("Average Days on Market by City")

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

        market_df = pd.read_sql(query, conn)

        st.dataframe(market_df)

        fig = px.bar(
            market_df,
            x="city",
            y="avg_days_on_market",
            color="avg_days_on_market",
            text_auto=".2f",
            title="Average Days on Market by City"
        )

        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Average Days on Market",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    elif question == "12. Which property types sell the fastest?":

        st.subheader("Which Property Types Sell the Fastest?")

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

        property_sales_df = pd.read_sql(query, conn)

        st.dataframe(property_sales_df)

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(
            property_sales_df["property_type"],
            property_sales_df["avg_days_on_market"]
        )

        ax.set_title("Average Days on Market by Property Type")
        ax.set_xlabel("Property Type")
        ax.set_ylabel("Average Days on Market")

        plt.xticks(rotation=20)
        plt.tight_layout()

        st.pyplot(fig) 

    elif question == "13. What percentage of properties are sold above listing price?":

        st.subheader("Percentage of Properties Sold Above Listing Price")

        query = """
        SELECT
            COUNT(*) AS total_properties_sold,

            SUM(
                CASE
                    WHEN s.sale_price > l.price THEN 1
                    ELSE 0
                END
            ) AS sold_above_listing,

            SUM(
                CASE
                    WHEN s.sale_price = l.price THEN 1
                    ELSE 0
                END
            ) AS sold_at_listing,

            SUM(
                CASE
                    WHEN s.sale_price < l.price THEN 1
                    ELSE 0
                END
            ) AS sold_below_listing,

            ROUND(
                (
                    SUM(
                        CASE
                            WHEN s.sale_price > l.price THEN 1
                            ELSE 0
                        END
                    ) * 100.0
                ) / COUNT(*),
                2
            ) AS percentage_above_listing

        FROM listings l
        JOIN sales s
            ON l.listing_id = s.listing_id;
        """

        sales_summary_df = pd.read_sql(query, conn)

        st.dataframe(sales_summary_df)

        st.metric(
            "Percentage Sold Above Listing Price",
            f"{sales_summary_df.loc[0, 'percentage_above_listing']}%"
        )

        labels = [
            "Above Listing",
            "At Listing",
            "Below Listing"
        ]

        sizes = [
            sales_summary_df.loc[0, "sold_above_listing"],
            sales_summary_df.loc[0, "sold_at_listing"],
            sales_summary_df.loc[0, "sold_below_listing"]
        ]

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Distribution of Sale Prices vs Listing Prices")

        st.pyplot(fig)

    elif question == "14. What is the sale-to-list price ratio by city?":

        st.subheader("Sale-to-List Price Ratio by City")

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

        ratio_df = pd.read_sql(query, conn)

        st.dataframe(ratio_df)

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(
            ratio_df["city"],
            ratio_df["sale_to_list_ratio"]
        )

        ax.set_title("Sale-to-List Price Ratio by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Sale-to-List Price Ratio (%)")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig) 
    

    elif question == "15. Which listings took more than 90 days to sell?":

        st.subheader("Listings That Took More Than 90 Days to Sell")

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

        slow_sales_df = pd.read_sql(query, conn)

        st.dataframe(slow_sales_df)

        fig = px.bar(
            slow_sales_df,
            x="listing_id",
            y="days_on_market",
            color="city",
            hover_data=[
                "property_type",
                "listing_price",
                "sale_price",
                "date_sold"
            ],
            title="Listings Taking More Than 90 Days to Sell"
        )

        fig.update_layout(
            xaxis_title="Listing ID",
            yaxis_title="Days on Market"
        )

        st.plotly_chart(fig, use_container_width=True)
    
    elif question == "16. How does metro distance affect time on market?":

        st.subheader("Impact of Metro Distance on Time on Market")

        query = """
        SELECT
            CASE
                WHEN pa.metro_distance_km <= 1 THEN '0-1 km'
                WHEN pa.metro_distance_km <= 3 THEN '1-3 km'
                WHEN pa.metro_distance_km <= 5 THEN '3-5 km'
                ELSE 'Above 5 km'
            END AS metro_distance,

            COUNT(*) AS total_properties,

            ROUND(AVG(s.days_on_market), 2) AS avg_days_on_market,

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

        metro_market_df = pd.read_sql(query, conn)

        st.dataframe(metro_market_df)

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.bar(
            metro_market_df["metro_distance"],
            metro_market_df["avg_days_on_market"]
        )

        ax.set_title("Average Time on Market by Distance to Metro")
        ax.set_xlabel("Distance to Metro")
        ax.set_ylabel("Average Days on Market")

        plt.tight_layout()

        st.pyplot(fig)
     
    elif question == "17. What is the monthly sales trend?":

        st.subheader("Monthly Sales Trend")

        query = """
        SELECT
            DATE_FORMAT(date_sold, '%Y-%m') AS sales_month,
            COUNT(*) AS total_properties_sold
        FROM sales
        GROUP BY DATE_FORMAT(date_sold, '%Y-%m')
        ORDER BY sales_month;
        """

        monthly_sales_df = pd.read_sql(query, conn)

        st.dataframe(monthly_sales_df)

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(
            monthly_sales_df["sales_month"],
            monthly_sales_df["total_properties_sold"],
            marker="o",
            linewidth=2
        )

        ax.set_title("Monthly Sales Trend")
        ax.set_xlabel("Sales Month")
        ax.set_ylabel("Number of Properties Sold")

        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        st.pyplot(fig) 
    
    elif question == "18. Which properties are currently unsold?":

        st.subheader("Currently Unsold Properties")

        # -----------------------------
        # Unsold Properties
        # -----------------------------
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

        unsold_df = pd.read_sql(query, conn)

        st.dataframe(unsold_df)

        # -----------------------------
        # Total Unsold Properties
        # -----------------------------
        count_query = """
        SELECT
            COUNT(*) AS total_unsold_properties
        FROM listings l
        LEFT JOIN sales s
            ON l.listing_id = s.listing_id
        WHERE s.listing_id IS NULL;
        """

        total_unsold = pd.read_sql(count_query, conn)

        st.metric(
            label="Total Unsold Properties",
            value=int(total_unsold.loc[0, "total_unsold_properties"])
        )

        # -----------------------------
        # Unsold Properties by City
        # -----------------------------
        city_query = """
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

        city_unsold_df = pd.read_sql(city_query, conn)

        st.dataframe(city_unsold_df)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            city_unsold_df["city"],
            city_unsold_df["unsold_properties"]
        )

        ax.set_title("Unsold Properties by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Number of Unsold Properties")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
    

elif dashboard == "Agent Performance":
    st.title("📊 Agent Performance")

    question = st.selectbox(
        "Select Analysis",
        [
            "19. Which agents have closed the most sales?",
            "20. Who are the top agents by total sales revenue?",
            "21. Which agents close deals fastest?",
            "22. Does experience correlate with deals closed?",
            "23. Do agents with higher ratings close deals faster?",
            "24. What is the average commission earned by each agent?",
            "25. Which agents currently have the most active listings?"
        ]
    )
    
    if question == "19. Which agents have closed the most sales?":

        st.subheader("Agents with the Most Sales Closed")

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
        GROUP BY
            a.agent_id,
            a.name
        ORDER BY total_sales_closed DESC;
        """

        agent_sales_df = pd.read_sql(query, conn)

        st.dataframe(agent_sales_df)

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(
            agent_sales_df["name"],
            agent_sales_df["total_sales_closed"]
        )

        ax.set_title("Top Agents by Number of Sales Closed")
        ax.set_xlabel("Agent")
        ax.set_ylabel("Sales Closed")

        plt.xticks(rotation=90)
        plt.tight_layout()

        st.pyplot(fig)
    
    elif question == "20. Who are the top agents by total sales revenue?":

        st.subheader("Top Agents by Total Sales Revenue")

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
        GROUP BY
            a.agent_id,
            a.name
        ORDER BY total_sales_revenue DESC;
        """

        agent_revenue_df = pd.read_sql(query, conn)

        st.dataframe(agent_revenue_df)

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(
            agent_revenue_df["name"],
            agent_revenue_df["total_sales_revenue"]
        )

        ax.set_title("Top Agents by Total Sales Revenue")
        ax.set_xlabel("Agent")
        ax.set_ylabel("Total Sales Revenue")

        plt.xticks(rotation=90)
        plt.tight_layout()

        st.pyplot(fig)

    elif question == "21. Which agents close deals fastest?":

        st.subheader("Agents Who Close Deals the Fastest")

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
        GROUP BY
            a.agent_id,
            a.name
        ORDER BY avg_days_to_close ASC;
        """

        agent_speed_df = pd.read_sql(query, conn)

        st.dataframe(agent_speed_df)

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(
            agent_speed_df["name"],
            agent_speed_df["avg_days_to_close"]
        )

        ax.set_title("Average Days to Close Deals by Agent")
        ax.set_xlabel("Agent")
        ax.set_ylabel("Average Days to Close")

        plt.xticks(rotation=90)
        plt.tight_layout()

        st.pyplot(fig)

        st.subheader("Top 10 Fastest Agents")

        top10_query = """
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
        GROUP BY
            a.agent_id,
            a.name
        ORDER BY avg_days_to_close ASC
        LIMIT 10;
        """

        top10_df = pd.read_sql(top10_query, conn)

        st.dataframe(top10_df)
    
    elif question == "22. Does experience correlate with deals closed?":

        st.subheader("Experience vs Deals Closed")

        # -----------------------------
        # Agent Experience Data
        # -----------------------------
        query = """
        SELECT
            agent_id,
            name,
            experience_years,
            deals_closed
        FROM agents
        ORDER BY experience_years ASC;
        """

        experience_df = pd.read_sql(query, conn)

        st.dataframe(experience_df)

        # -----------------------------
        # Correlation
        # -----------------------------
        correlation = experience_df["experience_years"].corr(
            experience_df["deals_closed"]
        )

        st.metric(
            "Correlation Coefficient",
            round(correlation, 3)
        )

        if correlation >= 0.7:
            st.success(
                "Strong positive relationship: More experienced agents generally close more deals."
            )

        elif correlation >= 0.3:
            st.info(
                "Moderate positive relationship between experience and deals closed."
            )

        elif correlation > -0.3:
            st.warning(
                "Little or no relationship between experience and deals closed."
            )

        else:
            st.error(
                "Negative relationship detected."
            )

        # -----------------------------
        # Scatter Plot
        # -----------------------------
        fig = px.scatter(
            experience_df,
            x="experience_years",
            y="deals_closed",
            hover_name="name",
            trendline="ols",
            title="Experience vs Deals Closed"
        )

        fig.update_layout(
            xaxis_title="Experience (Years)",
            yaxis_title="Deals Closed"
        )

        st.plotly_chart(fig, use_container_width=True)

    elif question == "23. Do agents with higher ratings close deals faster?":

        st.subheader("Do Higher-Rated Agents Close Deals Faster?")

        # ---------------------------------------
        # Agent Rating vs Closing Speed
        # ---------------------------------------
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
        GROUP BY
            a.agent_id,
            a.name,
            a.rating
        ORDER BY
            a.rating DESC,
            avg_days_to_close ASC;
        """

        rating_df = pd.read_sql(query, conn)

        st.dataframe(rating_df)

        # ---------------------------------------
        # Correlation
        # ---------------------------------------
        correlation = rating_df["rating"].corr(
            rating_df["avg_days_to_close"]
        )

        st.metric(
            "Correlation Coefficient",
            round(correlation, 3)
        )

        if correlation < -0.5:
            st.success(
                "Higher-rated agents generally close deals faster."
            )

        elif correlation < 0:
            st.info(
                "There is a slight tendency for higher-rated agents to close deals faster."
            )

        elif correlation > 0.5:
            st.warning(
                "Higher-rated agents appear to take longer to close deals."
            )

        else:
            st.info(
                "Little or no relationship exists between agent rating and closing speed."
            )

        # ---------------------------------------
        # Scatter Plot
        # ---------------------------------------
        fig = px.scatter(
            rating_df,
            x="rating",
            y="avg_days_to_close",
            size="total_sales",
            color="rating",
            hover_name="name",
            title="Agent Rating vs Average Days to Close"
        )

        fig.update_layout(
            xaxis_title="Agent Rating",
            yaxis_title="Average Days to Close",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Rating Categories
        # ---------------------------------------
        summary_query = """
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
                WHEN rating_category='Excellent (4.5-5.0)' THEN 1
                WHEN rating_category='Good (4.0-4.49)' THEN 2
                WHEN rating_category='Average (3.5-3.99)' THEN 3
                ELSE 4
            END;
        """

        rating_group_df = pd.read_sql(summary_query, conn)

        st.subheader("Average Closing Time by Rating Category")

        st.dataframe(rating_group_df)

        fig = px.bar(
            rating_group_df,
            x="rating_category",
            y="avg_days_to_close",
            color="avg_days_to_close",
            text_auto=".2f",
            title="Average Days to Close by Agent Rating"
        )

        fig.update_layout(
            xaxis_title="Rating Category",
            yaxis_title="Average Days to Close",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)
    
    elif question == "24. What is the average commission earned by each agent?":

        st.subheader("Average Commission Earned by Each Agent")

        # ---------------------------------------
        # Average Commission Earned
        # ---------------------------------------
        query = """
        SELECT
            a.agent_id,
            a.name,
            a.commission_rate,
            COUNT(s.listing_id) AS total_sales_closed,
            ROUND(AVG(s.sale_price), 2) AS average_sale_price,
            ROUND(
                AVG(s.sale_price * (a.commission_rate / 100)),
                2
            ) AS average_commission_earned
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

        commission_df = pd.read_sql(query, conn)

        st.dataframe(commission_df)

        fig = px.bar(
            commission_df,
            x="name",
            y="average_commission_earned",
            color="average_commission_earned",
            text_auto=".2f",
            hover_data=[
                "commission_rate",
                "total_sales_closed",
                "average_sale_price"
            ],
            title="Average Commission Earned by Agent"
        )

        fig.update_layout(
            xaxis_title="Agent",
            yaxis_title="Average Commission Earned",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Total Commission Earned
        # ---------------------------------------
        st.subheader("Total Commission Earned by Each Agent")

        total_query = """
        SELECT
            a.agent_id,
            a.name,
            COUNT(s.listing_id) AS total_sales_closed,
            ROUND(
                SUM(s.sale_price * (a.commission_rate / 100)),
                2
            ) AS total_commission_earned
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

        total_commission_df = pd.read_sql(total_query, conn)

        st.dataframe(total_commission_df)

        fig = px.bar(
            total_commission_df,
            x="name",
            y="total_commission_earned",
            color="total_commission_earned",
            text_auto=".2f",
            hover_data=["total_sales_closed"],
            title="Total Commission Earned by Agent"
        )

        fig.update_layout(
            xaxis_title="Agent",
            yaxis_title="Total Commission Earned",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)


    elif question == "25. Which agents currently have the most active listings?":

        st.subheader("Agents with the Most Active Listings")

        # ---------------------------------------
        # Active Listings by Agent
        # ---------------------------------------
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

        active_listing_df = pd.read_sql(query, conn)

        st.dataframe(active_listing_df)

        fig = px.bar(
            active_listing_df,
            x="name",
            y="active_listings",
            color="active_listings",
            text_auto=True,
            title="Number of Active Listings by Agent"
        )

        fig.update_layout(
            xaxis_title="Agent",
            yaxis_title="Active Listings",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Top 10 Agents
        # ---------------------------------------
        st.subheader("Top 10 Agents with the Most Active Listings")

        top10_query = """
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

        top10_df = pd.read_sql(top10_query, conn)

        st.dataframe(top10_df)

        fig = px.bar(
            top10_df,
            x="name",
            y="active_listings",
            color="active_listings",
            text_auto=True,
            title="Top 10 Agents by Active Listings"
        )

        fig.update_layout(
            xaxis_title="Agent",
            yaxis_title="Active Listings",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)


elif dashboard == "Buyer & Financing":
    st.title("📊 Buyer & Financing")

    question = st.selectbox(
        "Select Analysis",
        [
            "26. What percentage of buyers are investors vs end users?",
            "27. Which cities have the highest loan uptake rate?",
            "28. What is the average loan amount by buyer type?",
            "29. Which payment mode is most commonly used?",
            "30. Do loan-backed purchases take longer to close?"
        ]
    )
    
    if question == "26. What percentage of buyers are investors vs end users?":

        st.subheader("Investor vs End User Distribution")

        # ---------------------------------------
        # Buyer Type Distribution
        # ---------------------------------------
        query = """
        SELECT
            buyer_type,
            COUNT(*) AS total_buyers,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM buyers),
                2
            ) AS percentage
        FROM buyers
        GROUP BY buyer_type
        ORDER BY percentage DESC;
        """

        buyer_type_df = pd.read_sql(query, conn)

        st.dataframe(buyer_type_df)

        # ---------------------------------------
        # Pie Chart
        # ---------------------------------------
        fig = px.pie(
            buyer_type_df,
            names="buyer_type",
            values="total_buyers",
            title="Investor vs End User Distribution",
            hole=0.35
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Bar Chart
        # ---------------------------------------
        fig = px.bar(
            buyer_type_df,
            x="buyer_type",
            y="percentage",
            color="percentage",
            text_auto=".2f",
            title="Percentage of Buyers by Buyer Type"
        )

        fig.update_layout(
            xaxis_title="Buyer Type",
            yaxis_title="Percentage (%)",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    
    elif question == "27. Which cities have the highest loan uptake rate?":

        st.subheader("Loan Uptake Rate by City")

        query = """
        SELECT
            l.city,
            COUNT(b.buyer_id) AS total_buyers,

            SUM(
                CASE
                    WHEN b.loan_taken = TRUE THEN 1
                    ELSE 0
                END
            ) AS buyers_with_loan,

            ROUND(
                SUM(
                    CASE
                        WHEN b.loan_taken = TRUE THEN 1
                        ELSE 0
                    END
                ) * 100.0 / COUNT(b.buyer_id),
                2
            ) AS loan_uptake_rate

        FROM buyers b

        JOIN sales s
            ON b.sale_id = s.listing_id

        JOIN listings l
            ON s.listing_id = l.listing_id

        GROUP BY l.city

        ORDER BY loan_uptake_rate DESC;
        """

        loan_city_df = pd.read_sql(query, conn)

        st.dataframe(loan_city_df)

        fig = px.bar(
            loan_city_df,
            x="city",
            y="loan_uptake_rate",
            color="loan_uptake_rate",
            text_auto=".2f",
            title="Loan Uptake Rate by City"
        )

        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Loan Uptake Rate (%)",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        fig = px.pie(
            loan_city_df,
            names="city",
            values="buyers_with_loan",
            hole=0.4,
            title="Distribution of Loan-backed Buyers by City"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(fig, use_container_width=True)
    

    elif question == "28. What is the average loan amount by buyer type?":

        st.subheader("Average Loan Amount by Buyer Type")

        # ---------------------------------------
        # Average Loan Amount by Buyer Type
        # ---------------------------------------
        query = """
        SELECT
            buyer_type,
            COUNT(*) AS total_buyers,

            SUM(
                CASE
                    WHEN loan_taken = TRUE THEN 1
                    ELSE 0
                END
            ) AS buyers_with_loan,

            ROUND(
                AVG(
                    CASE
                        WHEN loan_taken = TRUE THEN loan_amount
                        ELSE NULL
                    END
                ),
                2
            ) AS average_loan_amount

        FROM buyers

        GROUP BY buyer_type

        ORDER BY average_loan_amount DESC;
        """

        loan_df = pd.read_sql(query, conn)

        st.dataframe(loan_df)

        # ---------------------------------------
        # Bar Chart
        # ---------------------------------------
        fig = px.bar(
            loan_df,
            x="buyer_type",
            y="average_loan_amount",
            color="average_loan_amount",
            text_auto=".2f",
            hover_data=[
                "total_buyers",
                "buyers_with_loan"
            ],
            title="Average Loan Amount by Buyer Type"
        )

        fig.update_layout(
            xaxis_title="Buyer Type",
            yaxis_title="Average Loan Amount",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Loan-backed Buyers by Buyer Type
        # ---------------------------------------
        fig = px.pie(
            loan_df,
            names="buyer_type",
            values="buyers_with_loan",
            hole=0.4,
            title="Loan-backed Buyers by Buyer Type"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(fig, use_container_width=True)

    
    elif question == "29. Which payment mode is most commonly used?":

        st.subheader("Most Commonly Used Payment Mode")

        # ---------------------------------------
        # Payment Mode Distribution
        # ---------------------------------------
        query = """
        SELECT
            payment_mode,
            COUNT(*) AS total_transactions,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM buyers),
                2
            ) AS percentage
        FROM buyers
        GROUP BY payment_mode
        ORDER BY total_transactions DESC;
        """

        payment_df = pd.read_sql(query, conn)

        st.dataframe(payment_df)

        # ---------------------------------------
        # Most Common Payment Mode
        # ---------------------------------------
        top_payment = payment_df.iloc[0]

        st.metric(
            label="Most Common Payment Mode",
            value=top_payment["payment_mode"],
            delta=f'{int(top_payment["total_transactions"])} Transactions'
        )

        # ---------------------------------------
        # Bar Chart
        # ---------------------------------------
        fig = px.bar(
            payment_df,
            x="payment_mode",
            y="total_transactions",
            color="total_transactions",
            text_auto=True,
            title="Number of Transactions by Payment Mode"
        )

        fig.update_layout(
            xaxis_title="Payment Mode",
            yaxis_title="Total Transactions",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Pie Chart
        # ---------------------------------------
        fig = px.pie(
            payment_df,
            names="payment_mode",
            values="total_transactions",
            hole=0.4,
            title="Distribution of Payment Modes"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Show Most Common Payment Mode
        # ---------------------------------------
        query = """
        SELECT
            payment_mode,
            COUNT(*) AS total_transactions
        FROM buyers
        GROUP BY payment_mode
        ORDER BY total_transactions DESC
        LIMIT 1;
        """

        result = pd.read_sql(query, conn)

        st.success(
            f"Most Common Payment Mode: **{result.iloc[0]['payment_mode']}** "
            f"({int(result.iloc[0]['total_transactions'])} Transactions)"
        )
    
    elif question == "30. Do loan-backed purchases take longer to close?":

        st.subheader("Loan-backed Purchases vs Non-loan Purchases")

        # ---------------------------------------
        # Query
        # ---------------------------------------
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
            ON b.sale_id = s.listing_id

        GROUP BY loan_status

        ORDER BY avg_days_to_close DESC;
        """

        loan_close_df = pd.read_sql(query, conn)

        # ---------------------------------------
        # Display Data
        # ---------------------------------------
        st.dataframe(loan_close_df)

        # ---------------------------------------
        # Metric
        # ---------------------------------------
        longest = loan_close_df.loc[
            loan_close_df["avg_days_to_close"].idxmax()
        ]

        st.metric(
            label="Longest Average Closing Time",
            value=longest["loan_status"],
            delta=f'{longest["avg_days_to_close"]:.2f} Days'
        )

        # ---------------------------------------
        # Bar Chart
        # ---------------------------------------
        fig = px.bar(
            loan_close_df,
            x="loan_status",
            y="avg_days_to_close",
            color="avg_days_to_close",
            text_auto=".2f",
            title="Average Time to Close by Loan Status"
        )

        fig.update_layout(
            xaxis_title="Loan Status",
            yaxis_title="Average Days to Close",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Pie Chart
        # ---------------------------------------
        fig = px.pie(
            loan_close_df,
            names="loan_status",
            values="total_purchases",
            hole=0.45,
            title="Loan-backed vs Non-loan Purchases"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------
        # Interpretation
        # ---------------------------------------
        loan_days = loan_close_df.loc[
            loan_close_df["loan_status"] == "Loan Taken",
            "avg_days_to_close"
        ].values[0]

        no_loan_days = loan_close_df.loc[
            loan_close_df["loan_status"] == "No Loan",
            "avg_days_to_close"
        ].values[0]

        if loan_days > no_loan_days:
            st.info(
                f"Loan-backed purchases take longer to close on average "
                f"({loan_days:.2f} days) than non-loan purchases "
                f"({no_loan_days:.2f} days)."
            )
        elif loan_days < no_loan_days:
            st.info(
                f"Non-loan purchases take longer to close on average "
                f"({no_loan_days:.2f} days) than loan-backed purchases "
                f"({loan_days:.2f} days)."
            )
        else:
            st.info(
                "Both loan-backed and non-loan purchases have the same average closing time."
            )




if page == "🛠 CRUD Operation":

    st.title("🛠 CRUD Operations")

    crud_option = st.sidebar.radio(
        "Select Table",
        (
            "Listings",
            "Agents",
            "Buyers",
            "Sales",
            "Property Attributes"
        )
    )

    if crud_option == "Listings":
        st.header("Listings CRUD")
        # Paste Listings CRUD code here

    elif crud_option == "Agents":
        st.header("Agents CRUD")
        # Paste Agents CRUD code here

    elif crud_option == "Buyers":
        st.header("Buyers CRUD")
        # Paste Buyers CRUD code here

    elif crud_option == "Sales":
        st.header("Sales CRUD")
        # Paste Sales CRUD code here

    elif crud_option == "Property Attributes":
        st.header("Property Attributes CRUD")