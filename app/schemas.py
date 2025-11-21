from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ExpenseCreate(BaseModel):
    title: str = Field(..., max_length=256)
    amount: float
    category: Optional[str] = None
    date: Optional[date] = None

class ExpenseOut(BaseModel):
    id: int
    title: str
    amount: float
    category: Optional[str]
    date: date

    class Config:
        orm_mode = True
