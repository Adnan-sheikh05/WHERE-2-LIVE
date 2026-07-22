from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session, select 
from database import get_session
from models.city import City , CityMetric 
from seed.seed_runner import run_seed
from services.dependencies import get_current_user
from sqlmodel import SQLModel
from typing import Optional
from models.user import User


class CityCreate(SQLModel):
    name: str
    state: str
    population: int
    year: int
    cost_of_living: float
    air_quality_index: float
    safety_score: float
    healthcare_score: float


class CityUpdate(SQLModel):
    name: str
    state: str
    population: int
    year: int
    cost_of_living: float
    air_quality_index: float
    safety_score: float
    healthcare_score: float
router = APIRouter(prefix="/cities" , tags=["Cities"])

@router.get("/")
def list(session : Session = Depends(get_session)) :
    cities = session.exec(select(City)).all()
    if len(cities) == 0 :
        run_seed()
    return cities

@router.post("/")
def add_city(
    data: CityCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    city = City(
        name=data.name,
        state=data.state,
        population=data.population
    )

    session.add(city)
    session.flush()   # city.id generate ho jayegi

    metric = CityMetric(
        city_id=city.id,
        year=data.year,
        cost_of_living=data.cost_of_living,
        air_quality_index=data.air_quality_index,
        safety_score=data.safety_score,
        healthcare_score=data.healthcare_score
    )

    session.add(metric)
    session.commit()

    return {
        "message": "City added successfully",
        "city": city,
        "metric": metric
    }

@router.get("/{city_id}")
def get_city(city_id : int , session : Session = Depends(get_session)) :
    city = session.get(City , city_id)
    if not city : 
        raise HTTPException(status_code=404 , details="City Not Found")
    return city

@router.put("/{city_id}")
def update_city(
    city_id: int,
    data: CityUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    city = session.get(City, city_id)

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    # Update City Table
    city.name = data.name
    city.state = data.state
    city.population = data.population

    # Find City Metric
    metric = session.exec(
        select(CityMetric).where(CityMetric.city_id == city_id)
    ).first()

    if not metric:
        raise HTTPException(
            status_code=404,
            detail="City Metric not found"
        )

    # Update Metric Table
    metric.year = data.year
    metric.cost_of_living = data.cost_of_living
    metric.air_quality_index = data.air_quality_index
    metric.safety_score = data.safety_score
    metric.healthcare_score = data.healthcare_score

    session.add(city)
    session.add(metric)
    session.commit()
    session.refresh(city)
    session.refresh(metric)

    return {
        "message": "City updated successfully",
        "city": city,
        "metric": metric
    }

@router.get("/{city_id}/history")
def get_history(city_id : int , session : Session = Depends(get_session)) :
    statement = select(CityMetric).where(CityMetric.city_id == city_id)
    return session.exec(statement).all()