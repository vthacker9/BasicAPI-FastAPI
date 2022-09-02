from typing import List, Optional
from pydantic import BaseModel

class Product(BaseModel):
    title: str = None
    description: str = None
    price: int = None
    
    class Config:
        orm_mode = True