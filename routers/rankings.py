from fastapi import APIRouter , Depends
from  sqlmodel import Session
from database import get_session 
from services.ranking_service import get_overall_rankings

router = APIRouter(prefix="/rankings", tags=["Rankings"])

@router.get("/")
def overall_rankings(session : Session = Depends(get_session)):
    return get_overall_rankings(session)

@router.get("/state/{state}")
def state_rankings(state: str):
    return {"message": f"rankings for {state} - TODO"}

@router.get("/compare")
def compare_cities(city1: str, city2: str):
    return {"message": f"compare {city1} vs {city2} - TODO"}