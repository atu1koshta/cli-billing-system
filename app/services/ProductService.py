from collections import Counter

from app.models.Product import Product
from tabulate import tabulate

from app.utils.Constant import Constant


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
                print(f"\n[SUCCESS] Product {product.name} created successfully\n")
            else:
                print("\n[FAILURE] Product creation failed. Try again.\n")
        except ValueError as e:
            print(f"\n[FAILURE] {e}\n")

    @staticmethod
    def list_products():
        products = Product.get_all_products()

        data = [[product.id, product.name, product.unit_price, product.discount_price, product.discount_units]
                for product in products]

        print(tabulate(data, headers=Constant.ALL_PRODUCTS_TABLE_HEADERS, tablefmt="grid"))

    @staticmethod
    def buy_and_checkout():
        cart_products = input("Enter the products to add in your cart: ")

        if not cart_products.isalpha() or not cart_products.isupper():
            print("\n[FAILURE] Cart products must be in uppercase letters\n")
            return

        product_counter = Counter(cart_products)
        products = Product.get_products_by_names(list(product_counter.keys()))

        data = ProductService._create_final_bill(products, product_counter)

        print(tabulate(data, headers=Constant.FINAL_BILL_TABLE_HEADERS, tablefmt="grid"))

    # PRIVATE METHODS
    @staticmethod
    def _product_bill(unit_price, total_units, discount_price, discount_units):
        if discount_price is None or discount_units is None:
            return 0, total_units * unit_price

        discount_bunch_count = total_units // discount_units
        actual_price_units_count = total_units - discount_bunch_count * discount_units

        actual_price = total_units * unit_price
        final_price = discount_bunch_count * discount_price + actual_price_units_count * unit_price
        discount_percent = round((actual_price - final_price) / actual_price * 100, 2)

        return discount_percent, final_price

    @staticmethod
    def _create_final_bill(products, product_counter):
        discount_total = 0
        actual_total = 0
        data = []

        for product in products:
            total_units = product_counter[product.name]
            discount_percent, price = ProductService._product_bill(product.unit_price, total_units,
                                                                   product.discount_price, product.discount_units)
            actual_total += total_units * product.unit_price
            discount_total += price

            data.append([product.name, product.unit_price, total_units, discount_percent, price])

        overall_discount = round((actual_total - discount_total) / actual_total * 100, 2)
        data.append(["Total", "", "", overall_discount, discount_total])

        return data
