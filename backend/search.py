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
    
    print(f"[DEBUG] Searching for: {query}")
    
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
        
        print(f"[DEBUG] Calling Wikipedia API with params: {params}")
        response = requests.get(WIKI_API, params=params, timeout=10)
        print(f"[DEBUG] Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[DEBUG] Response data keys: {data.keys()}")
            search_results = data.get('query', {}).get('search', [])
            print(f"[DEBUG] Found {len(search_results)} search results")
            
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
                print(f"[DEBUG] Added result: {title}")
        
        # If no results, try opensearch API as fallback
        if not results:
            print("[DEBUG] No results from search API, trying opensearch...")
            opensearch_params = {
                'action': 'opensearch',
                'search': query,
                'limit': limit,
                'namespace': 0,
                'format': 'json'
            }
            
            response = requests.get(WIKI_API, params=opensearch_params, timeout=10)
            print(f"[DEBUG] OpenSearch response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[DEBUG] OpenSearch data length: {len(data)}")
                titles = data[1] if len(data) > 1 else []
                descriptions = data[2] if len(data) > 2 else []
                urls = data[3] if len(data) > 3 else []
                print(f"[DEBUG] OpenSearch found {len(titles)} titles")
                
                for i, title in enumerate(titles):
                    snippet = descriptions[i] if i < len(descriptions) and descriptions[i] else 'Läs mer på Wikipedia'
                    url = urls[i] if i < len(urls) else f"https://sv.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    
                    results.append({
                        'title': title,
                        'snippet': clean_snippet(snippet),
                        'url': url
                    })
                    print(f"[DEBUG] Added opensearch result: {title}")
        
    except requests.RequestException as e:
        print(f"[ERROR] Wikipedia API error: {e}")
    except Exception as e:
        print(f"[ERROR] Search error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"[DEBUG] Returning {len(results)} results")
    return results

@router.get("/search")
def search(q: str = Query("", description="Fråga eller ämne på svenska")):
    """
    Search endpoint for Swedish Wikipedia.
    
    Returns relevant Wikipedia articles based on the query.
    """
    print(f"\n[DEBUG] === SEARCH REQUEST ===")
    print(f"[DEBUG] Query parameter: '{q}'")
    
    if not q or q.strip() == "":
        print("[DEBUG] Empty query, returning empty results")
        return JSONResponse({"results": [], "count": 0})
    
    # Perform Wikipedia search
    results = search_wikipedia(q.strip(), limit=10)
    
    response_data = {
        "results": results,
        "count": len(results),
        "query": q
    }
    
    print(f"[DEBUG] Response: {len(results)} results")
    print(f"[DEBUG] === END SEARCH REQUEST ===\n")
    
    return JSONResponse(response_data)
