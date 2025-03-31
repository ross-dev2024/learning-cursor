CREATE TABLE Customers (
  CustomerID INTEGER PRIMARY KEY,
  FirstName VARCHAR(255),
  LastName VARCHAR(255),
  Email VARCHAR(255)
);

-- 製品テーブル
CREATE TABLE Products (
  ProductID INTEGER PRIMARY KEY,
  ProductName VARCHAR(255),
  UnitPrice NUMERIC,
  UnitsInStock INTEGER
);

-- 注文テーブル
CREATE TABLE Orders (
  OrderID INTEGER PRIMARY KEY,
  CustomerID INTEGER,
  OrderDate DATE,
  TotalAmount NUMERIC,
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- 注文詳細テーブル
CREATE TABLE OrderDetails (
  OrderDetailID INTEGER PRIMARY KEY,
  OrderID INTEGER,
  ProductID INTEGER,
  Quantity INTEGER,
  UnitPrice NUMERIC,
  FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
  FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
); 
