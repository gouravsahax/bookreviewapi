from fastapi import HTTPException, status, HTTPException, status
from models import User
from core.security import hash_password, verify_password

def error(msg: str, sta):
    raise HTTPException(status_code=sta, detail=msg)

def get_all_user(db, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_email(email: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        error("No User Found", status.HTTP_404_NOT_FOUND)
    return user

def get_user_by_id(id: int, db):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        error("No User Found", status.HTTP_404_NOT_FOUND)
    return user

def create_user(username:str, email: str, password: str, db):
    if db.query(User).filter(User.email == email).first():
        error("User Already Exists", status.HTTP_409_CONFLICT)
    hashed_pw = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_password(id: int, current_password: str, new_password: str, db):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        error("No User Found", status.HTTP_404_NOT_FOUND)
    if not verify_password(current_password, user.hashed_password):
        error("Unauthorized", status.HTTP_401_UNAUTHORIZED)
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(id: int, password: str, db):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        error("No User Found", status.HTTP_404_NOT_FOUND)
    if not verify_password(password, user.hashed_password):
        error("Unauthorized", status.HTTP_401_UNAUTHORIZED)
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}

def all_films_by_user(user_id: int, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        error("User not found", status.HTTP_404_NOT_FOUND)

    return [
        {
            "name": film.name,
            "review": film.review,
            "username": user.username
        }
        for film in user.films
    ]