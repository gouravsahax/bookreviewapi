from db.db import base
from sqlalchemy import Integer, String, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

class User(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False, unique=True)

    books = relationship("Book", back_populates="writer", cascade="all")

class Book(base):
    __tablename__ = "book"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, nullable=False)
    review = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    writer = relationship("User", back_populates="books")