from db.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from models import Film, User

def error(msg: str, sta):
    raise HTTPException(status_code=sta, detail=msg)

def get_all_films(db, skip: int = 0, limit: int = 10):

    return  [
            { 
                "name":b.name,
                "review":b.review,
                "username":db.query(User).filter(User.id == b.user_id).first().username
            } 
            for b in db.query(Film).offset(skip).limit(limit).all()
            ]

def get_film_by_id(film_id: int, db):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        error("Film not found", status.HTTP_404_NOT_FOUND)
    film.username = db.query(User).filter(User.id == film.user_id).first().username
    return film

def create_film(film_title: str, review: str, user_id: int, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        error("User not found", status.HTTP_404_NOT_FOUND)
    film = Film(name=film_title, review=review, user_id=user_id)
    db.add(film)
    db.commit()
    db.refresh(film)
    film.username = user.username
    return film

def update_film(user_id:int, film_id: int, film_title: str, review: str, db):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        error("Film not found", status.HTTP_404_NOT_FOUND)
    if user_id != film.user_id:
        error("Unauthorized", status.HTTP_401_UNAUTHORIZED)
    film.name = film_title
    film.review = review
    db.commit()
    db.refresh(film)
    user = db.query(User).filter(User.id == film.user_id).first()
    film.username = user.username
    return film

def delete_film(user_id:int, film_id: int, db):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        error("Film not found", status.HTTP_404_NOT_FOUND)

    if int(film.user_id) != int(user_id):
        error("Unauthorized", status.HTTP_401_UNAUTHORIZED)

    db.delete(film)
    db.commit()
    return {"msg": "Film deleted"}
