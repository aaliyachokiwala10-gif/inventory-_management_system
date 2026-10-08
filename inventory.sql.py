import sqlite3
import os
from datetime import datetime, date, time

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "inventory.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#cursor.execute("""CREATE TABLE products (id int primary key, 
                  #name varchar(100), 
                  #ategory varchar(100),
                  #ice float,
                  #quantity float)
                  #""")
#conn.commit()

#cursor.execute("""CREATE TABLE sales (id int primary key,
                #product_id int unique,
                #quantity float,
                #total_price float,
                #sale_date date)""")
#conn.commit()

#cursor.execute("INSERT INTO products (name, category, price, quantity) VALUES(?,?,?,?)", ("cooking pots", "kitchen ware", 45.00, 10) )
#conn.commit()

def add_products():
    name = input("enter the name of the product: ")
    category = input("enter the category of the product: ")
    price = float(input("eneter the price of the product: "))
    quantity = float(input("enter the quantity of the product: "))
    cursor.execute("INSERT INTO products (name, category, price, quantity) VALUES(?,?,?,?)", (name, category, price, quantity) )
    conn.commit()
    print("product added successfully")


def view_products():
    cursor.execute("select * from products")
    products = cursor.fetchall()
    for item in products:
        print(f"name: {item[1]}")
        print(f"category: {item[2]}")
        print(f"price: {item[3]}")
        print(f"quantity: {item[4]}")

def search_products():
    try:
        product_name = input("enter the name of the product to search: ")
        searched = cursor.execute("select * from products where name = ?", (product_name,))
        products = searched.fetchall()
        for item in products:
            print(f"name: {item[1]}")
            print(f"category: {item[2]}")
            print(f"price: {item[3]}")
            print(f"quantity: {item[4]}")
    except Exception as e:
        print("erorr", e)

def make_sale():
    product_name = input("enter the name of the product: ").lower()
    cursor.execute("select * from products where name  = ?", (product_name,))
    product = cursor.fetchone()
    users_quantity = float(input("enter the quantity: "))
    print(product)
    available_products = product[4]
    if users_quantity <= available_products:
        product_price = product[3]
        total_price = product_price * users_quantity
        available_stock = available_products - users_quantity
        cursor.execute("""update products 
                          set quantity = ?
                          where name = ? """, (available_stock, product_name))
        conn.commit()
        print(f"sale can proceed your total price is:  {total_price} and remaining stock is {available_stock}")
        cursor.execute("insert into sales (product_id, quantity, total_price, sale_date) VALUES (?,?,?,?)", (product[0], users_quantity, total_price, datetime.now().date().isoformat()))
        conn.commit()
    else:
        ask_again = input("sale cannot procced please enter again: ")
        return 
    


while True:
    print("----------inventory------------")
    print("1. add products")
    print("2. view products")
    print("3. search prodcuts")
    print("4. make sale")
    choice = int(input("enter the choice: "))
    if choice == 1:
        add_products()
    elif choice == 2:
        view_products()
    elif choice == 3:
        search_products()
    elif choice == 4:
        make_sale()
        break