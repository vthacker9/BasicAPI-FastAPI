from sqlalchemy import Column, String, TEXT, Integer
from database import Base

class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(TEXT)
    price = Column(Integer)
