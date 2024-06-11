from pydantic import BaseModel, EmailStr

class NewUser(BaseModel):

    username: str
    password_user: str
    email: EmailStr
