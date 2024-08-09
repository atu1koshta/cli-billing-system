import logging

from sqlalchemy.exc import SQLAlchemyError
from tabulate import tabulate

from app.config.DbConnection import Session
from app.models.Bill import Bill
from app.services.BillProductService import BillProductService
from app.utils.Constant import Constant

log = logging.getLogger(__name__)


class BillService:

    @staticmethod
    def create_bill():
        cart_products = input("Enter the products to add in your cart: ")

        if not cart_products.isalpha() or not cart_products.isupper():
            print("\n[FAILURE] Cart products must be in uppercase letters\n")
            return

        bill, actual_total, discount_total = BillProductService.bill_products(cart_products)
        discount_percent = round((1 - discount_total / actual_total) * 100, 2)

        try:
            with Session() as session:
                bill = session.query(Bill).filter(Bill.id == bill.id).one_or_none()

                if not bill:
                    print(f"\n[FAILURE] No bill found with id {bill.id}\n")
                    return

                data = [
                    [bp.product.name, bp.product.unit_price, bp.total_units, bp.discount_percent, bp.price]
                    for bp in bill.products
                ]
                data.append(["Total", "", "", discount_percent, discount_total])

                print(f"\nBill Reference #: {bill.id}")
                print(tabulate(data, headers=Constant.BILL_TABLE_HEADERS, tablefmt="grid"))

        except SQLAlchemyError as e:
            log.error(f"Error listing bill products: {e}")
            print(f"\n[FAILURE] Error listing bill products: {e}\n")
