import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import pandas as pd
from gpu_market_dashboard.news.news import fetch_and_extract_all_news

def main():
    st.title("Strukturierte News-Extraktion (LLM-basiert)")
    st.info("Extrahiert strukturierte Informationen aus aktuellen News der Anbieter mittels LlamaIndex und OpenAI.")
    news_data = fetch_and_extract_all_news(max_items=10)
    all_articles = []
    for provider, articles in news_data.items():
        for article in articles:
            article['provider'] = provider
            all_articles.append(article)
    df = pd.DataFrame(all_articles)
    if df.empty or 'provider' not in df.columns:
        st.warning("Keine strukturierten News gefunden.")
        st.stop()
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
    filtered_df = df[
        df['provider'].isin(provider_filter)
        & (df['tags'].apply(lambda tags: any(tag in tags for tag in tag_filter) if tag_filter else True))
        & (df['location'].apply(lambda loc: loc in location_filter if location_filter else True))
        & (df['actors'].apply(lambda actors: any(actor in actors for actor in actor_filter) if actor_filter else True))
    ]
    st.dataframe(filtered_df, use_container_width=True)
    for _, row in filtered_df.iterrows():
        st.subheader(row['title'])
        st.markdown(f"**Anbieter:** {row['provider']}")
        st.markdown(f"**Veröffentlicht:** {row['published']}")
        st.markdown(f"**Zusammenfassung:** {row['summary']}")
        st.markdown(f"**Tags:** {', '.join(row['tags']) if isinstance(row['tags'], list) else row['tags']}")
        st.markdown(f"**Orte:** {row['location']}")
        st.markdown(f"**Akteure:** {', '.join(row['actors']) if isinstance(row['actors'], list) else row['actors']}")
        st.markdown(f"[Link zur News]({row['link']})")
        st.markdown("---")

if __name__ == "__main__":
    main()
