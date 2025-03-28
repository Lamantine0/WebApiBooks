from contextDB.settings import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi import FastAPI


app = FastAPI()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_name = Column(String, nullable=False)

    books = relationship("Book", back_populates='user')

    get_books = relationship("UserGetBook" , back_populates = "user")



class Book(Base):

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)

    author = Column(String, nullable=False)

    publication_year = Column(Integer)

    genre = Column(String)

    user_id = Column(Integer, ForeignKey('users.id')) 

    user = relationship("User", back_populates='books')

    
    

class UserGetBook(Base):

    __tablename__ = 'user_get_book'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)

    user_name = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))  # Добавляем внешний ключ

    user = relationship("User", back_populates='get_books')
      # Связь с User
    book_id = Column(Integer, ForeignKey('books.id'))  # Добавляем внешний ключ для связи с Book
     
    book = relationship("Book")  # Связь с Book

    

    



            



        