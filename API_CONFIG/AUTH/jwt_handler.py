import jwt
import time
from decouple import config


#jwt secret
JWT_SECRET = config("SECRET")

#jwt algorith
JWT_ALGORITH = config("ALGORITHM")


#Function that will return tokens

def token_response(token:str): 
    return { 
        "access_token":token
    }

def sign_JWT( email:str, password:int): 
    payload = { 
        "email":email, 
        "password":password, 
        "expiry": time.time() + 600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITH)
    return token

def decodeJWT(token: str):
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITH])
        return decoded_token

