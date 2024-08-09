from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.config.DbConnection import Base


class BillProduct(Base):
    __tablename__ = "bill_products"

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey('bills.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    total_units = Column(Integer, nullable=False)
    discount_percent = Column(Float, nullable=False)
    price = Column(Float, nullable=False)

    bill = relationship('Bill', back_populates='products')
    product = relationship("Product", back_populates='bills')
