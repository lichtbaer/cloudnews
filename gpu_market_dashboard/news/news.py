"""
Module for fetching and tagging news for GPU cloud providers.
"""
import feedparser
from typing import List, Dict

import os
from llama_index.core.extractors import BaseExtractor, EntityExtractor, KeywordExtractor, QuestionsAnsweredExtractor, TitleExtractor, SummaryExtractor
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

NEWS_FEEDS = {
    'AWS': 'https://aws.amazon.com/blogs/aws/feed/',
    'Microsoft Azure': 'https://azure.microsoft.com/en-us/updates/feed/',
    'Google Cloud': 'https://cloud.google.com/blog/rss/',
    'CoreWeave': 'https://coreweave.com/blog/rss.xml',
    'Lambda Labs': 'https://lambdalabs.com/blog/rss',
    'OVHcloud': 'https://www.ovhcloud.com/en/news/feed/',
    # Add more feeds as available
}

def fetch_news(provider: str, max_items: int = 5) -> List[Dict]:
    url = NEWS_FEEDS.get(provider)
    if not url:
        return []
def extract_structured_news(text: str) -> Dict:
    """
    Extracts structured information from a news article using LlamaIndex and OpenAI LLM.
    Returns a dict with keys: summary, location, tags, actors.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in environment variables.")

    llm = OpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, api_base=OPENAI_API_BASE)
    extractors = [
        SummaryExtractor(),
        EntityExtractor(prediction_type="location"),
        KeywordExtractor(),
        EntityExtractor(prediction_type="person"),
        EntityExtractor(prediction_type="organization"),
    ]
    # Compose prompt for extraction
    prompt = f"""
    Extract the following structured data from the text:
    - Summary: Short summary of the article
    - Location: All locations, regions, or countries mentioned (empty if none)
    - Tags: List of relevant keywords
    - Actors: List of people, organizations, or companies mentioned
    Text: {text}
    Return as a JSON object with keys: summary, location, tags, actors.
    """
    response = llm.complete(prompt)
    # Try to parse response as JSON
    import json
    try:
        data = json.loads(response.text)
    except Exception:
        data = {"summary": "", "location": "", "tags": [], "actors": []}
    return data

    feed = feedparser.parse(url)
    news = []
    for entry in feed.entries[:max_items]:
        news.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', ''),
            'summary': entry.get('summary', '')
        })
    return news
def fetch_and_extract_news(provider: str, max_items: int = 5) -> List[Dict]:
    """
    Fetches news and extracts structured data for each article.
    """
    articles = fetch_news(provider, max_items) or []
    for article in articles:
        text = article.get('title', '') + '\n' + article.get('summary', '')
        structured = extract_structured_news(text)
        article.update(structured)
    return articles


def fetch_all_news(max_items: int = 5) -> Dict[str, List[Dict]]:
    return {provider: fetch_news(provider, max_items) for provider in NEWS_FEEDS}
def fetch_and_extract_all_news(max_items: int = 5) -> Dict[str, List[Dict]]:
    """
    Fetches and extracts structured data for all providers.
    """
    return {provider: fetch_and_extract_news(provider, max_items) for provider in NEWS_FEEDS}


def tag_news(news_item: Dict) -> List[str]:
    # Simple keyword-based tagging (can be improved with NLP)
    tags = []
    text = (news_item.get('title', '') + ' ' + news_item.get('summary', '')).lower()
    for keyword in ['gpu', 'ai', 'ml', 'cloud', 'price', 'launch', 'update', 'partnership']:
        if keyword in text:
            tags.append(keyword)
    return tags

