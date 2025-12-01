from fastapi import APIRouter
from models.expense import Expense

router = APIRouter()

@router.post("/guardar_gasto")
async def guardar_gasto(data: Expense):
    return {"mensaje": "Datos recibidos correctamente", "data": data}
