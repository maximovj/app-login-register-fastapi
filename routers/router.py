from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schemas.user_schema import UserSchema, DataUser
from config.db import engine
from models.users import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

user = APIRouter()

@user.get("/")
def root():
    return {"message": "OK 200"}

@user.get("/api/user", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        return conn.execute(users.select()).mappings().all()

@user.get("/api/user/{user_id}", response_model=UserSchema)
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result 

@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.model_dump()
        print(data_user)
        print(new_user)
        
        new_user["password"] = generate_password_hash(data_user.password, "pbkdf2:sha256:30", 30)
        print(new_user)
        
        conn.execute(users.insert().values(new_user))
        conn.commit()
        return Response(status_code=HTTP_201_CREATED)
    
@user.post("/api/user/login", status_code=200)
def login_user(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        if result != None:
            check_password = check_password_hash(result[3], data_user.password)
            if check_password:
                return {"status": 200, "message": "Acceso exitosa"}
        return {"status": 410, "message": "Acceso no autorizado"}           

@user.put("/api/user/{user_id}", response_model=UserSchema)
def update_user(user_id: int, data_update: UserSchema):
    with engine.connect() as conn:
        print(user_id)
        print(data_update)
        
        encrypt_password = generate_password_hash(data_update.password, "pbkdf2:sha256:30", 30)
        
        conn.execute(users.update()
            .values(
            name = data_update.name, 
            username = data_update.username, 
            password = encrypt_password)
            .where(users.c.id == user_id)
        )
        conn.commit()
        
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result
    
@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))
        return Response(status_code=HTTP_204_NO_CONTENT)
