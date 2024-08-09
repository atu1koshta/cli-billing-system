from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship

from app.config.DbConnection import Base, Session


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)

    products = relationship("BillProduct", back_populates="bill")