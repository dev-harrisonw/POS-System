# Pytest code
import pytest

from main import Order, orderFunctions, pyodbc


@pytest.fixture
def db_conn():
    yield pyodbc.connect(
        "DRIVER={SQL Server};SERVER=inc-sandbox.database.windows.net,1433",
        user="inc_root",
        password="Golfer70!_",
        database="SAND-02",
    )


def test_createOrder(db_conn):
    order = Order(1, "John", "Coffee", "Large", "None", 5)
    service = orderFunctions(db_conn)
    service.createOrder(order)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=?", (1,))
    row = cursor.fetchone()
    assert row.order_id == 1
    assert row.customer_name == "John"
    assert row.drink == "Coffee"
    assert row.size == "Large"
    assert row.extras == "None"
    assert row.price == 5


def test_readOrder(db_conn):
    order = Order(2, "John", "Coffee", "Large", "None", 5)
    service = orderFunctions(db_conn)
    service.createOrder(order)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=?", (2,))
    row = cursor.fetchone()
    assert row.order_id == 2


def test_readAllOrders(db_conn):
    order1 = Order(3, "John", "Coffee", "Large", "None", 5)
    order2 = Order(4, "Jane", "Tea", "Small", "Cream", 3)
    service = orderFunctions(db_conn)
    service.createOrder(order1)
    service.createOrder(order2)
    orders = service.readAllOrders()
    assert len(orders) >= 1


def test_updateOrder(db_conn):
    order = Order(5, "John", "Coffee", "Large", "None", 5)
    service = orderFunctions(db_conn)
    service.createOrder(order)
    order.customer_name = "Jane"
    order.drink = "Tea"
    order.size = "Small"
    order.extras = "Cream"
    order.price = 3
    service.updateOrder(order)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=?", (5,))
    row = cursor.fetchone()
    assert row.order_id == 5
    assert row.customer_name == "Jane"
    assert row.drink == "Tea"
    assert row.size == "Small"
    assert row.extras == "Cream"
    assert row.price == 3


def test_deleteOrder(db_conn):
    order = Order(6, "John", "Coffee", "Large", "None", 5)
    service = orderFunctions(db_conn)
    service.createOrder(order)
    service.deleteOrder(6)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=?", (6,))
    row = cursor.fetchone()
    assert row == row is None


def test_deleteAllOrders(db_conn):
    order1 = Order(7, "John", "Coffee", "Large", "None", 5)
    order2 = Order(8, "Jane", "Tea", "Small", "Cream", 3)
    service = orderFunctions(db_conn)
    service.createOrder(order1)
    service.createOrder(order2)
    service.deleteAllOrders()
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    assert rows == []
