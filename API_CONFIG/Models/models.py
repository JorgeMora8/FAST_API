from pydantic import BaseModel, EmailStr, Field


class PostSchema(BaseModel) : 
    id: int = Field(default=None)
    title: str = Field(default=None)
    message: str = Field(default=None)

    class Config: 
        schema_extra = { 
            "post_demo":{
                "title": "Title about something", 
                "content":"Content about something"
            }
        }


class UserSchema(BaseModel): 
    name : str
    email : str
    password : str 


class LoginUserSchema(BaseModel): 
    email : str
    password : str


class Product(BaseModel): 
    # id : str
    name : str
    price : int 
    inventory : int 

from ..DAO.productDAO import base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Product_SQL(base): 
    __tablename__ = "Product_SA"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(Integer) 
    inventory = Column(Integer)
