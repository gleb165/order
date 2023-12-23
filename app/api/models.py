from pydantic import BaseModel
from datetime import datetime


class OrderIn(BaseModel):
    user_id: int
    show_id: int
    amount: int


class OrderOut(OrderIn):
    id: int


class OrderUpdate(BaseModel):
    amount: int | None = None
