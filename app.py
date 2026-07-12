import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm

import mysql.connector

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="700234OMk#",
        database="real_estate"
    )


st.sidebar.title("🏠 BrickView Dashboard")

page = st.sidebar.radio(
    "Select Module",
    (
        "🏠 BrickView Real Estate Listings Dashboard",
        "🧑‍💼 BrickView Real Estate Agents Dashboard",
        "🧍 BrickView Buyers Dashboard",
        "💰 BrickView Sales Dashboard",
        "🏢 BrickView Property Attributes Dashboard",
        "🛠 CRUD Operation",
        "📊 BrickView SQL Query Dashboard"
    )
)



# ---------------------------------------------------
# Page Configuration (Listings)
# ---------------------------------------------------

if page == "🏠 BrickView Real Estate Listings Dashboard":

    st.set_page_config(
        page_title="BrickView - Listings",
        page_icon="🏠",
        layout="wide"
    )

    st.title("🏠 BrickView Real Estate Listings Dashboard")

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

    @st.cache_data
    def load_data():
        df = pd.read_json("listings_final_expanded.json")
        df["Date_Listed"] = pd.to_datetime(df["Date_Listed"])
        return df

    df = load_data()

# ---------------------------------------------------
# Filters
# ---------------------------------------------------

    st.header("Filter Listings")

    city = st.multiselect(
        "Select City",
        options=sorted(df["City"].unique()),
        default=sorted(df["City"].unique())
    )

    property_type = st.multiselect(
        "Property Type",
        options=sorted(df["Property_Type"].unique()),
        default=sorted(df["Property_Type"].unique())
    )

    price_range = st.slider(
        "Price Range ($)",
        int(df["Price"].min()),
        int(df["Price"].max()),
        (
            int(df["Price"].min()),
            int(df["Price"].max())
        )
    )

    filtered_df = df[
        (df["City"].isin(city)) &
        (df["Property_Type"].isin(property_type)) &
        (df["Price"] >= price_range[0]) &
        (df["Price"] <= price_range[1])
    ]

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

    total_listings = len(filtered_df)
    avg_price = filtered_df["Price"].mean()
    avg_sqft = filtered_df["Sqft"].mean()
    max_price = filtered_df["Price"].max()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Listings", total_listings)
    c2.metric("Average Price", f"${avg_price:,.0f}")
    c3.metric("Average Sqft", f"{avg_sqft:,.0f}")
    c4.metric("Highest Price", f"${max_price:,.0f}")

    st.divider()

# ---------------------------------------------------
# Listings by City
# ---------------------------------------------------

    city_chart = (
        filtered_df.groupby("City")
        .size()
        .reset_index(name="Listings")
    )

    fig = px.bar(
        city_chart,
        x="City",
        y="Listings",
        color="City",
        title="Listings by City"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.header("Filter Listings")

# ---------------------------------------------------
# Property Type Distribution
# ---------------------------------------------------

    fig = px.pie(
        filtered_df,
        names="Property_Type",
        title="Property Type Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Average Price by City
# ---------------------------------------------------

    price_city = (
        filtered_df.groupby("City")["Price"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        price_city,
        x="City",
        y="Price",
        color="City",
        title="Average Property Price by City"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Price Distribution
# ---------------------------------------------------

    fig = px.histogram(
        filtered_df,
        x="Price",
        nbins=30,
        title="Property Price Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Sqft vs Price
# ---------------------------------------------------

    fig = px.scatter(
        filtered_df,
        x="Sqft",
        y="Price",
        color="Property_Type",
        hover_data=["City"],
        title="Property Size vs Price"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Listings Over Time
# ---------------------------------------------------

    monthly = filtered_df.copy()

    monthly["Month"] = monthly["Date_Listed"].dt.to_period("M").astype(str)

    trend = (
        monthly.groupby("Month")
        .size()
        .reset_index(name="Listings")
    )

    fig = px.line(
        trend,
        x="Month",
        y="Listings",
        markers=True,
        title="Monthly Listings Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Interactive Table
# ---------------------------------------------------

    st.subheader("Property Listings")

    st.dataframe(
        filtered_df.sort_values("Price", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------
# Download
# ---------------------------------------------------

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        "📥 Download Listings",
        csv,
        file_name="filtered_listings.csv",
        mime="text/csv"
    )



# -------------------------------------------------
# Page Configuration (Agents)
# -------------------------------------------------

if page == "🧑‍💼 BrickView Real Estate Agents Dashboard":

    st.set_page_config(
        page_title="BrickView - Agents Dashboard",
        page_icon="👨‍💼",
        layout="wide"
    )

    st.title("👨‍💼 BrickView Real Estate Agents Dashboard")

# -------------------------------------------------
# Load Data
# -------------------------------------------------

    @st.cache_data
    def load_data():
        return pd.read_json("agents_cleaned.json")

    df = load_data()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

    st.header("Filters")

    rating = st.slider(
        "Minimum Rating",
        float(df["rating"].min()),
        float(df["rating"].max()),
        float(df["rating"].min()),
        step=0.1
    )

    experience = st.slider(
        "Minimum Experience (Years)",
        int(df["experience_years"].min()),
        int(df["experience_years"].max()),
        int(df["experience_years"].min())
    )

    filtered = df[
        (df["rating"] >= rating) &
        (df["experience_years"] >= experience)
    ]

# -------------------------------------------------
# KPIs
# -------------------------------------------------

    total_agents = len(filtered)
    avg_rating = filtered["rating"].mean()
    total_deals = filtered["deals_closed"].sum()
    avg_commission = filtered["commission_rate"].mean()
    avg_closing = filtered["avg_closing_days"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Agents", total_agents)
    c2.metric("Average Rating", f"{avg_rating:.2f}")
    c3.metric("Deals Closed", f"{total_deals:,}")
    c4.metric("Avg Commission", f"{avg_commission:.2f}%")
    c5.metric("Avg Closing Days", f"{avg_closing:.1f}")

    st.divider()

# -------------------------------------------------
# Top 10 Agents
# -------------------------------------------------

    st.subheader("🏆 Top 10 Agents by Deals Closed")

    top_agents = filtered.sort_values(
        "deals_closed",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_agents,
        x="Name",
        y="deals_closed",
        color="rating",
        title="Top Performing Agents",
        text="deals_closed"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Rating Distribution
# -------------------------------------------------

    fig = px.histogram(
        filtered,
        x="rating",
        nbins=15,
        title="Agent Rating Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Experience Distribution
# -------------------------------------------------

    fig = px.histogram(
        filtered,
        x="experience_years",
        nbins=20,
        title="Experience Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Deals Closed vs Experience
# -------------------------------------------------

    fig = px.scatter(
        filtered,
        x="experience_years",
        y="deals_closed",
        size="rating",
        hover_name="Name",
        color="commission_rate",
        title="Experience vs Deals Closed"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Commission Rate Distribution
# -------------------------------------------------

    fig = px.box(
        filtered,
        y="commission_rate",
        title="Commission Rate Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Avg Closing Days
# -------------------------------------------------

    fig = px.scatter(
        filtered,
        x="avg_closing_days",
        y="deals_closed",
        color="rating",
        hover_name="Name",
        title="Closing Time vs Deals Closed"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Top Rated Agents
# -------------------------------------------------

    st.subheader("⭐ Highest Rated Agents")

    top_rated = filtered.sort_values(
        ["rating", "deals_closed"],
        ascending=False
    ).head(10)

    st.dataframe(
        top_rated[
            [
                "Agent_ID",
                "Name",
                "rating",
                "experience_years",
                "deals_closed",
                "commission_rate",
                "avg_closing_days"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------
# Complete Dataset
# -------------------------------------------------

    with st.expander("View All Agents"):

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

# -------------------------------------------------
# Download
# -------------------------------------------------

    csv = filtered.to_csv(index=False)

    st.download_button(
        "📥 Download Agent Data",
        csv,
        "agents_dashboard.csv",
        "text/csv"
    )

# -------------------------
# Page Config (buyers)
# -------------------------

if page == "🧍 BrickView Buyers Dashboard":

    st.set_page_config(
        page_title="BrickView - Buyers Dashboard",
        page_icon="👤",
        layout="wide"
    )

    st.title("👤 BrickView Buyers Dashboard")

# -------------------------
# Load Data
# -------------------------
    @st.cache_data
    def load_data():
        return pd.read_json("buyers_cleaned.json")

    df = load_data()

# -------------------------
# Sidebar
# -------------------------

    st.header("Filters")

    buyer_types = st.multiselect(
        "Buyer Type",
        sorted(df["buyer_type"].unique()),
        default=sorted(df["buyer_type"].unique())
    )

    payment_modes = st.multiselect(
        "Payment Mode",
        sorted(df["payment_mode"].unique()),
        default=sorted(df["payment_mode"].unique())
    )

    loan_filter = st.selectbox(
        "Loan Taken",
        ["All", "Yes", "No"]
    )

    filtered = df[
        (df["buyer_type"].isin(buyer_types)) &
        (df["payment_mode"].isin(payment_modes))
    ]

    if loan_filter == "Yes":
        filtered = filtered[filtered["loan_taken"] == True]

    elif loan_filter == "No":
        filtered = filtered[filtered["loan_taken"] == False]

# -------------------------
# KPIs
# -------------------------

    total_buyers = len(filtered)
    loan_buyers = filtered["loan_taken"].sum()
    cash_buyers = (filtered["payment_mode"] == "Cash").sum()
    avg_loan = filtered["loan_amount"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Buyers", total_buyers)
    c2.metric("Loan Buyers", loan_buyers)
    c3.metric("Cash Buyers", cash_buyers)
    c4.metric("Average Loan Amount", f"${avg_loan:,.0f}")

    st.divider()

# -------------------------
# Buyer Type
# -------------------------

    buyer_chart = (
        filtered["buyer_type"]
        .value_counts()
        .reset_index()
    )

    buyer_chart.columns = ["Buyer Type", "Count"]

    fig = px.bar(
        buyer_chart,
        x="Buyer Type",
        y="Count",
        color="Buyer Type",
        title="Buyer Type Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Payment Mode
# -------------------------

    fig = px.pie(
        filtered,
        names="payment_mode",
        title="Payment Mode Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Loan Status
# -------------------------

    loan_df = (
        filtered["loan_taken"]
        .value_counts()
        .reset_index()
    )

    loan_df.columns = ["Loan Taken", "Count"]

    loan_df["Loan Taken"] = loan_df["Loan Taken"].replace({
        True: "Yes",
        False: "No"
    })

    fig = px.bar(
        loan_df,
        x="Loan Taken",
        y="Count",
        color="Loan Taken",
        title="Loan Taken vs Not Taken"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Loan Provider
# -------------------------

    provider = filtered[filtered["loan_taken"] == True]

    if not provider.empty:

        provider_chart = (
            provider["loan_provider"]
            .value_counts()
            .reset_index()
        )

        provider_chart.columns = ["Loan Provider", "Count"]

        fig = px.bar(
            provider_chart,
            x="Loan Provider",
            y="Count",
            color="Loan Provider",
            title="Loan Provider Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Loan Amount
# -------------------------

    loan_amount = provider[provider["loan_amount"] > 0]

    if not loan_amount.empty:

        fig = px.histogram(
            loan_amount,
            x="loan_amount",
            nbins=30,
            title="Loan Amount Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Average Loan by Provider
# -------------------------

    if not provider.empty:

        avg = (
            provider.groupby("loan_provider")["loan_amount"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            avg,
            x="loan_provider",
            y="loan_amount",
            color="loan_provider",
            title="Average Loan Amount by Provider"
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Data Table
# -------------------------

    st.subheader("Buyer Transactions")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

# -------------------------
# Download
# -------------------------

    csv = filtered.to_csv(index=False)

    st.download_button(
        "Download Buyer Data",
        csv,
        "buyers.csv",
        "text/csv"
    )



#-----------------------
#SALES DASHBOARD
#------------------------

if page == "💰 BrickView Sales Dashboard":


    st.set_page_config(
        page_title="BrickView - Sales Dashboard",
        page_icon="👨‍💼",
        layout="wide"
    )

    st.title("Sales Dashboard")
    def load_data():
        df = pd.read_csv("sales_cleaned.csv")
        df["Date_Sold"] = pd.to_datetime(df["Date_Sold"])
        return df

    df = load_data()

    st.header("Filters")

    min_date = df["Date_Sold"].min()
    max_date = df["Date_Sold"].max()

    date_range = st.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    if isinstance(date_range, tuple):
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    filtered_df = df[
        (df["Date_Sold"] >= pd.to_datetime(start_date)) &
        (df["Date_Sold"] <= pd.to_datetime(end_date))
    ]


    total_sales = filtered_df["Sale_Price"].sum()
    avg_price = filtered_df["Sale_Price"].mean()
    max_price = filtered_df["Sale_Price"].max()
    avg_days = filtered_df["Days_on_Market"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Average Sale Price", f"${avg_price:,.0f}")
    col3.metric("Highest Sale Price", f"${max_price:,.0f}")
    col4.metric("Avg Days on Market", f"{avg_days:.1f}")

    st.divider()


    import plotly.express as px


    monthly = filtered_df.copy()
    monthly["Month"] = monthly["Date_Sold"].dt.to_period("M").astype(str)

    monthly_sales = (
        monthly.groupby("Month")["Sale_Price"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Month",
        y="Sale_Price",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Sale Price Distribution
# -------------------------
    fig = px.histogram(
        filtered_df,
        x="Sale_Price",
        nbins=30,
        title="Sale Price Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


# -------------------------
# Days on Market Distribution
# -------------------------
    fig = px.box(
        filtered_df,
        y="Days_on_Market",
        title="Days on Market"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Top 10 Highest Sales
# -------------------------
    st.subheader("Top 10 Property Sales")

    top_sales = filtered_df.sort_values(
        by="Sale_Price",
        ascending=False
    ).head(10)

    st.dataframe(top_sales, use_container_width=True)

# -------------------------
# Dataset
# -------------------------
    with st.expander("View Sales Dataset"):
        st.dataframe(filtered_df, use_container_width=True)

# -------------------------------------------------
# Page Configuration (Property Attributes)
# -------------------------------------------------

    st.set_page_config(
        page_title="BrickView - Property Attributes Dashboard",
        page_icon="👨‍💼",
        layout="wide"
)


##-------------------------
###Property Attributes
##-------------------------

if page == "🏢 BrickView Property Attributes Dashboard":


    st.title("👨‍💼 BrickView Property Attributes Dashboard")

# -------------------------------------------------
# Load Data
# -------------------------------------------------

    @st.cache_data
    def load_data():
        return pd.read_json("property_attributes_final_expanded.json")

    df = load_data()

# ----------------- SIDEBAR FILTERS -----------------
    st.header("📊 Filter Framework")

# Furnishing Status Multi-select
    furnishing_options = df["furnishing_status"].unique()
    selected_furnishing = st.multiselect(
        "Furnishing Status", 
        options=furnishing_options, 
        default=furnishing_options
    )

# Rental Status Filter
    rental_status = st.radio("Rental Status", ["All", "Rented Only", "Vacant Only"])

# Slider for Metro Distance
    max_metro = float(df["metro_distance_km"].max())
    min_metro = float(df["metro_distance_km"].min())
    selected_metro_range = st.slider(
        "Metro Distance Range (km)", 
        min_value=min_metro, 
        max_value=max_metro, 
        value=(min_metro, max_metro),
        step=0.1
    )

# Numeric filter limits
    bedroom_options = sorted(df["bedrooms"].unique())
    selected_bedrooms = st.multiselect("Bedrooms Count", options=bedroom_options, default=bedroom_options)

# Filter Application Logic
    filtered_df = df[
        (df["furnishing_status"].isin(selected_furnishing)) &
        (df["metro_distance_km"].between(selected_metro_range[0], selected_metro_range[1])) &
        (df["bedrooms"].isin(selected_bedrooms))
    ]

    if rental_status == "Rented Only":
        filtered_df = filtered_df[filtered_df["is_rented"] == True]
    elif rental_status == "Vacant Only":
        filtered_df = filtered_df[filtered_df["is_rented"] == False]

# ----------------- MAIN LAYOUT -----------------
    st.title("🏢 Real Estate Property Attributes Dashboard")
    st.markdown("An active visual playground generated from underlying asset configuration telemetry.")
    st.markdown("---")

# 1. Key Metrics Ribbon
    if not filtered_df.empty:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Matches", len(filtered_df))
        with m2:
            st.metric("Avg Metro Distance", f"{filtered_df['metro_distance_km'].mean():.2f} km")
        with m3:
            rented_pct = (filtered_df["is_rented"].sum() / len(filtered_df)) * 100
            st.metric("Occupancy / Rent Rate", f"{rented_pct:.1f}%")
        with m4:
            st.metric("Avg Year Built", int(filtered_df["year_built"].mean()))
    else:
        st.warning("⚠️ No records match the current filter selection configuration framework.")

    st.markdown("---")

# 2. Graphical Analytics Grid
    if not filtered_df.empty:
        chart_col1, chart_col2 = st.columns(2)
    
        with chart_col1:
            st.subheader("🛋️ Furnishing Breakdown & Rental Distribution")
            fig_furn = px.histogram(
                filtered_df, 
                x="furnishing_status", 
                color="is_rented",
                barmode="group",
                labels={"furnishing_status": "Status", "is_rented": "Is Rented"},
                color_discrete_map={True: "#1E88E5", False: "#FFB300"}
            )
            st.plotly_chart(fig_furn, use_container_width=True)
        
        with chart_col2:
            st.subheader("⏳ Metro Distance vs. Asset Era (Year Built)")
            fig_scatter = px.scatter(
                filtered_df, 
                x="year_built", 
                y="metro_distance_km", 
                color="bedrooms",
                size="bathrooms",
                hover_name="listing_id",
                labels={"year_built": "Year Built", "metro_distance_km": "Metro Distance (km)"},
                color_continuous_scale=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("---")
    
    # 3. Dynamic Amenities Breakdowns
        st.subheader("⚡ Amenity Availability Vectors")
        a1, a2 = st.columns(2)
        with a1:
            parking_count = filtered_df["parking_available"].value_counts().to_frame().reset_index()
            fig_park = px.pie(parking_count, names="parking_available", values="count", title="Dedicated Parking Availability", hole=0.4)
            st.plotly_chart(fig_park, use_container_width=True)
        with a2:
            backup_count = filtered_df["power_backup"].value_counts().to_frame().reset_index()
            fig_back = px.pie(backup_count, names="power_backup", values="count", title="Power Backup Integration Status", hole=0.4)
            st.plotly_chart(fig_back, use_container_width=True)

        st.markdown("---")

    # 4. Filtered Tabular Inspection Matrix
        st.subheader("📋 Granular Dataset Explorer")
        st.dataframe(
            filtered_df.drop(columns=["attribute_id"]), 
            use_container_width=True,
            column_config={
                "listing_id": "Listing ID",
                "bedrooms": "Bedrooms",
                "bathrooms": "Bathrooms",
                "floor_number": "Floor No.",
                "total_floors": "Total Storeys",
                "year_built": "Construction Year",
                "is_rented": "Leased Status",
                "tenant_count": "Active Occupants",
                "furnishing_status": "Furnishing Context",
                "metro_distance_km": st.column_config.NumberColumn("Metro Range", format="%.2f km"),
                "parking_available": "Parking Space",
                "power_backup": "Generator Grid"
            }
        )



####---------------------
#CRUD
###-------------------------
#listings_crud
import streamlit as st
import pandas as pd

if page == "🛠 CRUD Operation":

    st.set_page_config(page_title="Listings CRUD", layout="wide")

    st.title("🏠 Listings Management")

    tabs = st.tabs(["Create", "Read", "Update", "Delete"])


#CREATE

    with tabs[0]:

        st.subheader("Add New Listing")

        listing_id = st.number_input("Listing ID", step=1)

        address = st.text_input("Address")

        city = st.text_input("City")

        state = st.text_input("State")

        zipcode = st.text_input("Zip Code")

        property_type = st.selectbox(
            "Property Type",
            ["Apartment", "Villa", "Independent House", "Commercial", "Plot"]
        )

        price = st.number_input("Price", min_value=0.0)

        area = st.number_input("Area (Sqft)", step=1)

        agent_id = st.number_input("Agent ID", step=1)

        listed_date = st.date_input("Listed Date")

        if st.button("Create Listing"):

            conn = get_connection()
            cursor = conn.cursor()

            sql = """
            INSERT INTO listings
            (listing_id,address,city,state,zip,property_type,
            price,area_sqft,agent_id,listed_date)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(sql,(
                listing_id,
                address,
                city,
                state,
                zipcode,
                property_type,
                price,
                area,
                agent_id,
                listed_date
            ))

            conn.commit()

            st.success("Listing Added Successfully")

            cursor.close()
            conn.close()


#READ

    with tabs[1]:
 
        st.subheader("View Listings")

        conn = get_connection()

        df = pd.read_sql("SELECT * FROM listings", conn)

        conn.close()

        st.dataframe(df, use_container_width=True)

#UPDATE

    with tabs[2]:
   
        st.subheader("Update Listing")
 
        conn = get_connection()

        df = pd.read_sql("SELECT * FROM listings", conn)

        conn.close()

        listing = st.selectbox(
            "Select Listing",
            df["listing_id"]
        )

        row = df[df["listing_id"] == listing].iloc[0]

        new_price = st.number_input(
            "Price",
            value=float(row["price"])
        )

        new_city = st.text_input(
            "City",
            value=row["city"]
        )

        if st.button("Update Listing"):
  
            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE listings
            SET
            city=%s,
            price=%s
            WHERE listing_id=%s
            """,
            (
                new_city,
                new_price,
                listing
            ))

            conn.commit()

            st.success("Listing Updated Successfully")

            cursor.close()
            conn.close()

#DELETE

    with tabs[3]:

        st.subheader("Delete Listing")

        conn = get_connection()

        df = pd.read_sql("SELECT * FROM listings", conn)

        conn.close()

        listing = st.selectbox(
            "Listing",
            df["listing_id"]
        )

        if st.button("Delete Listing"):
 
            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM listings WHERE listing_id=%s",
                (listing,)
            )

            conn.commit()

            st.success("Listing Deleted Successfully")

            cursor.close()

            conn.close()

#---------------------
#Create CRUD for agents
#----------------------

#Import libraries

    import streamlit as st
    import pandas as pd


#Select Database Table
    st.title("AGENTS CRUD OPERATION")


#Create Tabs

    create_tab, read_tab, update_tab, delete_tab = st.tabs(
        [
            "Create",
            "Read",
            "Update",
            "Delete"
        ]
    )

#CREATE Operation
#Agents

    with create_tab:

        st.header("Add Agent")

        agent_id = st.text_input("Agent ID")

        name = st.text_input("Name")

        phone = st.text_input("Phone")

        email = st.text_input("Email")

        commission = st.number_input("Commission Rate")

        deals = st.number_input("Deals Closed", step=1)

        rating = st.number_input("Rating")

        experience = st.number_input("Experience")

        closing = st.number_input("Average Closing Days")

        if st.button("Save Agent"):

            conn = get_connection()

            cursor = conn.cursor()

            sql = """
            INSERT INTO agents
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(sql,
            (
                agent_id,
                name,
                phone,
                email,
                commission,
                deals,
                rating,
                experience,
                closing
            ))

            conn.commit()

            st.success("Agent Added Successfully")

            cursor.close()

            conn.close()


#READ Operation

    with read_tab:

        conn = get_connection()

        query = "SELECT * FROM agents"

        df = pd.read_sql(query, conn)

        st.dataframe(df)

        conn.close()


#UPDATE Operation

    with update_tab:

        conn = get_connection()

        df = pd.read_sql("SELECT * FROM agents", conn)

        conn.close()

        selected = st.selectbox(
            "Select Agent",
            df["agent_id"]
        )

        new_rating = st.number_input("New Rating")

        if st.button("Update"):

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
            """
            UPDATE agents
            SET rating=%s
            WHERE Agent_ID=%s
            """,
            (
                new_rating,
                selected
            ))

            conn.commit()

            st.success("Updated Successfully")

            cursor.close()

            conn.close()


#DELETE Operation

    with delete_tab:

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM agents",
            conn
        )

        conn.close()

        delete_id = st.selectbox(
            "Delete Agent",
            df["agent_id"]
        )

        if st.button("Delete"):

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
            """
            DELETE FROM agents
            WHERE Agent_ID=%s
            """,
            (delete_id,)
            )

            conn.commit()

            st.success("Deleted Successfully")

            cursor.close()

            conn.close()

##----------------------------------
#CRUD operations (buyers)
#---------------------

    st.set_page_config(
        page_title="Buyers CRUD",
        page_icon="👤",
        layout="wide"
    )

    st.title("👤 Buyers Management")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Create", "Read", "Update", "Delete"]
    )



    st.text_input("Loan Provider", key="update_provider")
    st.number_input("Loan Amount", key="create_amount")
    st.number_input("Loan Amount", key="update_amount")
    st.checkbox("Loan Taken", key="create_loan")
    st.checkbox("Loan Taken", key="update_loan")

#CREATE

    with tab1:

        st.subheader("Add New Buyer")

        buyer_id = st.number_input("Buyer ID", step=1)

        sale_id = st.number_input("Sale ID", step=1)

        buyer_type = st.selectbox(
            "Buyer Type",
            ["Investor", "End User"],
            key="create_buyer_type"
        )

        payment_mode = st.selectbox(
            "Payment Mode",
            ["Cash", "Loan"],
            key="create_payment_mode"
        )

        loan_taken = st.checkbox(
            "Loan Taken",
            key="create_loan_taken"
        )

        loan_provider = st.text_input(
            "Loan Provider",
            key="create_loan_provider"
        )

        loan_amount = st.number_input(
            "Loan Amount",
            key="create_loan_amount"
        )

        if st.button("Add Buyer"):

            conn = get_connection()

            cursor = conn.cursor()

            sql = """
            INSERT INTO buyers
            (
            buyer_id,
            sale_id,
            buyer_type,
            payment_mode,
            loan_taken,
            loan_provider,
            loan_amount
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(
                sql,
                (
                    buyer_id,
                    sale_id,
                    buyer_type,
                    payment_mode,
                    loan_taken,
                    loan_provider,
                    loan_amount
                )
            )

            conn.commit()

            st.success("Buyer Added Successfully")

            cursor.close()
            conn.close()

#READ

    with tab2:

        st.subheader("Buyer Records")

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM buyers",
            conn
        )

        conn.close()

        st.dataframe(
            df,
            use_container_width=True
        )

#UPDATE

    with tab3:

        st.subheader("Update Buyer")

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM buyers",
            conn
        )

        conn.close()

# create the selectbox
        selected_buyer = st.selectbox(
            "Select Buyer",
            df["buyer_id"].tolist(),
            key="update_select_buyer"
        )

    # Retrieve the selected buyer
        buyer = df[df["buyer_id"] == selected_buyer].iloc[0]

        buyer_type = st.selectbox(
            "Buyer Type",
            ["Investor", "End User"],
            index=0 if buyer["buyer_type"] == "Investor" else 1,
            key="update_buyer_type"
        )

        payment_mode = st.selectbox(
            "Payment Mode",
            ["Cash", "Loan"],
            index=0 if buyer["payment_mode"] == "Cash" else 1,
            key="update_payment_mode"
        )

        loan_taken = st.checkbox(
            "Loan Taken",
            value=bool(buyer["loan_taken"]),
            key="update_loan_taken"
        )

        loan_provider = st.text_input(
            "Loan Provider",
            value=str(buyer["loan_provider"]),
            key="update_loan_provider"
        )

        loan_amount = st.number_input(
            "Loan Amount",
            value=float(buyer["loan_amount"]),
            key="update_loan_amount"
        )

        if st.button("Update Buyer"):

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE buyers
            SET
            buyer_type=%s,
            payment_mode=%s,
            loan_taken=%s,
            loan_provider=%s,
            loan_amount=%s
            WHERE buyer_id=%s
            """,
            (
                buyer_type,
                payment_mode,
                loan_taken,
                loan_provider,
                loan_amount,
                selected
            ))

            conn.commit()

            st.success("Buyer Updated Successfully")

            cursor.close()

            conn.close()

#DELETE

    with tab4:
  
        st.subheader("Delete Buyer")

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM buyers",
            conn
        )

        conn.close()

        buyer = st.selectbox(
        "Select Buyer",
        df["buyer_id"],
        key="delete_buyer_id"
        )

        confirm = st.checkbox(
            "Confirm Delete"
        )

        if st.button("Delete Buyer") and confirm:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM buyers
                WHERE buyer_id=%s
                """,
                (buyer,)
            )

            conn.commit()

            st.success("Buyer Deleted Successfully")

            cursor.close()

            conn.close()

##---------------------
#CRUD operation (sales)
##--------------------

    st.set_page_config(
        page_title="Sales CRUD",
        page_icon="💰",
        layout="wide"
    )

    st.title("💰 Sales Management")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Create", "Read", "Update", "Delete"]
    )

#CREATE

    with tab1:

        st.subheader("Add Sale")

        listing_id = st.text_input(
        "Listing ID",
        key="create_listingid"
        )

        sale_price = st.number_input(
            "Sale Price",
            min_value=0.0,
            key="create_saleprice"
        )

        date_sold = st.date_input(
            "Date Sold",
            key="create_datesold"
        )

        days = st.number_input(
            "Days on Market",
            step=1,
            key="create_days"
        )

        if st.button("Add Sale", key="create_sale_button"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO sales
            (listing_id,sale_price,date_sold,days_on_market)
            VALUES(%s,%s,%s,%s)
            """,
            (
                listing_id,
                sale_price,
                date_sold,
                days
            ))

            conn.commit()

            st.success("Sale Added Successfully")

            cursor.close()
            conn.close()

#READ

    with tab2:

        st.subheader("Sales Records")

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM sales",
            conn
        )

        conn.close()

        st.dataframe(
            df,
            use_container_width=True
        )

#UPDATE

    with tab3:

        st.subheader("Update Sale")

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM sales",
            conn
        )

        conn.close()

        selected_sale = st.selectbox(
            "Select listing",
            df["listing_id"].tolist(),
            key="update_sale_select"
        )

        sale = df[
            df["listing_id"] == selected_sale
        ].iloc[0]

        listing_id = st.text_input(
        "Listing ID",
        value=sale["listing_id"],
        key="update_listingid"
        )

        sale_price = st.number_input(
            "Sale Price",
            value=float(sale["sale_price"]),
            key="update_saleprice"
        )

        date_sold = st.date_input(
            "Date Sold",
            value=pd.to_datetime(sale["date_sold"]),
            key="update_datesold"
        )

        days = st.number_input(
            "Days on Market",
            value=int(sale["days_on_market"]),
            key="update_days"
        )

        if st.button(
            "Update Sale",
            key="update_sale_button"
        ):

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE sales
            SET
            listing_id=%s,
            sale_price=%s,
            date_sold=%s,
            days_on_market=%s
            WHERE listing_id=%s
            """,
            (
                listing_id,
                sale_price,
                date_sold,
                days,
                selected_sale
            ))

            conn.commit()

            st.success("Sale Updated Successfully")

            cursor.close()
            conn.close()

#DELETE

    with tab4:

        st.subheader("Delete Sale")

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM sales",
            conn
        )

        conn.close()

        sale = st.selectbox(
            "Select listing ID",
            df["listing_id"].tolist(),
            key="delete_listing"
        )

        confirm = st.checkbox(
            "Confirm Delete",
            key="delete_confirm"
        )

        if st.button(
            "Delete Sale",
            key="delete_sale_button"
        ) and confirm:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM sales
                WHERE listing_id=%s
                """,
                (sale,)
            )

            conn.commit()

            st.success("Sale Deleted Successfully")

            cursor.close()
            conn.close()

##-------------------
#CRUD operation (property attributes)
##-------------------

    st.title("🏠 Property Attributes Management")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Create","Read","Update","Delete"]
    )

#CREATE

    with tab1:

        st.subheader("Add Property Attributes")

        attribute_id = st.text_input(
            "Attribute ID",
            key="create_attribute"
        )

        listing_id = st.text_input(
            "Listing ID",
            key="create_listing"
        )

        bedrooms = st.number_input(
            "Bedrooms",
            min_value=0,
            step=1,
            key="create_bedrooms"
        )

        bathrooms = st.number_input(
            "Bathrooms",
            min_value=0.0,
            step=0.5,
            key="create_bathrooms"
        )

        floor_number = st.number_input(
            "Floor Number",
            min_value=0,
            step=1,
            key="create_floor"
        )

        total_floors = st.number_input(
            "Total Floors",
            min_value=0,
            step=1,
            key="create_total_floor"
        )

        year_built = st.number_input(
            "Year Built",
            min_value=1900,
            max_value=2100,
            step=1,
            key="create_year"
        )

        is_rented = st.checkbox(
            "Is Rented",
            key="create_rented"
        ) 

        tenant_count = st.number_input(
            "Tenant Count",
            min_value=0,
            step=1,
            key="create_tenants"
        )

        furnishing_status = st.selectbox(
            "Furnishing Status",
            ["Unfurnished","Semi-Furnished","Fully Furnished"],
            key="create_furnishing"
        )

        metro_distance = st.number_input(
            "Metro Distance (Km)",
            min_value=0.0,
            step=0.1,
            key="create_metro"
        )

        parking = st.checkbox(
            "Parking Available",
            key="create_parking"
        )

        power_backup = st.checkbox(
            "Power Backup",
            key="create_power"
        )


        if st.button("Add Property", key="create_property_button"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO property_attributes
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                attribute_id,
                listing_id,
                bedrooms,
                bathrooms,
                floor_number,
                total_floors,
                year_built,
                is_rented,
                tenant_count,
                furnishing_status,
                metro_distance,
                parking,
                power_backup
            ))

            conn.commit()

            st.success("Property Added Successfully")

            cursor.close()
            conn.close()

#READ

    with tab2:

        st.subheader("Property Attributes")

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM property_attributes",
            conn
        )

        conn.close()

        st.dataframe(
            df,
            use_container_width=True
        )


#UPDATE

    with tab3:

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM property_attributes",
            conn
        )

        conn.close()

        selected = st.selectbox(
            "Select Property",
            df["attribute_id"],
            key="update_property"
        )

        property_data = df[
            df["attribute_id"] == selected
        ].iloc[0]

        bedrooms = st.number_input(
            "Bedrooms",
            value=int(property_data["bedrooms"]),
            key="update_bedrooms"
        )

        bathrooms = st.number_input(
            "Bathrooms",
            value=float(property_data["bathrooms"]),
            key="update_bathrooms"
        )

        furnishing = st.selectbox(
            "Furnishing",
            ["Unfurnished","Semi-Furnished","Fully Furnished"],
            key="update_furnishing"
        )

        parking = st.checkbox(
            "Parking",
            value=bool(property_data["parking_available"]),
            key="update_parking"
        )

        power = st.checkbox(
            "Power Backup",
            value=bool(property_data["power_backup"]),
            key="update_power"
        )

        if st.button(
            "Update Property",
            key="update_property_button"
        ):

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE property_attributes
            SET
            bedrooms=%s,
            bathrooms=%s,
            furnishing_status=%s,
            parking_available=%s,
            power_backup=%s
            WHERE attribute_id=%s
            """,
            (
                bedrooms,
                bathrooms,
                furnishing,
                parking,
                power,
                selected
            ))

            conn.commit()

            st.success("Property Updated Successfully")

            cursor.close()

            conn.close()


#DELETE

    with tab4:

        conn = get_connection()

        df = pd.read_sql(
            "SELECT * FROM property_attributes",
            conn
        )

        conn.close()

        selected = st.selectbox(
            "Select Property",
            df["attribute_id"],
            key="delete_property"
        )

        confirm = st.checkbox(
            "Confirm Delete",
            key="confirm_delete_property"
        )

        if st.button(
            "Delete Property",
            key="delete_property_button"
        ) and confirm:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM property_attributes
                WHERE attribute_id=%s
                """,
                (selected,)
            )

            conn.commit()

            st.success("Property Deleted Successfully")

            cursor.close()

            conn.close()


#SQL query


import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="700234OMk#",
    database="real_estate"
)
cursor = conn.cursor()

if page == "📊 BrickView SQL Query Dashboard":

    st.title("🏠 BrickView SQL Query Dashboard")

    dashboard = st.selectbox(
        "Choose Analysis Category",
        [
            "Property & Pricing",
            "Sales & Market Performance",
            "Agent Performance",
            "Buyer & Financing"
        ]
    )



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