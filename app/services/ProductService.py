from app.models.Product import Product
from tabulate import tabulate

from app.utils.Constant import Constant
import logging

log = logging.getLogger(__name__)


class ProductService:
    @staticmethod
    def add_product():
        try:
            name = input("Name: ")
            unit_price = int(input("Unit Price: "))
            discount_price = int(input("Discount Price: "))
            discount_units = int(input("Discount Units: "))

            product = Product.add_product(name, unit_price, discount_price, discount_units)

            if product is not None:
                log.info(f"Product {product.name} created successfully")
                print(f"\n[SUCCESS] Product {product.name} created successfully\n")
            else:
                log.error("Product creation failed")
                print("\n[FAILURE] Product creation failed. Try again.\n")
        except ValueError as e:
            log.error(f"Invalid input: {e}")
            print(f"\n[FAILURE] {e}\n")

    @staticmethod
    def list_products():
        products = Product.get_all_products()

        data = [[product.id, product.name, product.unit_price, product.discount_price, product.discount_units]
                for product in products]

        print(tabulate(data, headers=Constant.ALL_PRODUCTS_TABLE_HEADERS, tablefmt="grid"))

    @staticmethod
    def get_products_by_names(names: list):
        return Product.get_products_by_names(names)
