from .connection import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_URL = "postgresql://postgres:08012002@localhost:5432/fastapi"

#Se encarga de interactuar con la DDBB
engine = create_engine(SQL_ALCHEMY_URL)

#Se encarga de tener un estado actual de los datos
sessionLocal = sessionmaker(bind=engine, autoflush=False)

base = declarative_base()

def get_db():
    db = sessionLocal() 
    try: 
        yield db
    finally: 
        db.close()

class ProductDao(ConnectDB): 

    def get_products(self): 
        self.cursor.execute("""SELECT * FROM products""")
        products = self.cursor.fetchall()
        return products

    def get_product_by_id(self, id):
        self.cursor.execute(f"""SELECT * FROM products WHERE id = {id}""")
        product = self.cursor.fetchone()
        return dict(product) 

    def add_product(self, product_data): 
        self.cursor.execute("""INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s) RETURNING *""", 
                    (product_data.name , product_data.price, product_data.inventory))
        product = self.cursor.fetchone()
        self.connection.commit()
        return product

    def update_product(self, id, product_data): 
        self.cursor.execute("UPDATE products SET name = %s, price = %s, inventory = %s WHERE id = %s RETURNING *", 
                    (product_data.name, str(product_data.price), product_data.inventory, str(id)))
        product = self.cursor.fetchone()
        self.connection.commit()
        return dict(product)
    
    def delete_product(self, id):
        self.cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(id)))
        product = self.cursor.fetchone()
        self.connection.commit()
        return product


PostgresService = ProductDao()