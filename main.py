import time

import pyodbc
from tabulate import tabulate

print(
    """

    ░██████╗░░█████╗░  ░█████╗░░█████╗░███████╗███████╗
    ██╔═══██╗██╔══██╗  ██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██║██╗██║███████║  ██║░░╚═╝███████║█████╗░░█████╗░░
    ╚██████╔╝██╔══██║  ██║░░██╗██╔══██║██╔══╝░░██╔══╝░░
    ░╚═██╔═╝░██║░░██║  ╚█████╔╝██║░░██║██║░░░░░███████╗
    ░░░╚═╝░░░╚═╝░░╚═╝  ░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚══════╝
                                   """
)


class Order:
    def __init__(self, order_id, customer_name, drink, size, extras, price):
        self.order_id = order_id
        self.customer_name = customer_name
        self.drink = drink
        self.size = size
        self.extras = extras
        self.price = price


class orderFunctions:
    def __init__(self, db_conn):
        self.db_conn = pyodbc.connect(
            "DRIVER={SQL Server};SERVER=SERVER_HERE",
            user="USER_HERE",
            password="PASSWORD_HERE",
            database="DB_HERE",
        )

    def createOrder(self, order):
        cursor = self.db_conn.cursor()
        cursor.execute(
            """INSERT INTO orders
             (order_id, customer_name, drink, size, extras, price)
             VALUES (?, ?, ?, ?, ?, ?)""",
            (
                order.order_id,
                order.customer_name,
                order.drink,
                order.size,
                order.extras,
                order.price,
            ),
        )
        self.db_conn.commit()

    def readOrder(self, order_id):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        row = cursor.fetchone()
        if row:
            return Order(*row)
        return None

    def readAllOrders(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        if rows:
            return [
                Order(
                    row.order_id,
                    row.customer_name,
                    row.drink,
                    row.size,
                    row.extras,
                    row.price,
                )
                for row in rows
            ]
        return []

    def updateOrder(self, order):
        cursor = self.db_conn.cursor()
        cursor.execute(
            """UPDATE orders
             SET customer_name=?, drink=?, size=?, extras=?, price=? WHERE order_id=?""",
            (
                order.customer_name,
                order.drink,
                order.size,
                order.extras,
                order.price,
                order.order_id,
            ),
        )
        self.db_conn.commit()

    def deleteOrder(self, order_id):
        cursor = self.db_conn.cursor()
        cursor.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
        self.db_conn.commit()

    def deleteAllOrders(self):
        cursor = self.db_conn.cursor()
        cursor.execute("DELETE FROM orders")
        self.db_conn.commit()


class orderController:
    def __init__(self, db_conn):
        self.service = orderFunctions(db_conn)

    def createOrder(self, order_id, customer_name, drink, size, extras, price):
        order = Order(order_id, customer_name, drink, size, extras, price)
        self.service.createOrder(order)

    def updateOrder(self, order_id, customer_name, drink, size, extras, price):
        order = Order(order_id, customer_name, drink, size, extras, price)
        self.service.updateOrder(order)

    def readOrder(self, order_id):
        return self.service.readOrder(order_id)

    def readAllOrders(self):
        return self.service.readAllOrders()

    def deleteOrder(self, order_id):
        self.service.deleteOrder(order_id)

    def deleteAllOrders(self):
        self.service.deleteAllOrders()


def main():
    db_conn = None
    controller = orderController(db_conn)
    while True:
        print(
            """
        }------------------------------------{
        1. Create Order
        2. Read Order
        3. Read All Orders
        4. Update Order
        5. Delete Order
        6. Delete All Orders
        7. Quit
        }------------------------------------{\n"""
        )

        choice = input("Enter your choice: ")

        if choice == "1":
            order_id = input("Enter the order ID: ")
            customer_name = input("Enter the customer name: ")
            drink = input("Enter the drink: ")
            size = input("Enter the size: ")
            extras = input("Enter any extras: ")
            price = input("Enter the price: ")
            controller.createOrder(order_id, customer_name, drink, size, extras, price)
            time.sleep(2)
        elif choice == "2":
            order_id = input("Enter the order ID: ")
            order = controller.readOrder(order_id)
            if order:
                orders = controller.readAllOrders()
                headers = [
                    "Order ID",
                    "Customer Name",
                    "Drink",
                    "Size",
                    "Extras",
                    "Price",
                ]
                table = [
                    [
                        order.order_id,
                        order.customer_name,
                        order.drink,
                        order.size,
                        order.extras,
                        order.price,
                    ]
                ]
                print("\n", tabulate(table, headers), "\n")
            else:
                print("Order not found.")
            time.sleep(2)
        elif choice == "3":
            # Read all orders
            orders = controller.readAllOrders()
            headers = ["Order ID", "Customer Name", "Drink", "Size", "Extras", "Price"]
            table = [
                [
                    order.order_id,
                    order.customer_name,
                    order.drink,
                    order.size,
                    order.extras,
                    order.price,
                ]
                for order in orders
            ]
            print("\n", tabulate(table, headers), "\n")
            time.sleep(2)
        elif choice == "4":
            order_id = input("Enter the order ID: ")
            order = controller.readOrder(order_id)
            if order:
                customer_name = input("Enter the new customer name: ")
                drink = input("Enter the new drink: ")
                size = input("Enter the new size: ")
                extras = input("Enter the new extras: ")
                price = input("Enter the new price: ")
                order.customer_name = customer_name
                order.drink = drink
                order.size = size
                order.extras = extras
                order.price = price
                controller.updateOrder(
                    order_id, customer_name, drink, size, extras, price
                )
            else:
                print("Order not found.")
            time.sleep(2)
        elif choice == "5":
            order_id = input("Enter the order ID: ")
            controller.deleteOrder(order_id)
        elif choice == "6":
            controller.deleteAllOrders()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
