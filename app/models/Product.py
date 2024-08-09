from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import validates
from app.config.DbConnection import Base, engine, Session
from sqlalchemy.exc import SQLAlchemyError
import logging


class Product(Base):
    __tablename__ = "products"
    log = logging.getLogger(__name__)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    unit_price: Mapped[int] = mapped_column(Integer)
    discount_price: Mapped[int] = mapped_column(Integer, nullable=True)
    discount_units: Mapped[int] = mapped_column(Integer, nullable=True)

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

    # Class Methods
    @classmethod
    def add_product(cls, name: str, unit_price: int, discount_price: int = None, discount_units: int = None):
        product = cls(name=name, unit_price=unit_price, discount_price=discount_price,
                      discount_units=discount_units)

        try:
            with Session() as session:
                session.add(product)
                session.commit()
                session.refresh(product)

                cls.log.info(f"Product {name} added successfully")

                return product
        except SQLAlchemyError as e:
            cls.log.error(e)

    @classmethod
    def get_all_products(cls):
        try:
            with Session() as session:
                return session.query(cls).all()
        except SQLAlchemyError as e:
            cls.log.error(e)

    @classmethod
    def get_products_by_names(cls, names: list):
        try:
            with Session() as session:
                return session.query(cls).filter(cls.name.in_(names)).all()
        except SQLAlchemyError as e:
            cls.log.error(e)


Base.metadata.create_all(engine)
