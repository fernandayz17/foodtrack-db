import pyodbc
import pandas as pd
import os

server = 'localhost\\SQLEXPRESS'
database = 'FoodTrack'
connection_string_master = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes;'
connection_string_foodtrack = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=FoodTrack;Trusted_Connection=yes;'



def crear_database():
    print("Creando base de datos...")
    conn = pyodbc.connect(connection_string_master, autocommit=True)
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'FoodTrack')
        BEGIN
            CREATE DATABASE FoodTrack
        END
    """)
    cursor.close()
    conn.close()
    print("✅ Base de datos creada")

def crear_tablas():
    print("Creando tablas...")
    conn = pyodbc.connect(connection_string_foodtrack)
    cursor = conn.cursor()

    # Eliminar tablas en orden de dependencias
    cursor.execute("IF OBJECT_ID('order_items', 'U') IS NOT NULL DROP TABLE order_items;")
    cursor.execute("IF OBJECT_ID('locations', 'U') IS NOT NULL DROP TABLE locations;")
    cursor.execute("IF OBJECT_ID('orders', 'U') IS NOT NULL DROP TABLE orders;")
    cursor.execute("IF OBJECT_ID('products', 'U') IS NOT NULL DROP TABLE products;")
    cursor.execute("IF OBJECT_ID('foodtrucks', 'U') IS NOT NULL DROP TABLE foodtrucks;")

    # Foodtrucks
    cursor.execute("""
    CREATE TABLE foodtrucks (
        foodtruck_id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        cuisine_type VARCHAR(50),
        city VARCHAR(50)
    )""")

    # Products
    cursor.execute("""
    CREATE TABLE products (
        product_id INT IDENTITY(1,1) PRIMARY KEY,
        foodtruck_id INT,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2),
        stock INT,
        FOREIGN KEY (foodtruck_id) REFERENCES foodtrucks(foodtruck_id)
    )""")

    # Orders
    cursor.execute("""
    CREATE TABLE orders (
        order_id INT PRIMARY KEY,
        foodtruck_id INT,
        order_date DATETIME,
        status VARCHAR(20),
        total DECIMAL(10,2),
        FOREIGN KEY (foodtruck_id) REFERENCES foodtrucks(foodtruck_id)
    )""")

    # Locations
    cursor.execute("""
    CREATE TABLE locations (
        location_id INT IDENTITY(1,1) PRIMARY KEY,
        foodtruck_id INT,
        location_date DATE,
        zone VARCHAR(50),
        FOREIGN KEY (foodtruck_id) REFERENCES foodtrucks(foodtruck_id)
    )""")

    # Order_items
    cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INT IDENTITY(1,1) PRIMARY KEY,
        order_id INT,
        product_id INT,
        quantity INT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )""")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tablas creadas")

def limpiar_datos():
    print("Limpiando datos...")
    
    # Leer CSVs
    df_products = pd.read_csv('data/products.csv')
    df_order_items = pd.read_csv('data/order_items.csv')
    df_orders = pd.read_csv('data/orders.csv')
    
    # IDs válidos
    valid_product_ids = set(df_products['product_id'])
    valid_order_ids = set(df_orders['order_id'])
    
    # Filtrar order_items
    df_order_items_clean = df_order_items[
        (df_order_items['product_id'].isin(valid_product_ids)) & 
        (df_order_items['order_id'].isin(valid_order_ids))
    ]
    
    # Guardar CSV limpio
    df_order_items_clean.to_csv('data/order_items_clean.csv', index=False)
    print("✅ Datos limpiados")

def cargar_datos():
    print("Cargando datos...")
    conn = pyodbc.connect(connection_string_foodtrack)
    cursor = conn.cursor()

    # Cargar cada CSV
    df_foodtrucks = pd.read_csv('data/foodtrucks.csv')
    df_products = pd.read_csv('data/products.csv')
    df_orders = pd.read_csv('data/orders.csv')
    df_locations = pd.read_csv('data/locations.csv')
    df_order_items = pd.read_csv('data/order_items_clean.csv')  # <-- usar el limpio


    # Insertar datos con manejo de errores y mensajes
    try:
        for _, row in df_foodtrucks.iterrows():
            cursor.execute("INSERT INTO foodtrucks (name, cuisine_type, city) VALUES (?, ?, ?)",
                           str(row['name']), str(row['cuisine_type']), str(row['city']))
        print("✔️ Foodtrucks insertados correctamente")
    except Exception as e:
        print(f"❌ Error insertando foodtrucks: {e}")

    try:
        for _, row in df_products.iterrows():
            cursor.execute("INSERT INTO products (foodtruck_id, name, price, stock) VALUES (?, ?, ?, ?)",
                           int(row['foodtruck_id']), str(row['name']), float(row['price']), int(row['stock']))
        print("✔️ Products insertados correctamente")
    except Exception as e:
        print(f"❌ Error insertando products: {e}")

    try:
        for _, row in df_orders.iterrows():
            cursor.execute("INSERT INTO orders (order_id, foodtruck_id, order_date, status, total) VALUES (?, ?, ?, ?, ?)",
                           int(row['order_id']), int(row['foodtruck_id']), str(row['order_date']), str(row['status']), float(row['total']))
        print("✔️ Orders insertados correctamente")
    except Exception as e:
        print(f"❌ Error insertando orders: {e}")

    try:
        for _, row in df_locations.iterrows():
            cursor.execute("INSERT INTO locations (foodtruck_id, location_date, zone) VALUES (?, ?, ?)",
                           int(row['foodtruck_id']), str(row['location_date']), str(row['zone']))
        print("✔️ Locations insertados correctamente")
    except Exception as e:
        print(f"❌ Error insertando locations: {e}")

    try:
        for _, row in df_order_items.iterrows():
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                           int(row['order_id']), int(row['product_id']), int(row['quantity']))
        print("✔️ Order_items insertados correctamente")
    except Exception as e:
        print(f"❌ Error insertando order_items: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Datos cargados")

if __name__ == "__main__":
    limpiar_datos()
    crear_database()
    crear_tablas() 
    cargar_datos()
    print("🎉 ¡COMPLETADO!")