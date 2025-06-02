"""
Module for fetching and normalizing GPU cloud pricing data from major providers.
"""
import requests
import pandas as pd
from typing import List, Dict
from bs4 import BeautifulSoup
import re

# NOTE: Most provider pricing pages are JavaScript-rendered. For robust, real-time data, use official APIs or downloadable CSV/JSON endpoints if available. Static values are used as fallback. See each fetch_xxx_prices() docstring for details.


PROVIDERS = [
    'aws', 'azure', 'gcp', 'coreweave', 'lambdalabs', 'northerndata', 'ovhcloud', 'hyperstack'
]

GPU_MODELS = ['H100 (80GB)', 'A100 (80GB)', 'V100 (16GB)']


def fetch_aws_prices() -> Dict:
    """
    Fetch AWS EC2 on-demand pricing for GPU instances (H100, A100, V100). Pricing page is JavaScript-rendered; fallback to static values.
    TODO: Use AWS Pricing API for robust, real-time data.
    """
    return {'H100 (80GB)': 98.32, 'A100 (80GB)': 32.77, 'V100 (16GB)': 3.06, 'region': 'Global'}

def fetch_azure_prices() -> Dict:
    """
    Fetch Azure GPU VM prices. Azure pricing page is JavaScript-rendered; fallback to static values.
    TODO: Use Azure Retail Prices API for real-time data.
    """
    return {'H100 (80GB)': 6.98, 'A100 (80GB)': 3.67, 'V100 (16GB)': 3.06, 'region': 'Global'}

def fetch_gcp_prices() -> Dict:
    """
    Fetch Google Cloud GPU prices. Pricing page is JavaScript-rendered; fallback to static values.
    TODO: Use Google Cloud Billing Catalog API for real-time data.
    """
    return {'H100 (80GB)': 11.05, 'A100 (80GB)': 6.24, 'V100 (16GB)': 2.48, 'region': 'Global'}

def fetch_coreweave_prices() -> Dict:
    """
    Fetch CoreWeave GPU prices. Pricing page is JavaScript-rendered; fallback to static values.
    TODO: Use CoreWeave API or headless browser for real-time data.
    """
    return {'H100 (80GB)': 4.25, 'A100 (80GB)': 2.25, 'V100 (16GB)': None, 'region': 'US/Global'}

def fetch_lambdalabs_prices() -> Dict:
    """
    Fetch Lambda Labs GPU prices. Pricing page is JavaScript-rendered; fallback to static values.
    TODO: Use Lambda Labs API or headless browser for real-time data.
    """
    return {'H100 (80GB)': 2.49, 'A100 (80GB)': 1.29, 'V100 (16GB)': 0.55, 'region': 'US'}

def fetch_northerndata_prices() -> Dict:
    """
    Fetch Northern Data (Taiga) GPU prices. No public pricing available; returns None.
    TODO: Add scraping/API if public pricing becomes available.
    """
    return {'H100 (80GB)': None, 'A100 (80GB)': None, 'V100 (16GB)': None, 'region': 'Europe'}

def fetch_ovhcloud_prices() -> Dict:
    """
    Fetch OVHcloud GPU prices. Pricing page is JavaScript-rendered; fallback to static values.
    TODO: Use OVHcloud API or headless browser for real-time data.
    """
    return {'H100 (80GB)': 3.39, 'A100 (80GB)': 3.35, 'V100 (16GB)': 2.19, 'region': 'Europe'}

def fetch_hyperstack_prices() -> Dict:
    """
    Fetch Hyperstack GPU prices. Pricing page is JavaScript-rendered; fallback to static values.
    TODO: Use Hyperstack API or headless browser for real-time data.
    """
    return {'H100 (80GB)': 1.90, 'A100 (80GB)': 1.35, 'V100 (16GB)': None, 'region': 'Global'}

def get_all_prices() -> pd.DataFrame:
    data = []
    fetchers = [
        fetch_aws_prices, fetch_azure_prices, fetch_gcp_prices,
        fetch_coreweave_prices, fetch_lambdalabs_prices, fetch_northerndata_prices,
        fetch_ovhcloud_prices, fetch_hyperstack_prices
    ]
    names = [
        'AWS', 'Microsoft Azure', 'Google Cloud', 'CoreWeave',
        'Lambda Labs', 'Northern Data (Taiga)', 'OVHcloud', 'Hyperstack'
    ]
    focus = [
        'Hyperscaler', 'Hyperscaler', 'Hyperscaler', 'GPU Specialized',
        'AI/ML Specialized', 'European AI Cloud', 'European Cloud', 'Multi-Cloud'
    ]
    for i, fetch in enumerate(fetchers):
        row = fetch()
        row['Anbieter'] = names[i]
        row['Fokus'] = focus[i]
        data.append(row)
    df = pd.DataFrame(data)
    cols = ['Anbieter'] + GPU_MODELS + ['region', 'Fokus']
    return df[cols]

