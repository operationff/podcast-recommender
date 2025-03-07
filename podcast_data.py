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
    sources = [
        {
            'name': 'iTunes',
            'url': 'https://itunes.apple.com/us/rss/toppodcasts/limit=100/genre=1321/json',
            'categories': ['Business', 'Top Rated']
        },
        {
            'name': 'Spotify',
            'url': 'https://api.spotify.com/v1/shows/categories/business',
            'categories': ['Business', 'Featured']
        }
    ]
    
    for source in sources:
        try:
            # Add request headers and timeout
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; PodcastRecommender/1.0)',
                'Accept': 'application/json'
            }
            response = requests.get(
                source['url'],
                headers=headers,
                timeout=10  # 10 seconds timeout
            )
            
            # Check response status
            response.raise_for_status()
            
            # Parse data based on source
            if source['name'] == 'iTunes':
                data = response.json()
                for entry in data.get('feed', {}).get('entry', []):
                    podcasts.append({
                        'title': entry.get('title', {}).get('label', ''),
                        'description': entry.get('summary', {}).get('label', ''),
                        'image': entry.get('im:image', [{}])[0].get('label', ''),
                        'website': entry.get('link', {}).get('attributes', {}).get('href', ''),
                        'categories': source['categories'],
                        'source': source['name'],
                        'rating': float(entry.get('im:rating', {}).get('label', 0)),
                        'release_date': entry.get('im:releaseDate', {}).get('label', '')
                    })
            
            elif source['name'] == 'Spotify':
                # Implementation for Spotify API would go here
                # Requires OAuth token handling
                pass
                
        except requests.exceptions.RequestException as e:
            print(f"Error scraping {source['name']}: {str(e)}")
        except ValueError as e:
            print(f"Error parsing {source['name']} data: {str(e)}")
        except Exception as e:
            print(f"Unexpected error scraping {source['name']}: {str(e)}")
    
    # If we couldn't get any podcasts, use sample data
    if not podcasts:
        print("Using sample podcast data as fallback")
        podcasts = get_sample_podcasts()
    
    # Sort podcasts by rating
    podcasts.sort(key=lambda x: x.get('rating', 0), reverse=True)
    
    return podcasts

def load_or_scrape_podcasts() -> List[Dict]:
    """
    Load podcasts from cache file if it exists and is recent,
    otherwise scrape new data.
    """
    try:
        if os.path.exists(CACHE_FILE):
            # Check if cache is less than 24 hours old
            cache_age = time.time() - os.path.getmtime(CACHE_FILE)
            if cache_age < 86400:  # 24 hours
                try:
                    with open(CACHE_FILE, 'r') as f:
                        cached_data = json.load(f)
                        
                    # Validate cached data structure
                    if isinstance(cached_data, list) and all(
                        isinstance(p, dict) and
                        'title' in p and
                        'description' in p and
                        'categories' in p
                        for p in cached_data
                    ):
                        print(f"Using cached podcast data ({len(cached_data)} podcasts)")
                        return cached_data
                    else:
                        print("Invalid cache data structure, refreshing...")
                except json.JSONDecodeError:
                    print("Invalid JSON in cache file, refreshing...")
                except Exception as e:
                    print(f"Error reading cache: {str(e)}, refreshing...")
            else:
                print(f"Cache is {cache_age/3600:.1f} hours old, refreshing...")
    except Exception as e:
        print(f"Error checking cache: {str(e)}")
    
    # Scrape new data
    try:
        podcasts = scrape_podcasts()
        
        # Save to cache
        cache_dir = os.path.dirname(CACHE_FILE)
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            
        with open(CACHE_FILE, 'w') as f:
            json.dump(podcasts, f, indent=2)
            
        print(f"Successfully cached {len(podcasts)} podcasts")
        return podcasts
        
    except Exception as e:
        print(f"Error refreshing podcast data: {str(e)}")
        # If all else fails, return sample data
        return get_sample_podcasts()

def search_podcasts(query: str, offset: int = 0, limit: int = 10, categories: List[str] = None) -> Dict:
    """
    Search podcasts based on query string and optional filters.
    Returns dict with total count and paginated results.
    """
    try:
        podcasts = load_or_scrape_podcasts()
        query = query.lower().strip()
        
        # Filter podcasts based on query and categories
        matching_podcasts = []
        for podcast in podcasts:
            # Score the match
            score = 0
            title_lower = podcast['title'].lower()
            desc_lower = podcast['description'].lower()
            
            # Title match (highest weight)
            if query in title_lower:
                score += 3
                if title_lower.startswith(query):
                    score += 2
            
            # Description match
            if query in desc_lower:
                score += 1
            
            # Category match
            if categories:
                podcast_categories = [c.lower() for c in podcast['categories']]
                if any(c.lower() in podcast_categories for c in categories):
                    score += 2
            
            # Add to results if there's a match
            if score > 0:
                matching_podcasts.append((score, podcast))
        
        # Sort by score
        matching_podcasts.sort(key=lambda x: (-x[0], x[1]['title']))
        matching_podcasts = [p[1] for p in matching_podcasts]
        
        # Handle pagination
        total_count = len(matching_podcasts)
        start = min(offset, total_count)
        end = min(start + limit, total_count)
        
        return {
            'total': total_count,
            'offset': offset,
            'limit': limit,
            'results': matching_podcasts[start:end]
        }
        
    except Exception as e:
        print(f"Error searching podcasts: {str(e)}")
        return {
            'total': 0,
            'offset': offset,
            'limit': limit,
            'results': []
        }

def get_all_podcasts() -> List[Dict]:
    """
    Get all available podcasts.
    """
    return load_or_scrape_podcasts()
