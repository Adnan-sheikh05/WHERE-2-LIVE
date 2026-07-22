from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session , select 
from database import get_session 
from models.city import City , CityMetric 
from services.llm_service import generate_comparison_summary , generate_recommendation

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/summary")
async def ai_summary(city1 :  str , city2 : str , session : Session = Depends (get_session)):
    c1 = session.exec(select(City).where(City.name == city1)).first()
    c2 = session.exec(select(City).where(City.name == city2)).first()
    if not c1 or not c2 :
        raise HTTPException(status_code=404 , detail="City Not Found!")
    try : 
        summary = await generate_comparison_summary(c1.dict() , c2.dict())
        return {"summary" : summary}
    except Exception as e :
        raise HTTPException(status_code=502 , detail=f"AI service failed {e}")
   

@router.post("/recommend")
async def ai_recommend(preference : str , session : Session = Depends(get_session)):
    cities = session.exec(select(City)).all()
    recommendation = await generate_recommendation(preference , cities)
    return {"recommendation": recommendation}