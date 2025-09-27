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
    date_col = next((col for col in df_market.columns if "date" in col.lower()), None)
    crop_col = next((col for col in df_market.columns if "commodity" in col.lower() or "crop" in col.lower()), None)
    price_col = next((col for col in df_market.columns if any(x in col.lower() for x in ["modal", "price", "rate"])), None)

    if not date_col or not crop_col or not price_col:
        st.warning("CSV is missing required columns (date, crop/commodity, or price).")
        return

    # -------------------------
    # Preprocess
    # -------------------------
    df_market[date_col] = pd.to_datetime(df_market[date_col], errors='coerce')
    df_market = df_market.dropna(subset=[date_col, crop_col, price_col])

    # Normalize names
    df_market[crop_col] = df_market[crop_col].str.strip().str.lower()
    normalized_crops = [c.strip().lower() for c in top_crops]

    # Mapping ML crop names to CSV equivalents
    crop_name_map = {
        "rice": "paddy",
        "maize": "maize",   # change to "corn" if your CSV uses that
        "groundnut": "groundnut",
        "banana": "banana",
        "wheat": "wheat"
    }

    mapped_crops = [crop_name_map.get(c, c) for c in normalized_crops]

    # Filter only top crops
    df_top = df_market[df_market[crop_col].isin(mapped_crops)]

    if df_top.empty:
        st.warning("⚠️ No data found for the selected crops in the CSV.")
        st.write("Available Commodities:", df_market[crop_col].unique())
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

    # Latest prices table
    latest_prices = df_top.sort_values(date_col).groupby(crop_col).tail(1)
    st.subheader("Latest Prices")
    st.dataframe(latest_prices[[crop_col, price_col, date_col]].reset_index(drop=True))
