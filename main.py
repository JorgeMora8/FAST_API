import psycopg2
from psycopg2.extras import RealDictCursor

#Interact with the database
from DAO.postgres import postgresDAO

from fastapi import FastAPI, status, Body, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from models import Product, PostSchema, UserSchema, LoginUserSchema
from AUTH.jwt_handler import sign_JWT, decodeJWT
from Config.metaConfig import tags_metadata
from routers.products import productsRouter

#Fast API endpoint
home = FastAPI(openapi_tags=tags_metadata)


#Connection
while True: 
    try: 
        #todo: Change the string for .env variables
        connection = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="08012002", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        PostgresService = postgresDAO(connection, cursor)
        break
    except Exception as error: 
        print(error)


#Authentication middleware
@home.middleware("http")
async def check_auth(request: Request, call_next): 
    try:
        user_token = request.headers["token"]
        decode = decodeJWT(user_token)
        request.state.user = decode
        response = await call_next(request)
        return response
    except KeyError: 
        return JSONResponse(content={ 
            "message":"error"
        }, status_code=status.HTTP_401_UNAUTHORIZED)
        

#Instalacion de Routers
@home.include_router(productsRouter)
    

#List of posts
@home.get("/posts/list", tags=["posts"], status_code=status.HTTP_200_OK)
async def getPosts(): 
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"Posts": posts}

# #LOGIN / SIGN_UP USER
@home.post("/users/signup", tags=["posts"], status_code=status.HTTP_200_OK)
async def signup(user: UserSchema): 
    cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING *""", 
                    ( user.name , user.email, user.password))

    user = dict(cursor.fetchone())
    connection.commit()
    token = sign_JWT(user["name"], user["email"], user["password"])
    return {"User added succesfully": token}































# @home.get("/decode")
# async def update_item(payload: dict = Body(...)):
#     token = payload["token"]
#     decode = decodeJWT(token)
#     print(decode)
#     return {"ok"}


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