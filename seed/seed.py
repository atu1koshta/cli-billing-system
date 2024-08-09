from app.models.Product import Product
from sqlalchemy.exc import SQLAlchemyError
import logging

log = logging.getLogger(__name__)


def seed_products():
    products = [
        {
            "name": "A",
            "unit_price": 50,
            "discount_price": 130,
            "discount_units": 3
        },
        {
            "name": "B",
            "unit_price": 30,
            "discount_price": 45,
            "discount_units": 2
        },
        {
            "name": "C",
            "unit_price": 20,
        },
        {
            "name": "D",
            "unit_price": 15
        },
    ]

    for product in products:
        try:
            Product.add_product(**product)
        except SQLAlchemyError as e:
            log.error("SQLAlchemyError occured while seeding products")
            log.error(e)
        except Exception as e:
            log.error(e)
