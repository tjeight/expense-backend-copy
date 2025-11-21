from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base
import datetime

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(128), nullable=True)
    date = Column(Date, nullable=False, default=datetime.date.today)
