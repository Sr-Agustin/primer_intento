from pydantic import BaseModel

class Expense(BaseModel):
    tipo: str
    importe: float
    notas: str | None = None
