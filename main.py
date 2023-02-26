import psycopg2
from psycopg2.extras import RealDictCursor

#Interact with the database
from API_CONFIG.DAO.productDAO import ProductDao

from fastapi import FastAPI, status, Body, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from API_CONFIG.Models.models import Product, PostSchema, UserSchema, LoginUserSchema
from API_CONFIG.AUTH.jwt_handler import sign_JWT, decodeJWT
from API_CONFIG.Config.metaConfig import tags_metadata
from API_CONFIG.routers.products import productsRouter
from API_CONFIG.routers.user import userRouter
from API_CONFIG.DAO.productDAO import PostgresService
from API_CONFIG.DAO.userDAO import UserService




home = FastAPI(openapi_tags=tags_metadata)

from API_CONFIG.DAO.productDAO import base, engine

def create_table(): 
    base.metadata.create_all(bind=engine)
create_table()


#Authentication middleware
# @home.middleware("http")
# async def check_auth(request: Request, call_next): 
#     try:
#         user_token = request.headers["token"]
#         decode = decodeJWT(user_token)
#         request.state.user = decode
#         response = await call_next(request)
#         return response
#     except KeyError: 
#         return JSONResponse(content={ 
#             "message":"error"
#         }, status_code=status.HTTP_401_UNAUTHORIZED)
        


#Instalacion de Routers
# home.middleware(check_auth)
home.include_router(productsRouter)
home.include_router(userRouter)

@home.get("/")
async def getproduct(): 
    return {"Hello world"}

    

#List of posts
@home.get("/posts/list", tags=["posts"], status_code=status.HTTP_200_OK)
async def getPosts(): 
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return {"Posts"}

# #LOGIN / SIGN_UP USER
@home.post("/users/signup", tags=["posts"], status_code=status.HTTP_200_OK)
async def signup(user: UserSchema): 
    # cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING *""", 
    #                 ( user.name , user.email, user.password))

    # user = dict(cursor.fetchone())
    # connection.commit()
    # token = sign_JWT(user["name"], user["email"], user["password"])
    try:
        user_registered_token = UserService.register_user(user.name, user.email, user.password)
        return {"Success signup": user_registered_token}
    except Exception as Error: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{Error}")


@home.post("/login")
async def loginUser(userData: LoginUserSchema): 
    user = UserService.get_user_by_email(userData.email)

    if user == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user['password'] != userData.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    token = sign_JWT(user["email"], user["password"])
    return {"Success login": token}





























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