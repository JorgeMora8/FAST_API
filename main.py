import psycopg2

from DAO.postgres import postgresDAO


from fastapi import FastAPI, status, Body
from models import Product, PostSchema, UserSchema, LoginUserSchema
from psycopg2.extras import RealDictCursor
from fastapi.exceptions import HTTPException
from jwt_handler import sign_JWT, decodeJWT
from Config.metaConfig import tags_metadata


home = FastAPI(openapi_tags=tags_metadata)

while True: 
    try: 
        connection = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="08012002", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        PostgresService = postgresDAO(connection, cursor)
        break
    except Exception as error: 
        print(error)

# @home.get("/login")
# async def login(user: UserSchema): 
    # print(user.email)
    # cursor.execute(f"""SELECT * FROM users WHERE email = '{user.email}'""")
    # userFound = cursor.fetchone()
    # if userFound == None: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    # if userFound["password"] != user.password:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    # return userFound
    



@home.get("/decode")
async def update_item(payload: dict = Body(...)):
    token = payload["token"]
    decode = decodeJWT(token)
    print(decode)
    return {"ok"}


@home.get("/", tags=["products"], status_code=status.HTTP_200_OK)
async def homepage():
    return PostgresService.get_products()

@home.get("/{id}", tags=["products"], status_code=status.HTTP_200_OK)
async def getProduct(id:int): 
      return PostgresService.get_product_by_id(id)
    

@home.post("/", tags=["products"], status_code=status.HTTP_201_CREATED)
async def addProduct(productData: Product): 
        return PostgresService.add_product(productData)

@home.put("/{id}", tags=["products"], status_code=status.HTTP_201_CREATED)
async def updateProduct(id:int, productData:Product): 
    return PostgresService.update_product(id, productData)


@home.delete("/{id}", tags=["products"], status_code=status.HTTP_204_NO_CONTENT)
async def deleteProduct(id:int): 
    return PostgresService.delete_product(id)
    

@home.get("/posts/list", tags=["posts"], status_code=status.HTTP_200_OK)
async def getPosts(): 
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"Posts": posts}






#LOGIN / SIGN_UP USER

@home.post("/users/signup", tags=["posts"], status_code=status.HTTP_200_OK)
async def signup(user: UserSchema): 
    cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING *""", 
                    ( user.name , user.email, user.password))

    user = dict(cursor.fetchone())
    connection.commit()
    # print(user["password"])
    token = sign_JWT(user["name"], user["email"], user["password"])
    return {"User added succesfully": token}




