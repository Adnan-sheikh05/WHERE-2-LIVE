from sqlmodel import SQLModel , Field 
from typing import Optional  
from datetime import datetime

class SavedComparison(SQLModel , table=True) : 
    id : Optional[int] = Field(default=None , primary_key=True)
    user_id : int = Field(foreign_key="user.id")
    city1_id : int = Field(foreign_key="city.id")
    city2_id : int = Field(foreign_key="city.id")
    ai_summary : Optional[str] = None
    created_at : datetime = Field(default_factory=datetime.utcnow)