"""
Module for scraping and analyzing LinkedIn profiles.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re

def validate_linkedin_url(url: str) -> bool:
    """
    Validate LinkedIn URL format.
    Valid formats:
    - https://www.linkedin.com/in/username
    - https://linkedin.com/in/username
    - http://www.linkedin.com/in/username
    - http://linkedin.com/in/username
    """
    try:
        # Check basic URL structure
        if not url or not isinstance(url, str):
            return False
            
        # Parse URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc or not parsed.path:
            return False
            
        # Validate scheme
        if parsed.scheme not in ('http', 'https'):
            return False
            
        # Validate domain
        domain = parsed.netloc.lower()
        if not ('linkedin.com' in domain):
            return False
            
        # Validate path format
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2 or path_parts[0] != 'in':
            return False
            
        # Validate username format
        username = path_parts[1]
        if not re.match(r'^[\w\-]{3,100}$', username):
            return False
            
        return True
        
    except Exception:
        return False

def extract_profile_data(linkedin_url: str) -> Dict:
    """
    Extract relevant information from a LinkedIn profile URL.
    In a production environment, this would use LinkedIn's API or a proper scraping service.
    For now, we'll return mock data based on the profile URL.
    """
    # Validate URL format
    if not validate_linkedin_url(linkedin_url):
        raise ValueError("Invalid LinkedIn URL format. Expected format: https://www.linkedin.com/in/username")
    
    # Extract username from LinkedIn URL
    username = re.search(r'linkedin\.com/in/([\w\-]+)', linkedin_url)
    if not username:
        raise ValueError("Could not extract username from LinkedIn URL")
    
    username = username.group(1)
    
    try:
        # In a real implementation, we would:
        # 1. Use LinkedIn API with proper authentication
        # 2. Handle rate limiting
        # 3. Parse the actual profile data
        # For now, generate mock data based on username
        mock_data = {
            'name': username.replace('-', ' ').title(),
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
                    'description': 'Leading a technology startup focused on AI and machine learning applications.',
                    'duration': '2020 - Present'
                },
                {
                    'title': 'Product Manager',
                    'company': 'Tech Company',
                    'description': 'Led product development for enterprise software solutions.',
                    'duration': '2018 - 2020'
                }
            ],
            'summary': 'Experienced entrepreneur and business leader with a passion for technology and innovation.',
            'interests': [
                'Technology',
                'Startups',
                'Innovation',
                'Leadership',
                'Digital Transformation'
            ],
            'location': 'San Francisco Bay Area',
            'industry': 'Technology'
        }
        
        return mock_data
        
    except Exception as e:
        raise ValueError(f"Error processing LinkedIn profile: {str(e)}")

def analyze_profile_for_podcasts(profile_data: Dict, wants_to_be_featured: bool = False) -> Dict:
    """
    Analyze LinkedIn profile data to determine relevant podcast categories
    and potential speaking opportunities.
    
    Args:
        profile_data: Dictionary containing LinkedIn profile information
        wants_to_be_featured: Boolean indicating if the user wants to be featured on podcasts
    
    Returns:
        Dictionary containing analyzed profile data including keywords, categories,
        and potential speaking opportunities.
    
    Raises:
        ValueError: If profile_data is missing required fields or has invalid format
    """
    # Validate input data
    required_fields = ['skills', 'experience', 'interests']
    for field in required_fields:
        if field not in profile_data:
            raise ValueError(f"Missing required field: {field}")
    
    try:
        # Extract relevant keywords from profile
        keywords = set()
        
        # Process skills
        skills = profile_data.get('skills', [])
        if not isinstance(skills, list):
            raise ValueError("Skills must be a list")
        keywords.update(skills)
        
        # Process interests
        interests = profile_data.get('interests', [])
        if not isinstance(interests, list):
            raise ValueError("Interests must be a list")
        keywords.update(interests)
        
        # Extract keywords from experience
        experience = profile_data.get('experience', [])
        if not isinstance(experience, list):
            raise ValueError("Experience must be a list")
            
        # Define important terms for categorization
        domain_keywords = {
            'technology': [
                'ai', 'machine learning', 'blockchain', 'saas', 'cloud',
                'software', 'data science', 'cybersecurity', 'devops'
            ],
            'business': [
                'business', 'entrepreneurship', 'leadership', 'management',
                'strategy', 'operations', 'finance', 'marketing'
            ],
            'startups': [
                'startup', 'founder', 'entrepreneurship', 'venture capital',
                'seed funding', 'scaling', 'growth'
            ],
            'innovation': [
                'innovation', 'digital transformation', 'strategy',
                'disruption', 'emerging technologies', 'future'
            ]
        }
        
        # Process experience entries
        for exp in experience:
            if not isinstance(exp, dict):
                continue
                
            # Add job title keywords
            title = exp.get('title', '').lower()
            keywords.add(title)
            
            # Process description
            desc = exp.get('description', '').lower()
            
            # Extract domain-specific keywords
            for domain, terms in domain_keywords.items():
                for term in terms:
                    if term in desc or term in title:
                        keywords.add(term)
        
        # Clean and normalize keywords
        keywords = {k.strip().lower() for k in keywords if k.strip()}
        
        # Determine podcast categories based on keywords
        categories = {}
        for domain, terms in domain_keywords.items():
            relevance_score = sum(1 for term in terms if term in keywords)
            categories[domain] = relevance_score >= 2  # Require at least 2 matching terms
        
        # Analyze expertise level for featured opportunities
        featured_opportunities = []
        has_leadership = False
        total_years = 0
        
        if wants_to_be_featured:
            # Leadership analysis
            leadership_titles = {'founder', 'ceo', 'director', 'vp', 'head', 'chief'}
            has_leadership = any(
                any(title in exp.get('title', '').lower() for title in leadership_titles)
                for exp in experience
            )
            
            # Experience duration analysis
            total_years = sum(
                float(exp.get('duration', '0').split()[0])
                for exp in experience
                if exp.get('duration')
            )
            
            # Determine podcast opportunities based on experience
            if has_leadership and total_years >= 5:
                featured_opportunities.extend([
                    'Leadership Insights',
                    'Founder Stories',
                    'Executive Perspectives'
                ])
            
            # Domain-specific opportunities
            if categories['technology']:
                featured_opportunities.extend([
                    'Tech Talks',
                    'Innovation Spotlight',
                    'Future of Tech'
                ])
                
            if categories['startups']:
                featured_opportunities.extend([
                    'Startup Stories',
                    'Entrepreneur Spotlight',
                    'Venture Capital Insights'
                ])
            
            if categories['innovation']:
                featured_opportunities.extend([
                    'Innovation Leaders',
                    'Digital Transformation Stories',
                    'Change Makers'
                ])
        
        return {
            'keywords': sorted(list(keywords)),
            'categories': [cat for cat, relevant in categories.items() if relevant],
            'featured_opportunities': sorted(list(set(featured_opportunities))),
            'expertise_level': 'expert' if has_leadership and total_years >= 5 else 'intermediate'
        }
        
    except Exception as e:
        raise ValueError(f"Error analyzing profile: {str(e)}")
