from fastapi import APIRouter

router = APIRouter()


@router.get("/expenses")
async def get_expenses():
    return []


@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str):
    return {"message": "delete endpoint - Phase 3에서 구현 예정"}


@router.put("/expenses/{expense_id}")
async def update_expense(expense_id: str):
    return {"message": "update endpoint - Phase 3에서 구현 예정"}
