from db.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from models import Book, User

def error(msg: str, sta):
    raise HTTPException(status_code=sta, detail=msg)

def get_all_books(db, skip: int = 0, limit: int = 10):

    return  [
            { 
                "name":b.name,
                "review":b.review,
                "username":db.query(User).filter(User.id == b.user_id).first().username
            } 
            for b in db.query(Book).offset(skip).limit(limit).all()
            ]

def get_book_by_id(book_id: int, db):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        error("Book not found", status.HTTP_404_NOT_FOUND)
    book.username = db.query(User).filter(User.id == book.user_id).first().username
    return book

def create_book(book_title: str, review: str, user_id: int, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        error("User not found", status.HTTP_404_NOT_FOUND)
    book = Book(name=book_title, review=review, user_id=user_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    book.username = user.username
    return book

def update_book(user_id:int, book_id: int, book_title: str, review: str, db):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        error("Book not found", status.HTTP_404_NOT_FOUND)
    if user_id != book.user_id:
        error("Unauthorized", status.HTTP_401_UNAUTHORIZED)
    book.name = book_title
    book.review = review
    db.commit()
    db.refresh(book)
    user = db.query(User).filter(User.id == book.user_id).first()
    book.username = user.username
    return book

def delete_book(user_id:int, book_id: int, db):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        error("Book not found", status.HTTP_404_NOT_FOUND)

    if int(book.user_id) != int(user_id):
        error("Unauthorized", status.HTTP_401_UNAUTHORIZED)

    db.delete(book)
    db.commit()
    return {"msg": "Book deleted"}
