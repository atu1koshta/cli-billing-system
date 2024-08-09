from app.models.Bill import Bill
from app.models.Product import Product
from app.models.BillProduct import BillProduct
from app.config.DbConnection import Base, engine
from app.services.BillService import BillService
from app.services.ProductService import ProductService
from seed.seed import seed_products

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    seed_products()

    while True:
        print("\n1. Buy & Checkout")
        print("2. List all products")
        print("3. Add product")
        print("q. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            BillService.create_bill()
        elif choice == '2':
            ProductService.list_products()
        elif choice == '3':
            ProductService.add_product()
        elif choice == 'q':
            break
