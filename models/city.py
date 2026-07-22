from sqlmodel import SQLModel , Field , Relationship
from typing import Optional , List 

class City(SQLModel , table=True) :
    id : Optional[int] = Field(default=None , primary_key=True)
    name : str
    state : str
    population : int
    metrics :  List["CityMetric"] = Relationship(back_populates="city")

class CityMetric(SQLModel , table=True) :
    id : Optional[int] = Field(default=None , primary_key=True)
    city_id : int = Field(foreign_key="city.id")
    year : int 
    cost_of_living : float
    air_quality_index : float
    safety_score : float 
    healthcare_score : float 
    city : Optional[City] = Relationship(back_populates="metrics")