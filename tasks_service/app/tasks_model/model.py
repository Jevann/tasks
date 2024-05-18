from pydantic import BaseModel
from datetime import date
from typing import Optional

class Task(BaseModel):
    id: Optional[int]
    title: str
    description: str
    priority: int
    due_date: date
