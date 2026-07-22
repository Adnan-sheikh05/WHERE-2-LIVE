from fastapi import APIRouter
router = APIRouter(prefix="/comparisons", tags=["Saved Comparisons"])

@router.post("/")
def save_comparison():
    return {"message": "save comparison - TODO"}

@router.get("/mine")
def my_comparisons():
    return {"message": "my saved comparisons - TODO"}
