import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
st.set_page_config(page_title="GPU Cloud Market Dashboard", layout="wide")
import pandas as pd
from gpu_market_dashboard.data.pricing import get_all_prices
from gpu_market_dashboard.news.news import fetch_all_news, tag_news

def main():
    st.title("GPU Cloud Market Monitoring Dashboard")
    st.header("GPU Preisvergleich (USD pro Stunde)")
    prices_df = get_all_prices()
    st.dataframe(prices_df, use_container_width=True)
    st.header("Aktuelle Marktnews der Anbieter")
    news_data = fetch_all_news(max_items=5)
    for provider, news_list in news_data.items():
        if not news_list:
            continue
        st.subheader(provider)
        for item in news_list:
            tags = tag_news(item)
            st.markdown(f"**[{item['title']}]({item['link']})**  ")
            st.markdown(f"*{item['published']}*  ")
            st.markdown(item['summary'])
            if tags:
                st.markdown(f"Tags: {', '.join(tags)}")
            st.markdown("---")

if __name__ == "__main__":
    main()
