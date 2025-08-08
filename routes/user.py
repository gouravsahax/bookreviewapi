from fastapi import APIRouter, Depends, HTTPException
from crud.user import get_all_user, get_user_by_id, get_user_by_email, create_user, update_user_password, delete_user, all_books_by_user
from schemas import UserReturn, BookReturn
from typing import List
from sqlalchemy.orm import Session
from db.db import get_db
from core.security import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/all", response_model=List[UserReturn])
def get_all_user_route(db:Session=Depends(get_db)):
    return get_all_user(db)

@router.get("/getOne", response_model=UserReturn)
def get_user_by_email_route(email: str, db: Session = Depends(get_db)):
    return get_user_by_email(email, db)

@router.get("/getAllBook", response_model=List[BookReturn])
def get_user_books_route(id: int, db: Session = Depends(get_db)):
    return all_books_by_user(user_id=id, db=db)

@router.get("/{id}", response_model=UserReturn)
def get_user_by_id_route(id: int, db: Session = Depends(get_db)):
    return get_user_by_id(id, db)

@router.post("/create", response_model=UserReturn)
def create_user_route(username:str, email:str, password:str, db:Session=Depends(get_db)):
    return create_user(username, email, password, db)

@router.put("/update", response_model=UserReturn)
def update_user_route(old_pass:str, new_pass:str, curr_user:UserReturn = Depends(get_current_user), db:Session=Depends(get_db)):
    return update_user_password(curr_user.id, old_pass, new_pass, db)

@router.delete("/delete")
def delete_user_route(password:str, curr_user:UserReturn = Depends(get_current_user), db:Session=Depends(get_db)):
    return delete_user(curr_user.id, password, db)