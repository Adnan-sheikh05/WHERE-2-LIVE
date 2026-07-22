from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session, select 
from database import get_session
from models.city import City , CityMetric 
from seed.seed_runner import run_seed

router = APIRouter(prefix="/cities" , tags=["Cities"])

@router.get("/")
def list(session : Session = Depends(get_session)) :
    cities = session.exec(select(City)).all()
    if len(cities) == 0 :
        run_seed()
    return cities

@router.post("/")
def add_city() :
    return {"message" : f"city created"}

@router.get("/{city_id}")
def get_city(city_id : int , session : Session = Depends(get_session)) :
    city = session.get(City , city_id)
    if not city : 
        raise HTTPException(status_code=404 , details="City Not Found")
    return city

@router.put("/{city_id}")
def update_city(city_id : int) :
    return {"message" : f"{city_id} updated"}

@router.get("/{city_id}/history")
def get_histroy(city_id : int , session : Session = Depends(get_session)) :
    statement = select(CityMetric).where(CityMetric.city_id == city_id)
    return session.exec(statement).all()