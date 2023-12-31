import database as _database
import models as _models
import sqlalchemy.orm as _orm
import schemas as _schemas
import jwt as _jwt

import email_validator as _email_check
import fastapi as _fastapi
import passlib.hash as _hash

_JWT_SECRET = "thisisnotverysafe"

def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
async def get_user_by_email(email:str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    # check email is valid
    try:
        valid = _email_check.validate_email(email=user.email)
        email = valid.email
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(status_code=404, detail="Please enter valid email")
    
    hashed_password = _hash.bcrypt.hash(user.password)
    user_obj = _models.User(email=email, hashed_password=hashed_password, name=user.name)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: _models.User):
    user_schema_obj = _schemas.User.from_orm(user)
    
    user_dict = user_schema_obj.dict()
    del user_dict['date_created']
    
    token = _jwt.encode(user_dict, _JWT_SECRET)
    
    return dict(access_token=token, token_type='bearer')

