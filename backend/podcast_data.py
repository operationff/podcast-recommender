"""
Module for scraping and managing podcast data.
"""
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from typing import List, Dict

# Cache file for storing scraped podcast data
CACHE_FILE = 'podcasts.json'

def get_sample_podcasts() -> List[Dict]:
    """Return sample podcast data for testing and fallback."""
    return [
        {
            'title': 'StartUp',
            'description': 'A series about what it\'s really like to start a business.',
            'image': 'https://example.com/startup.jpg',
            'website': 'https://gimletmedia.com/startup',
            'categories': ['Business', 'Entrepreneurship', 'Startups'],
            'source': 'Sample'
        },
        {
            'title': 'How I Built This',
            'description': 'Guy Raz dives into the stories behind some of the world\'s best known companies.',
            'image': 'https://example.com/hibt.jpg',
            'website': 'https://npr.org/hibt',
            'categories': ['Business', 'Entrepreneurship', 'Innovation'],
            'source': 'Sample'
        },
        {
            'title': 'Masters of Scale',
            'description': 'Reid Hoffman shows how companies grow from zero to a gazillion.',
            'image': 'https://example.com/scale.jpg',
            'website': 'https://mastersofscale.com',
            'categories': ['Startups', 'Business', 'Venture Capital'],
            'source': 'Sample'
        },
        {
            'title': 'The Pitch',
            'description': 'Where real entrepreneurs pitch to real investors.',
            'image': 'https://example.com/pitch.jpg',
            'website': 'https://gimletmedia.com/the-pitch',
            'categories': ['Startups', 'Venture Capital', 'Business'],
            'source': 'Sample'
        },
        {
            'title': 'Business Wars',
            'description': 'Inside the most dramatic business battles in history.',
            'image': 'https://example.com/bw.jpg',
            'website': 'https://wondery.com/business-wars',
            'categories': ['Business', 'Innovation', 'Top Rated'],
            'source': 'Sample'
        }
    ]

def scrape_podcasts() -> List[Dict]:
    """
    Scrape podcast data from multiple sources and return a list of podcasts.
    Each podcast has: title, description, image_url, website, categories
    """
    podcasts = []
    
    # Try to scrape from various sources
    try:
        # Scrape from iTunes/Apple Podcasts business category
        response = requests.get('https://itunes.apple.com/us/rss/toppodcasts/limit=100/genre=1321/json')
        if response.status_code == 200:
            data = response.json()
            for entry in data.get('feed', {}).get('entry', []):
                podcasts.append({
                    'title': entry.get('title', {}).get('label', ''),
                    'description': entry.get('summary', {}).get('label', ''),
                    'image': entry.get('im:image', [{}])[0].get('label', ''),
                    'website': entry.get('link', {}).get('attributes', {}).get('href', ''),
                    'categories': ['Business', 'Top Rated'],
                    'source': 'iTunes'
                })
    except Exception as e:
        print(f"Error scraping iTunes: {str(e)}")

    # If we couldn't get any podcasts, use sample data
    if not podcasts:
        print("Using sample podcast data as fallback")
        podcasts = get_sample_podcasts()

    return podcasts

def load_or_scrape_podcasts() -> List[Dict]:
    """
    Load podcasts from cache file if it exists and is recent,
    otherwise scrape new data.
    """
    if os.path.exists(CACHE_FILE):
        # Check if cache is less than 24 hours old
        if os.path.getmtime(CACHE_FILE) > time.time() - 86400:
            try:
                with open(CACHE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading cache file: {str(e)}")
    
    # Scrape new data
    podcasts = scrape_podcasts()
    
    # Save to cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(podcasts, f)
    
    return podcasts

def search_podcasts(query: str, offset: int = 0) -> List[Dict]:
    """
    Search podcasts based on query string.
    """
    podcasts = load_or_scrape_podcasts()
    query = query.lower()
    
    # Filter podcasts based on query
    matching_podcasts = []
    for podcast in podcasts:
        if (query in podcast['title'].lower() or 
            query in podcast['description'].lower() or
            any(query in category.lower() for category in podcast['categories'])):
            matching_podcasts.append(podcast)
    
    # Handle pagination
    start = offset
    end = start + 10
    return matching_podcasts[start:end]

def get_all_podcasts() -> List[Dict]:
    """
    Get all available podcasts.
    """
    return load_or_scrape_podcasts()
