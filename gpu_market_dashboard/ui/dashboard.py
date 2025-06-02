import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
st.set_page_config(page_title="GPU Cloud Market Dashboard", layout="wide")
from gpu_market_dashboard.news.news import fetch_and_extract_all_news

"""
Streamlit dashboard for GPU Cloud Market Monitoring.
"""
import pandas as pd
from gpu_market_dashboard.data.pricing import get_all_prices
from gpu_market_dashboard.news.news import fetch_all_news, tag_news

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
# --- Neue Seite: Strukturierte News-Extraktion ---
def show_dashboard_page():
    st.title("GPU Cloud Market Monitoring Dashboard")
    st.header("GPU Preisvergleich (USD pro Stunde)")
    from gpu_market_dashboard.data.pricing import get_all_prices
    prices_df = get_all_prices()
    st.dataframe(prices_df, use_container_width=True)
    st.header("Aktuelle Marktnews der Anbieter")
    from gpu_market_dashboard.news.news import fetch_all_news, tag_news
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

def show_structured_news_page():
    st.title("Strukturierte News-Extraktion (LLM-basiert)")
    st.info("Extrahiert strukturierte Informationen aus aktuellen News der Anbieter mittels LlamaIndex und OpenAI.")
    # Filter: Anbieter, Zeitraum, Tags, Orte, Akteure
    news_data = fetch_and_extract_all_news(max_items=10)
    all_articles = []
    for provider, articles in news_data.items():
        for article in articles:
            article['provider'] = provider
            all_articles.append(article)
    df = pd.DataFrame(all_articles)
    # Filter-Widgets
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        provider_filter = st.multiselect("Anbieter filtern", options=df['provider'].unique(), default=list(df['provider'].unique()))
    with col2:
        tag_options = sorted({tag for tags in df['tags'] if isinstance(tags, list) for tag in tags})
        tag_filter = st.multiselect("Tags filtern", options=tag_options)
    with col3:
        location_options = sorted({loc for loc in df['location'] if loc})
        location_filter = st.multiselect("Orte filtern", options=location_options)
    with col4:
        actor_options = sorted({actor for actors in df['actors'] if isinstance(actors, list) for actor in actors})
        actor_filter = st.multiselect("Akteure filtern", options=actor_options)
    # Filter anwenden
    filtered = df[
        df['provider'].isin(provider_filter)
    ]
    if tag_filter:
        filtered = filtered[filtered['tags'].apply(lambda tags: any(tag in tags for tag in tag_filter) if isinstance(tags, list) else False)]
    if location_filter:
        filtered = filtered[filtered['location'].apply(lambda loc: loc in location_filter if loc else False)]
    if actor_filter:
        filtered = filtered[filtered['actors'].apply(lambda actors: any(actor in actors for actor in actor_filter) if isinstance(actors, list) else False)]
    # Visualisierung: Tabelle
    st.dataframe(filtered[['provider', 'title', 'summary', 'location', 'tags', 'actors', 'published', 'link']], use_container_width=True)
    # Visualisierung: Tag-Häufigkeit
    st.subheader("Tag-Häufigkeit")
    import collections
    tag_counter = collections.Counter(tag for tags in filtered['tags'] if isinstance(tags, list) for tag in tags)
    if tag_counter:
        st.bar_chart(pd.DataFrame.from_dict(tag_counter, orient='index', columns=['Häufigkeit']))
    # Visualisierung: Orte
    st.subheader("Orte (Location) Verteilung")
    loc_counter = collections.Counter(loc for loc in filtered['location'] if loc)
    if loc_counter:
        st.bar_chart(pd.DataFrame.from_dict(loc_counter, orient='index', columns=['Häufigkeit']))
    # Visualisierung: Akteure
    st.subheader("Akteure Verteilung")
    actor_counter = collections.Counter(actor for actors in filtered['actors'] if isinstance(actors, list) for actor in actors)
    if actor_counter:
        st.bar_chart(pd.DataFrame.from_dict(actor_counter, orient='index', columns=['Häufigkeit']))
    # Einzelansicht
    st.subheader("Artikel-Details")
    for idx, row in filtered.iterrows():
        with st.expander(f"{row['provider']}: {row['title']}"):
            st.markdown(f"**Veröffentlicht:** {row['published']}")
            st.markdown(f"**Zusammenfassung:** {row['summary']}")
            st.markdown(f"**Orte:** {row['location']}")
            st.markdown(f"**Tags:** {', '.join(row['tags']) if isinstance(row['tags'], list) else row['tags']}")
            st.markdown(f"**Akteure:** {', '.join(row['actors']) if isinstance(row['actors'], list) else row['actors']}")
            st.markdown(f"[Zum Artikel]({row['link']})")
# --- Seiten-Navigation ---
page = st.sidebar.radio("Seite wählen", ["Dashboard", "Strukturierte News-Extraktion"])
if page == "Dashboard":
    show_dashboard_page()
if page == "Strukturierte News-Extraktion":
    show_structured_news_page()

        st.markdown("---")

