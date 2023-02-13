class postgresDAO: 
    def __init__(self, connection, cursor): 
        self.connection = connection
        self.cursor = cursor

    def get_products(self): 
        self.cursor.execute("""SELECT * FROM products""")
        products = self.cursor.fetchall()
        return products

    def get_product_by_id(self, id:int):
        self.cursor.execute(f"""SELECT * FROM products WHERE id = {str(id)}""")
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
                    (product_data.name, product_data.price, product_data.inventory, id))
        product = self.cursor.fetchone()
        self.connection.commit()
        return product
    
    def delete_product(self, id):
        self.cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(id)))
        product = self.cursor.fetchone()
        self.connection.commit()
        return product