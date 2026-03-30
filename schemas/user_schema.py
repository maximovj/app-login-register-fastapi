from pydantic import BaseModel
from typing import Optional 

class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    password: str
    
class DataUser(BaseModel):
    username: str
    password: str