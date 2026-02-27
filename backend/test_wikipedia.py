#!/usr/bin/env python3
"""
Test script for Wikipedia API integration.
Run this to verify the Wikipedia search functionality works correctly.
"""

import wikipediaapi
import requests

def test_wikipedia_api():
    """Test Swedish Wikipedia API access."""
    print("Testing Swedish Wikipedia API Integration")
    print("="*50)
    print()
    
    # Initialize Swedish Wikipedia
    wiki = wikipediaapi.Wikipedia(
        language='sv',
        user_agent='Upsum/0.1 (https://oscyra.solutions/upsum; test)'
    )
    
    # Test 1: Direct page access
    print("Test 1: Direct page access (Stockholm)")
    page = wiki.page('Stockholm')
    
    if page.exists():
        print(f"  ✓ Page found: {page.title}")
        print(f"  ✓ Summary (first 100 chars): {page.summary[:100]}...")
        print(f"  ✓ URL: {page.fullurl}")
    else:
        print("  ✗ Page not found")
    
    print()
    
    # Test 2: Search API
    print("Test 2: Search API (Sverige)")
    search_url = "https://sv.wikipedia.org/w/api.php"
    params = {
        'action': 'opensearch',
        'search': 'Sverige',
        'limit': 5,
        'namespace': 0,
        'format': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            titles = data[1] if len(data) > 1 else []
            print(f"  ✓ Found {len(titles)} results:")
            for i, title in enumerate(titles[:3], 1):
                print(f"    {i}. {title}")
        else:
            print(f"  ✗ API returned status {response.status_code}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print()
    
    # Test 3: Test various queries
    print("Test 3: Multiple search queries")
    test_queries = [
        'Gustav Vasa',
        'Minecraft',
        'Python programmeringsspråk',
        'Stockholm stad'
    ]
    
    for query in test_queries:
        try:
            response = requests.get(search_url, 
                                   params={**params, 'search': query, 'limit': 3}, 
                                   timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = len(data[1]) if len(data) > 1 else 0
                print(f"  '{query}': {count} results")
            else:
                print(f"  '{query}': API error")
        except Exception as e:
            print(f"  '{query}': {str(e)}")
    
    print()
    print("="*50)
    print("Testing complete!")
    print()
    print("If all tests passed, Wikipedia integration is working.")
    print("You can now run 'uvicorn main:app --reload' to start the backend.")

if __name__ == "__main__":
    test_wikipedia_api()
