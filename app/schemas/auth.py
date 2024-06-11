from pydantic import BaseModel, EmailStr

class ResetPassword(BaseModel):

    operating_system : str
    browser_name : str
    email: EmailStr
