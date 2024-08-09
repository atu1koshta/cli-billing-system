# CLI Billing System

This project is a CLI Billing System built with Python. The application is containerized using Docker.

## Prerequisites

- Docker installed on your machine

## Getting Started

Follow these steps to run the project using a Docker container:

1. **Clone the repository:**
    ```sh
    git clone git@github.com:atu1koshta/cli-billing-system.git
    ```

2. **Navigate to the cloned repository:**
    ```sh
    cd cli-billing-system
    ```

3. **Build the Docker image:**
    ```sh
    docker build -t cli-billing-system .
    ```

4. **Run the Docker container:**
    ```sh
    docker run -it cli-billing-system
    ```

The application should now be running inside the Docker container, in interactive mode.

## Initial Setup
Upon successful running application, 4 products('A', 'B', 'C' and 'D') are already seeded. 
Select '2' to view list of stored items.

## Usage
The application provides the following option in command line interface:
1. **Buy & Checkout**
   Upon selecting this option, user can buy product and checkout. User can buy multiple products at once by providing
    names of products without any space in between. For example, 'ABCD' will buy product 'A', 'B', 'C' and 'D'.
    If unsure about the existing products, user can select '2' to view list of stored items.

    Example:
    ```sh
    Enter your choice: 1
    Enter the products to add in your cart: AAABBD
   ```
   Output: 
   ```sh
    Bill Reference #: 1
    +----------------+--------------+---------------+--------------+---------+
    | Product Name   | Unit Price   | Total Units   |   Discount % |   Price |
    +================+==============+===============+==============+=========+
    | A              | 50           | 3             |        13.33 |     130 |
    +----------------+--------------+---------------+--------------+---------+
    | B              | 30           | 2             |        25    |      45 |
    +----------------+--------------+---------------+--------------+---------+
    | D              | 15           | 1             |         0    |      15 |
    +----------------+--------------+---------------+--------------+---------+
    | Total          |              |               |        15.56 |     190 |
    +----------------+--------------+---------------+--------------+---------+
   ```
   The above command will add 3 products 'A', 2 products 'B' and 1 product 'D' in the cart. Press 'Enter' to checkout
    and generate bill. The total amount will be displayed at the last line of the bill.

2. **List all products**
   This option will list all the products stored in the system.
    
    Example:
    ```sh
   Enter your choice: 2
   ```
    Output:
   ```sh
   +------+--------+--------------+------------------+------------------+
    |   ID | Name   |   Unit Price |   Discount Price |   Discount Units |
    +======+========+==============+==================+==================+
    |    1 | A      |           50 |              130 |                3 |
    +------+--------+--------------+------------------+------------------+
    |    2 | B      |           30 |               45 |                2 |
    +------+--------+--------------+------------------+------------------+
    |    3 | C      |           20 |                  |                  |
    +------+--------+--------------+------------------+------------------+
    |    4 | D      |           15 |                  |                  |
    +------+--------+--------------+------------------+------------------+ 
    ```
 
3. **Add product**
   This option will allow user to add new product in the system. User will be prompted to enter product name and price.

    Example:
    ```sh
    Enter your choice: 3
    Name: Y
    Unit Price: 12
    Discount Price: 20
    Discount Units: 2
    ```
    - 'Name' should be unique among products. Use option '2' to know existing products.
    - 'Discount Price' per 'Discount Units' should be less than or equal to Unit Price of product. For ex. 20/2 < 12

4. Use 'q' to exit program