import sqlite3
import random
from datetime import datetime, timedelta

# データベース接続
conn = sqlite3.connect('sqlite/sql_practice.sqlite')
cursor = conn.cursor()

# 顧客名と商品名のサンプルデータ
customer_names = [f"顧客{str(i).zfill(3)}" for i in range(1, 101)]
product_names = [f"商品{str(i).zfill(3)}" for i in range(1, 101)]

# 商品データの挿入
for i, product_name in enumerate(product_names, start=1):
    unit_price = random.randint(100, 1000)
    units_in_stock = random.randint(10, 100)
    cursor.execute("INSERT INTO Products (ProductID, ProductName, UnitPrice, UnitsInStock) VALUES (?, ?, ?, ?)",
                   (i, product_name, unit_price, units_in_stock))

# 顧客データの挿入
for i, customer_name in enumerate(customer_names, start=1):
    email = f"customer{i}@example.com"
    cursor.execute("INSERT INTO Customers (CustomerID, FirstName, LastName, Email) VALUES (?, ?, ?, ?)",
                   (i, customer_name, "", email))

# 注文データの挿入
order_id = 1
order_detail_id = 1  # 注文明細IDの初期化をループの外に移動
for _ in range(1000):
    customer_id = random.randint(1, 100)
    order_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))
    total_amount = random.randint(500, 10000)
    cursor.execute("INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount) VALUES (?, ?, ?, ?)",
                   (order_id, customer_id, order_date.strftime('%Y-%m-%d'), total_amount))

    for _ in range(random.randint(1, 3)):
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 5)
        unit_price = cursor.execute("SELECT UnitPrice FROM Products WHERE ProductID = ?", (product_id,)).fetchone()[0]
        cursor.execute("INSERT INTO OrderDetails (OrderDetailID, OrderID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?, ?)",
                       (order_detail_id, order_id, product_id, quantity, unit_price))
        order_detail_id += 1  # 注文明細IDをインクリメント
    order_id += 1

# コミットして接続を閉じる
conn.commit()
conn.close() 