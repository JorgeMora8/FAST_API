from fastapi import FastAPI
import psycopg2

from pydantic import BaseModel


from psycopg2.extras import RealDictCursor

class Product(BaseModel): 
    name : str
    price : int 
    inventory : int 

home = FastAPI()

while True: 
    try: 
        connection = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="08012002", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        break
    except Exception as error: 
        print(error)




@home.get("/")
async def homepage(): 
    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall()
    return products


@home.get("/{id}")
async def getProduct(id:int): 
    cursor.execute("""SELECT * FROM products WHERE id = %s""", (str(id)))
    product = cursor.fetchone()
    return product
    

@home.post("/")
async def addProduct(productData: Product): 
    cursor.execute("""INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s) RETURNING *""", 
                    (productData.name , productData.price, productData.inventory))

    product = cursor.fetchone()
    connection.commit()
    return {"Product_added":product}

@home.put("/{id}")
async def updateProduct(id:int, productData:Product): 
    cursor.execute("UPDATE products SET name = %s, price = %s, inventory = %s WHERE id = %s RETURNING *", 
                    (productData.name, productData.price, productData.inventory, id))
    product = cursor.fetchone()
    connection.commit()
    return {"Product_updated": product}


@home.delete("/{id}")
async def deleteProduct(id:int): 
    cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(id)))
    product = cursor.fetchone()
    connection.commit()
    return {"Product deleted": product}
    