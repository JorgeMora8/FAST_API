from .connection import *
from ..AUTH.jwt_handler import *

class UserDAO(ConnectDB): 

    def get_user_by_email(self, email): 
        self.cursor.execute("""SELECT * FROM users WHERE email = '{0}'""".format(email)  )
        users = self.cursor.fetchone()
        if users == None: 
            return None
        return dict(users)

    def register_user(self, name, email, password): 

        user_searched = self.get_user_by_email(email)
        
        if user_searched is not None: 
            raise Exception("This email is already in use... choose other email.")
        
        else:
            cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING *""", 
                    ( name, email, password ))

            user = cursor.fetchone()
            connection.commit()
            token = sign_JWT(email, password)
            return token

    def authenticate_user(self, email, password): 
        user_searched = self.get_user_by_email(email)
        
        if user_searched is not None: 
            raise Exception("User not found")

        if user_searched.password != password: 
            raise Exception("Incorrect password")

        new_token = sign_JWT(email, password)
        return new_token
        

UserService = UserDAO()