from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import requests
import re
from typing import List, Dict

router = APIRouter()

# Swedish Wikipedia API endpoint
WIKI_API = "https://sv.wikipedia.org/w/api.php"

def clean_html(text: str) -> str:
    """Remove HTML tags from text."""
    clean = re.sub(r'<[^>]+>', '', text)
    return clean.strip()

def clean_snippet(text: str, max_length: int = 200) -> str:
    """Clean and truncate text for snippet display."""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate to max_length
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '…'
    
    return text

def search_wikipedia(query: str, limit: int = 10) -> List[Dict[str, str]]:
    """
    Search Swedish Wikipedia using MediaWiki API.
    
    Args:
        query: Search query in Swedish
        limit: Maximum number of results to return
    
    Returns:
        List of dictionaries containing title, snippet, and url
    """
    results = []
    
    try:
        # First, try to get page extracts using the search API
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': limit,
            'srprop': 'snippet',
            'utf8': 1
        }
        
        response = requests.get(WIKI_API, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            search_results = data.get('query', {}).get('search', [])
            
            for result in search_results:
                title = result.get('title', '')
                snippet = clean_html(result.get('snippet', 'Läs mer på Wikipedia'))
                
                # Construct Wikipedia URL
                url = f"https://sv.wikipedia.org/wiki/{title.replace(' ', '_')}"
                
                results.append({
                    'title': title,
                    'snippet': clean_snippet(snippet),
                    'url': url
                })
        
        # If no results, try opensearch API as fallback
        if not results:
            opensearch_params = {
                'action': 'opensearch',
                'search': query,
                'limit': limit,
                'namespace': 0,
                'format': 'json'
            }
            
            response = requests.get(WIKI_API, params=opensearch_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                titles = data[1] if len(data) > 1 else []
                descriptions = data[2] if len(data) > 2 else []
                urls = data[3] if len(data) > 3 else []
                
                for i, title in enumerate(titles):
                    snippet = descriptions[i] if i < len(descriptions) and descriptions[i] else 'Läs mer på Wikipedia'
                    url = urls[i] if i < len(urls) else f"https://sv.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    
                    results.append({
                        'title': title,
                        'snippet': clean_snippet(snippet),
                        'url': url
                    })
        
    except requests.RequestException as e:
        print(f"Wikipedia API error: {e}")
    except Exception as e:
        print(f"Search error: {e}")
    
    return results

@router.get("/search")
def search(q: str = Query("", description="Fråga eller ämne på svenska")):
    """
    Search endpoint for Swedish Wikipedia.
    
    Returns relevant Wikipedia articles based on the query.
    """
    if not q or q.strip() == "":
        return JSONResponse({"results": [], "count": 0})
    
    # Perform Wikipedia search
    results = search_wikipedia(q.strip(), limit=10)
    
    return JSONResponse({
        "results": results,
        "count": len(results),
        "query": q
    })
