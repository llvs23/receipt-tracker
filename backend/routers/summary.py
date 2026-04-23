from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
async def get_summary():
    return {"total_amount": 0, "this_month_amount": 0, "category_summary": []}
