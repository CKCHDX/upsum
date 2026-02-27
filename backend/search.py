from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/search")
def search(q: str = Query("", description="Fråga eller ämne på svenska")):
    """Search endpoint. Currently returns empty results - Wikipedia integration pending."""
    if not q or q.strip() == "":
        return JSONResponse({"results": [], "count": 0})
    
    # TODO: Implement actual Swedish Wikipedia search
    return JSONResponse({"results": [], "count": 0})
