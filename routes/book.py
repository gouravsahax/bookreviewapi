from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db import get_db
from crud.book import (
    get_all_books, get_book_by_id,
    create_book, update_book, delete_book
)
from schemas import BookReturn, UserReturn
from core.security import get_current_user

router = APIRouter(
    prefix="/book",
    tags=["Books"]
)

@router.get("/all", response_model=list[BookReturn])
def all_books_route(db: Session = Depends(get_db)):
    books = get_all_books(db)
    return books

@router.get("/{id}", response_model=BookReturn)
def get_book_by_id_route(id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/create", response_model=BookReturn, status_code=status.HTTP_201_CREATED)
def create_book_route(book_title: str, review: str, curr_user:UserReturn = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_book(book_title, review, curr_user.id, db)

@router.put("/{id}", response_model=BookReturn)
def update_book_route(book_id:int, book_title: str, review: str, curr_user:UserReturn = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_book = update_book(curr_user.id, book_id, book_title, review, db)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_route(id:int, curr_user:UserReturn = Depends(get_current_user), db: Session = Depends(get_db)):
    success = delete_book(curr_user.id, id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return success
