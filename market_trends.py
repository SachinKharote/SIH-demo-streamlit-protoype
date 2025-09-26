# market_trends.py

import streamlit as st
import pandas as pd
import plotly.express as px

def show_market_trends(top_crops, csv_path="commodity_price.csv"):
    """
    Show market price trends for given crops from government CSV.
    
    Parameters:
        top_crops (list): List of crop names to display.
        csv_path (str): Path to the CSV file containing commodity prices.
    """
    try:
        df_market = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.warning(f"CSV file not found: {csv_path}")
        return
    except Exception as e:
        st.warning(f"Error reading CSV: {e}")
        return

    # -------------------------
    # Identify columns
    # -------------------------
    # Find a date column
    date_col = None
    for col in df_market.columns:
        if "date" in col.lower():
            date_col = col
            break
    if not date_col:
        st.warning("No date column found in CSV.")
        return

    # Find crop/commodity column
    crop_col = None
    for col in df_market.columns:
        if "commodity" in col.lower() or "crop" in col.lower():
            crop_col = col
            break
    if not crop_col:
        st.warning("No crop/commodity column found in CSV.")
        return

    # Find price column (modal/min/average)
    price_col = None
    for col in df_market.columns:
        if any(x in col.lower() for x in ["modal", "price", "rate"]):
            price_col = col
            break
    if not price_col:
        st.warning("No price column found in CSV.")
        return

    # -------------------------
    # Preprocess
    # -------------------------
    df_market[date_col] = pd.to_datetime(df_market[date_col], errors='coerce')
    df_market = df_market.dropna(subset=[date_col, crop_col, price_col])
    
    # Filter only top crops
    df_top = df_market[df_market[crop_col].isin(top_crops)]

    if df_top.empty:
        st.warning("No data found for the selected crops in the CSV.")
        return

    # -------------------------
    # Plot
    # -------------------------
    fig = px.line(
        df_top, 
        x=date_col, 
        y=price_col, 
        color=crop_col,
        title="Market Price Trends for Top Crops",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Optional: show latest prices in a table
    latest_prices = df_top.sort_values(date_col).groupby(crop_col).tail(1)
    st.subheader("Latest Prices")
    st.dataframe(latest_prices[[crop_col, price_col, date_col]].reset_index(drop=True))
