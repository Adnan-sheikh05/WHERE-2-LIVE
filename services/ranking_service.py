from sqlmodel import Session , select , func 
from models.city import City , CityMetric 

def get_overall_rankings(session : Session) :
    statement = (select(City.name ,
                        func.avg(CityMetric.cost_of_living).label("cost"),
                        func.avg(CityMetric.air_quality_index).label("air"),
                        func.avg(CityMetric.safety_score).label("safety"),
                        func.avg(CityMetric.healthcare_score).label("healthcare")
                        )
                        .join(CityMetric , City.id == CityMetric.city_id)
                        .group_by(City.name)
                )
    results = session.exec(statement).all()
    ranked = []
    for name , cost , air , safety , healthcare in results : 
        score = (safety * 0.35) + (air * 0.25) + (healthcare * 0.25) - (cost / 100 * 0.15)
        ranked.append({"city": name, "livability_score": round(score, 2)})
    ranked.sort(key = lambda x:x["livability_score"] , reverse=True)
    return ranked