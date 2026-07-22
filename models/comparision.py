from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel

from database import get_session
from models.comparision import SavedComparison
from models.city import City
from models.user import User
from services.dependencies import get_current_user

router = APIRouter(
    prefix="/comparisons",
    tags=["Saved Comparisons"]
)


class ComparisonCreate(SQLModel):
    city1_id: int
    city2_id: int
    ai_summary: str | None = None


@router.post("/")
def save_comparison(
    data: ComparisonCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check first city
    city1 = session.get(City, data.city1_id)
    if not city1:
        raise HTTPException(
            status_code=404,
            detail="First city not found"
        )

    # Check second city
    city2 = session.get(City, data.city2_id)
    if not city2:
        raise HTTPException(
            status_code=404,
            detail="Second city not found"
        )

    comparison = SavedComparison(
        user_id=current_user.id,
        city1_id=data.city1_id,
        city2_id=data.city2_id,
        ai_summary=data.ai_summary
    )

    session.add(comparison)
    session.commit()
    session.refresh(comparison)

    return {
        "message": "Comparison saved successfully",
        "comparison": comparison
    }


@router.get("/mine")
def my_comparisons(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    comparisons = session.exec(
        select(SavedComparison).where(
            SavedComparison.user_id == current_user.id
        )
    ).all()

    return {
        "total": len(comparisons),
        "comparisons": comparisons
    }