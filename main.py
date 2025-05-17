from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, crud
from database import Base, engine
from auth import authenticate_user, create_access_token, get_current_user, get_db, create_email_verification_token, verify_email_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from admin import setup_admin
from utils import send_verification_email


app = FastAPI()
Base.metadata.create_all(bind=engine)

setup_admin(app) 

@app.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    new_user = crud.create_user(db, user)

    token = create_email_verification_token(new_user.email)
    await send_verification_email(new_user.email, token)

    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Неверный или просроченный токен")
    
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.is_email_verified = True
    db.commit()
    return {"message": "Email успешно подтверждён"}
