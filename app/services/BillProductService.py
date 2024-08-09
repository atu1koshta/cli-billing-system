import logging
from collections import Counter

from sqlalchemy.exc import SQLAlchemyError

from app.config.DbConnection import Session
from app.models.Bill import Bill
from app.models.BillProduct import BillProduct
from app.services.ProductService import ProductService

log = logging.getLogger(__name__)


class BillProductService:
    @staticmethod
    def bill_products(cart_products: str):
        product_counter = Counter(cart_products)
        names = list(product_counter.keys())
        products = ProductService.get_products_by_names(names)

        if not products:
            print("\nNo valid products found in the cart\n")
        if len(products) != len(names):
            missing_products = set(names) - set([product.name for product in products])
            print("\nFollowing product(s) are not available! Billing rest...")
            print(' '.join(missing_products))

        product_counter = Counter(cart_products)
        actual_total, discount_total = 0, 0

        try:
            with Session() as session:
                bill = Bill()
                session.add(bill)
                session.flush()

                for product in products:
                    total_units = product_counter[product.name]
                    discount_percent, price = BillProductService._calculate_price(product, total_units)

                    actual_total += total_units * product.unit_price
                    discount_total += price

                    bill_product = BillProduct(bill_id=bill.id, product_id=product.id, total_units=total_units,
                                               discount_percent=discount_percent, price=price)
                    session.add(bill_product)

                session.commit()

                log.info(f"Bill products added successfully for bill_id: {bill.id}")

                return bill, actual_total, discount_total
        except SQLAlchemyError as e:
            log.error(e)

    @staticmethod
    def _calculate_price(product, total_units):
        if product.discount_price is None or product.discount_units is None:
            return 0, total_units * product.unit_price

        discount_bunch_count = total_units // product.discount_units
        actual_price_units_count = total_units - discount_bunch_count * product.discount_units

        actual_price = total_units * product.unit_price
        final_price = discount_bunch_count * product.discount_price + actual_price_units_count * product.unit_price
        discount_percent = round((actual_price - final_price) / actual_price * 100, 2)

        return discount_percent, final_price
