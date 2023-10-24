import email_validator
import jwt
from fastapi import HTTPException
from passlib import hash
from sqlalchemy import orm
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

import database
import schemas
import json
import models

_JWT_SECRET = "thisisnotverysafe"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# create token
async def create_token(user: models.User):
    user_obj = schemas.UserCreate.from_orm(user)
    user_dict = user_obj.dict()
    
    token = jwt.encode(user_dict, _JWT_SECRET, algorithm='HS256')
    
    return dict(access_token=token, token_type='bearer')

# verify token
async def verify_token(token):
    verifyed = jwt.decode(token, _JWT_SECRET, algorithms=['HS256'])
    return verifyed

# Email checking function
async def check_email(email:str):
    try:
        valid = email_validator.validate_email(email=email)
        return valid.email
    except email_validator.EmailNotValidError:
        raise HTTPException(status_code=400, detail="Please enter valid email")
        
#  hash password function
async def hash_function(password:str):
    hashed_password = hash.bcrypt.hash(password)
    return hashed_password

# get user by email
async def get_user_by_email(email:str, db: orm.Session):
    user =  db.query(models.User).filter(models.User.email==email).first()
    return user
# password match
async def password_match(password: str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)

        
# create user
async def create(user: schemas.UserCreate, db: orm.Session):
    valid_email = await check_email(user.email)
    if not valid_email:
        raise HTTPException(status_code=400, detail="Please enter valid email")
    
    email = await get_user_by_email(user.email, db)
    if email:
        raise HTTPException(status_code=400, detail="You are already exists")
    hashed_password = await hash_function(user.password)
    user_obj = models.User(email=user.email, name=user.name, password=hashed_password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    result = await create_token(user_obj)
    return result
    
    
# login by email and password
async def login(user: schemas.UserLogin, db: orm.Session):
    valid_email = await check_email(user.email)
    if not valid_email:
        raise HTTPException(status_code=400, detail="Please enter valid email")
    data = await get_user_by_email(user.email, db)
    if data == None:
        raise HTTPException(status_code=401, detail="You are not registered yet")
    
    is_password = await password_match(user.password, data.password)
    if is_password:
        result = await create_token(data)
        return result   
    else: 
        raise HTTPException(status_code=401, detail="Password error")
        
    
        
# get user data by token
async def get_user_info(token:schemas.Token, db: orm.Session):
    verifyed = await verify_token(token.token)
    return verifyed

# update user by token
async def update_user(user:schemas.UserUpdate, token:schemas.Token, db:orm.Session):
    verifyed = await verify_token(token.token)
    update_user = db.query(models.User).filter(models.User.email == verifyed['email'])
    update_user.first()   
    if update_user == None:
        raise HTTException(status_code=status.HTT_NOT_FOUND, detail='user does not exist')
    if user.password:
        hashed_password = await hash_function(user.password)
        del user.password 
        user.password = hashed_password
    update_user.update(user.dict(), synchronize_session=False)
    db.commit()
    return update_user.first()

        
    valid_email = await check_email(user.email)
    if not valid_email:
        raise HTTPException(status_code=400, detail="Please enter valid email")
    
async def delete_user(token: schemas.Token, db:orm.Session):
    verifyed = await verify_token(token.token)
    is_have = db.query(models.User).filter(models.User.email == verifyed['email'])
    is_have.first()   
    if is_have == None:
        raise HTTException(status_code=status.HTT_NOT_FOUND, detail='user does not exist')
    # delete_user = db.query(models.User).filter(models.User.email == verifyed['email']).delete()
    is_have.delete()
    db.commit()   
    return JSONResponse(content='User deleted successfully')
    