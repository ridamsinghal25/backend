from pydantic import Field, BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    email: EmailStr
    clerk_id: str
    name: str
