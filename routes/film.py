from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db import get_db
from crud.film import (
    get_all_films, get_film_by_id,
    create_film, update_film, delete_film
)
from schemas import FilmReturn, UserReturn
from core.security import get_current_user

router = APIRouter(
    prefix="/film",
    tags=["Films"]
)

@router.get("/all", response_model=list[FilmReturn])
def all_films_route(db: Session = Depends(get_db)):
    films = get_all_films(db)
    return films

@router.get("/{id}", response_model=FilmReturn)
def get_film_by_id_route(id: int, db: Session = Depends(get_db)):
    film = get_film_by_id(id, db)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@router.post("/create", response_model=FilmReturn, status_code=status.HTTP_201_CREATED)
def create_film_route(film_title: str, review: str, curr_user:UserReturn = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_film(film_title, review, curr_user.id, db)

@router.put("/{id}", response_model=FilmReturn)
def update_film_route(film_id:int, film_title: str, review: str, curr_user:UserReturn = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_film = update_film(curr_user.id, film_id, film_title, review, db)
    if not updated_film:
        raise HTTPException(status_code=404, detail="Film not found")
    return updated_film

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_film_route(id:int, curr_user:UserReturn = Depends(get_current_user), db: Session = Depends(get_db)):
    success = delete_film(curr_user.id, id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Film not found")
    return success
