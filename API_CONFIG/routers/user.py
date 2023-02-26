from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from ..Models.models import LoginUserSchema
from ..DAO.userDAO import UserService

userRouter = APIRouter(prefix="/user")

@userRouter.get("/")
async def info_about_user(request: Request): 
    user_info = request.state.user
    return {"User_information": user_info}

@userRouter.post("/login")
async def login(auth_Data: LoginUserSchema ,request: Request):
    if request.headers.get("token"): 
        return {"This user is already authenticated"}
    
    try: 
        return UserService.authenticate_user(auth_Data.email, auth_Data.password) 
    except Exception as Error:
        return {"There was an error": f"{Error}"}


@userRouter.post("/signin")
async def signup(): 
    return {"Signup user"}