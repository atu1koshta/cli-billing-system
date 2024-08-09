from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import validates
from app.config.DbConnection import Base, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

log = logging.getLogger(__name__)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    unit_price: Mapped[int] = mapped_column(Integer)
    discount_price: Mapped[int] = mapped_column(Integer, nullable=True)
    discount_units: Mapped[int] = mapped_column(Integer, nullable=True)

    bills = relationship('BillProduct', back_populates='product')

    @validates('name')
    def validate_name(self, _, value):
        if not value:
            raise ValueError("Name can't be empty")
        if len(value) > 1:
            raise ValueError("Name must be an uppercase letter")
        if not value.isupper():
            raise ValueError("Name must be in uppercase")

        return value

    @validates('unit_price')
    def validate_unit_price(self, key, value):
        if value is None:
            raise ValueError("Unit price is required")
        if value < 1:
            raise ValueError("Unit price must be greater than 0")

        return value

    def validate_discount(self):
        if (self.discount_price is None and self.discount_units is not None) or (
                self.discount_price is not None and self.discount_units is None):
            raise ValueError("Both discount price and discount units must be provided together")
        elif self.discount_price is not None and self.discount_units is not None:
            if self.discount_price < 1:
                raise ValueError("Discount price must be greater than 0")
            if self.discount_units < 1:
                raise ValueError("Discount units must be greater than 0")
            if self.discount_price / self.discount_units > self.unit_price:
                raise ValueError("Discount price per unit must be less than or equal to unit price")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_discount()

    @staticmethod
    def add_product(name: str, unit_price: int, discount_price: int = None, discount_units: int = None):
        product = Product(name=name, unit_price=unit_price, discount_price=discount_price,
                          discount_units=discount_units)

        try:
            with Session() as session:
                session.add(product)
                session.commit()
                session.refresh(product)

                log.info(f"Product {name} added successfully")

                return product
        except SQLAlchemyError as e:
            log.error(e)

    @staticmethod
    def get_all_products():
        try:
            with Session() as session:
                return session.query(Product).all()
        except SQLAlchemyError as e:
            log.error(e)

    @staticmethod
    def get_products_by_names(names: list):
        try:
            with Session() as session:
                return session.query(Product).filter(Product.name.in_(names)).all()
        except SQLAlchemyError as e:
            Product.log.error(e)
