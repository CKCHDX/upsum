from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import wikipediaapi
import re
from typing import List, Dict

router = APIRouter()

# Initialize Swedish Wikipedia API
wiki = wikipediaapi.Wikipedia(
    language='sv',
    user_agent='Upsum/0.1 (https://oscyra.solutions/upsum; alex@oscyra.solutions)'
)

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
    Search Swedish Wikipedia and return formatted results.
    
    Args:
        query: Search query in Swedish
        limit: Maximum number of results to return
    
    Returns:
        List of dictionaries containing title, snippet, and url
    """
    results = []
    
    try:
        # Get the main page for exact match
        page = wiki.page(query)
        
        if page.exists():
            results.append({
                'title': page.title,
                'snippet': clean_snippet(page.summary),
                'url': page.fullurl
            })
        
        # Search for related pages
        import requests
        search_url = f"https://sv.wikipedia.org/w/api.php"
        params = {
            'action': 'opensearch',
            'search': query,
            'limit': limit,
            'namespace': 0,
            'format': 'json'
        }
        
        response = requests.get(search_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            titles = data[1] if len(data) > 1 else []
            descriptions = data[2] if len(data) > 2 else []
            urls = data[3] if len(data) > 3 else []
            
            # Add search results (skip duplicates)
            seen_titles = {r['title'] for r in results}
            
            for i, title in enumerate(titles):
                if title not in seen_titles and len(results) < limit:
                    snippet = descriptions[i] if i < len(descriptions) else ''
                    
                    # If no description, try to get page summary
                    if not snippet:
                        try:
                            article = wiki.page(title)
                            if article.exists():
                                snippet = clean_snippet(article.summary)
                        except:
                            snippet = 'Artikel tillgänglig på Wikipedia'
                    
                    results.append({
                        'title': title,
                        'snippet': snippet or 'Läs mer på Wikipedia',
                        'url': urls[i] if i < len(urls) else f"https://sv.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })
                    seen_titles.add(title)
        
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
