**_Sneaker E-commerce Website with Flask_**

**Introduction**

This is a shoe selling website built using Flask, MySQL, and PyMySQL. All products are stored in the database and can be accessed through the website.

**Requirements**
* Flask
* MySQL
* PyMySQL
* Other dependencies are listed in requirements.txt file.

**Setting up the environment**

1.Create a virtual environment.


2.Install the dependencies using the following command:

`pip install -r requirements.txt`

**Database Setup**

1.Create the database and tables using the following SQL commands:

`
CREATE DATABASE IF NOT EXISTS user_system;`

`CREATE TABLE IF NOT EXISTS products (
  pid INT NULL,
  pname VARCHAR(255) NULL,
  productprice DECIMAL(10,2) NULL
);    
`

`CREATE TABLE IF NOT EXISTS cart (
  productid INT NOT NULL PRIMARY KEY,
  pname VARCHAR(255) NOT NULL,
  productprice FLOAT NOT NULL,
  quantity INT NOT NULL,
  size VARCHAR(255) NULL,
  userid INT NOT NULL,
  total_price INT NULL,
  FOREIGN KEY (userid) REFERENCES user(userid)
);`

`CREATE TABLE IF NOT EXISTS orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  userid INT NULL,
  product_id INT NULL,
  quantity INT NOT NULL,
  size VARCHAR(20) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (userid) REFERENCES user(userid),
  FOREIGN KEY (product_id) REFERENCES products(pid)
);
`

`CREATE TABLE IF NOT EXISTS user (
  userid INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  address VARCHAR(255) NULL
);
`

`INSERT INTO products (pid, pname, productprice)
VALUES
(1, 'Sneaker 1', 50.00),
(2, 'Sneaker 2', 60.00),
(3, 'Sneaker 3', 70.00),
`

2.Configure the database by updating the host, username, and password in the config.py file.

**Tools and Technologies**

* The project was built using PyCharm and MySQL Workbench.

* PyMySQL was used as the Object Relational Mapping (ORM) tool.

**Author**

The project was built by the author alone.