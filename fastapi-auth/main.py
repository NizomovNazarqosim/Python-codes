from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import orm


import models
import database
import schemas
from services import user_services


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  ----------User-------
# create_user
@app.post('/user/create')
async def user_create(user: schemas.UserCreate, db: orm.Session = Depends(get_db)):
    result = await user_services.create(user, db)
    return result

@app.post('/user/login')
async def user_login(user: schemas.UserLogin, db: orm.Session = Depends(get_db)):
    result = await user_services.login(user, db)
    return result

@app.post('/user/data')
async def get_user(token:schemas.Token, db: orm.Session = Depends(get_db)):
    result = await user_services.get_user_info(token, db)
    return result

@app.put('/user/update')
async def update_user_by_token(user:schemas.UserUpdate, token:schemas.Token,db : orm.Session = Depends(get_db)):
    result = await user_services.update_user(user=user, token=token, db=db)
    return result

@app.delete('/user/delete')
async def delete_user_by_token(token:schemas.Token,db : orm.Session = Depends(get_db)):
    result = await user_services.delete_user(token=token, db=db)
    return result

