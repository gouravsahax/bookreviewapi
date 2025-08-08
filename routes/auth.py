from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.db import get_db
from crud.user import get_user_by_email
from models import User
from core.security import verify_password, create_access_token, get_current_user
from schemas import UserReturn

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me", response_model=UserReturn)
def current_user(curr_user:UserReturn = Depends(get_current_user)):
    return curr_user

@router.post("/token")
def login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email==form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}