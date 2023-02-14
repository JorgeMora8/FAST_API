# from fastapi import APIRouter
# from ..

# userRouter = APIRouter()

# #LOGIN / SIGN_UP USER
# @userRouter.post("/users/signup", tags=["posts"], status_code=status.HTTP_200_OK)
# async def signup(user: UserSchema): 
#     cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING *""", 
#                     ( user.name , user.email, user.password))

#     user = dict(cursor.fetchone())
#     connection.commit()
#     # print(user["password"])
#     token = sign_JWT(user["name"], user["email"], user["password"])
#     return {"User added succesfully": token}