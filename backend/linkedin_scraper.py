"""
Module for scraping and analyzing LinkedIn profiles.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re

def extract_profile_data(linkedin_url: str) -> Dict:
    """
    Extract relevant information from a LinkedIn profile URL.
    In a production environment, this would use LinkedIn's API or a proper scraping service.
    For now, we'll return mock data based on the profile URL.
    """
    # Extract username from LinkedIn URL
    username = re.search(r'linkedin\.com/in/([\w\-]+)', linkedin_url)
    if not username:
        raise ValueError("Invalid LinkedIn URL format")
    
    username = username.group(1)
    
    # In a real implementation, we would:
    # 1. Use LinkedIn API or a scraping service
    # 2. Handle rate limiting and authentication
    # 3. Parse the actual profile data
    # For now, return mock data
    mock_data = {
        'skills': [
            'Business Development',
            'Entrepreneurship',
            'Strategic Planning',
            'Team Leadership',
            'Product Management',
            'Digital Marketing'
        ],
        'experience': [
            {
                'title': 'Founder & CEO',
                'company': 'Tech Startup',
                'description': 'Leading a technology startup focused on AI and machine learning applications.'
            },
            {
                'title': 'Product Manager',
                'company': 'Tech Company',
                'description': 'Led product development for enterprise software solutions.'
            }
        ],
        'summary': 'Experienced entrepreneur and business leader with a passion for technology and innovation.',
        'interests': [
            'Technology',
            'Startups',
            'Innovation',
            'Leadership',
            'Digital Transformation'
        ]
    }
    
    return mock_data

def analyze_profile_for_podcasts(profile_data: Dict, wants_to_be_featured: bool) -> Dict:
    """
    Analyze LinkedIn profile data to determine relevant podcast categories
    and potential speaking opportunities.
    """
    # Extract relevant keywords from profile
    keywords = set()
    
    # Add skills
    keywords.update(profile_data.get('skills', []))
    
    # Add interests
    keywords.update(profile_data.get('interests', []))
    
    # Extract keywords from experience
    for exp in profile_data.get('experience', []):
        keywords.add(exp.get('title', ''))
        desc = exp.get('description', '').lower()
        # Extract key tech and business terms
        tech_terms = ['ai', 'machine learning', 'blockchain', 'saas', 'cloud']
        business_terms = ['startup', 'leadership', 'strategy', 'innovation']
        
        for term in tech_terms + business_terms:
            if term in desc.lower():
                keywords.add(term)
    
    # Determine podcast categories based on keywords
    categories = {
        'technology': any(k.lower() in ['technology', 'ai', 'machine learning', 'digital'] for k in keywords),
        'business': any(k.lower() in ['business', 'entrepreneurship', 'leadership'] for k in keywords),
        'startups': any(k.lower() in ['startup', 'founder', 'entrepreneurship'] for k in keywords),
        'innovation': any(k.lower() in ['innovation', 'digital transformation', 'strategy'] for k in keywords)
    }
    
    # If they want to be featured, analyze their expertise level
    featured_opportunities = []
    if wants_to_be_featured:
        # Check for leadership experience
        has_leadership = any('founder' in exp.get('title', '').lower() or 
                           'ceo' in exp.get('title', '').lower() or 
                           'director' in exp.get('title', '').lower() 
                           for exp in profile_data.get('experience', []))
        
        # Determine relevant podcast types for featuring
        if has_leadership:
            featured_opportunities.extend([
                'Leadership Insights',
                'Founder Stories',
                'CEO Interviews'
            ])
        
        if categories['technology']:
            featured_opportunities.extend([
                'Tech Talks',
                'Innovation Spotlight'
            ])
            
        if categories['startups']:
            featured_opportunities.extend([
                'Startup Stories',
                'Entrepreneur Spotlight'
            ])
    
    return {
        'keywords': list(keywords),
        'categories': [cat for cat, relevant in categories.items() if relevant],
        'featured_opportunities': featured_opportunities
    }
