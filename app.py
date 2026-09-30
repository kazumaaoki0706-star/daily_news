import datetime
import streamlit as st
import feedparser
import requests
import pandas as pd
import jpholiday

# Page configuration
st.set_page_config(
    page_title="General Information Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# Sidebar: Japanese Public Holidays
# ==========================================
with st.sidebar:
    st.header("📅 Upcoming Holidays in Japan")
    
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    
    # Generate holidays for the current year and the next year to ensure full-year visibility
    holidays_data = []
    for year in [current_year, current_year + 1]:
        year_holidays = jpholiday.year_holidays(year)
        for h_date, h_name in year_holidays:
            # Filter for current month onwards in the current year, or any month in the next year
            if (h_date.year == current_year and h_date.month >= current_month) or (h_date.year > current_year):
                holidays_data.append({
                    "Date": h_date.strftime("%Y-%m-%d"),
                    "Holiday": h_name
                })
    
    if holidays_data:
        df_holidays = pd.DataFrame(holidays_data)
        st.dataframe(df_holidays, hide_index=True, use_container_width=True)
    else:
        st.info("No upcoming holidays found.")

# Main Dashboard Title
st.title("📊 General Information Dashboard")
st.markdown("---")

# Create 3-column layout
col1, col2, col3 = st.columns(3)

# ==========================================
# 1. Nagasaki Weather & US News (col1)
# ==========================================
with col1:
    st.header("🌤️ Nagasaki Weather")
    
    # Open-Meteo API (Nagasaki City: Lat 32.75, Lon 129.87)
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=32.75&longitude=129.87&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=Asia%2FTokyo"
    
    weather_code_map = {
        0: "☀ Clear sky",
        1: "🌤️ Mainly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast",
        45: "🌫️ Fog", 48: "🌫️ Depositing rime fog",
        51: "🌧 Drizzle", 53: "🌧 Moderate drizzle", 55: "🌧️ Dense drizzle",
        61: "☔ Slight rain", 63: "☔ Moderate rain", 65: "☔ Heavy rain",
        80: "🌦️ Slight rain showers", 81: "🌦️ Moderate rain showers", 82: "⛈️ Violent rain showers"
    }

    try:
        response = requests.get(weather_url, timeout=5)
        data = response.json()
        
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        codes = daily.get("weathercode", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])

        weather_list = []
        for i in range(min(5, len(dates))):
            weather_text = weather_code_map.get(codes[i], "❓ Unknown")
            weather_list.append({
                "Date": dates[i],
                "Condition": weather_text,
                "Max (°C)": max_temps[i],
                "Min (°C)": min_temps[i]
            })

        df_weather = pd.DataFrame(weather_list)
        st.dataframe(df_weather, hide_index=True, use_container_width=True)

    except Exception as e:
        st.error(f"Failed to fetch weather data: {e}")

    # --- US Latest News below weather ---
    st.markdown("---")
    st.header("🇺🇸 US Latest News")
    
    # Google News RSS (United States Search in English)
    us_rss_url = "https://news.google.com/rss/search?q=United+States&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed_us = feedparser.parse(us_rss_url)
        entries_us = feed_us.entries[:5]  # Top 5 items

        if not entries_us:
            st.info("No news articles found.")
        else:
            for entry in entries_us:
                st.markdown(f"**[{entry.title}]({entry.link})**")
                published = getattr(entry, "published", "Unknown date")
                st.caption(f"📅 {published}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Failed to fetch US news: {e}")

# ==========================================
# 2. Nagasaki News (col2)
# ==========================================
with col2:
    st.header("📰 Nagasaki News")
    
    # Google News RSS (Topic: Nagasaki in English)
    nagasaki_rss_url = "https://news.google.com/rss/search?q=Nagasaki&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(nagasaki_rss_url)
        entries = feed.entries[:7]

        if not entries:
            st.info("No news articles found.")
        else:
            for entry in entries:
                st.markdown(f"**[{entry.title}]({entry.link})**")
                published = getattr(entry, "published", "Unknown date")
                st.caption(f"📅 {published}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Failed to fetch Nagasaki news: {e}")

# ==========================================
# 3. Facility Management News (col3)
# ==========================================
with col3:
    st.header("🔧 Facility Management News")
    
    # Google News RSS (Topic: Facility Management OR Building Maintenance in English)
    facility_rss_url = "https://news.google.com/rss/search?q=%22Facility+Management%22+OR+%22Building+Maintenance%22&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(facility_rss_url)
        entries = feed.entries[:7]

        if not entries:
            st.info("No news articles found.")
        else:
            for entry in entries:
                st.markdown(f"**[{entry.title}]({entry.link})**")
                published = getattr(entry, "published", "Unknown date")
                st.caption(f"📅 {published}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Failed to fetch Facility Management news: {e}")