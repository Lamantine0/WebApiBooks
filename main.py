
from fastapi import FastAPI
from sqlalchemy import select, delete
from contextDB.model import Book, User, UserGetBook
from contextDB.settings import settings_db
from fastapi import HTTPException
from model.bookwebapi_model import Book_DTO


app = FastAPI()


class BooksWebApi:
                
    @app.post("/create_book/", tags=["Создание книги"])
    async def create_book(
        title : str,
        author: str,
        publication_year: int,
        genre : str
):
        
       async with settings_db.session() as db:

            create_book = Book(
                title = title,
                author = author,
                publication_year = publication_year,
                genre = genre
            )

            if not create_book:

                raise HTTPException(status_code=404, detail="Книга не создана")



            db.add(create_book)

            await  db.commit()

            await db.refresh(create_book)
            
            return {"Книга добавлена" : create_book.title}

    @app.post("/create_book_DTO/", tags=["Создание книги c DTO"])
    async def create_book(book : Book_DTO):

        with settings_db.session() as db:

            create_book = Book(

                title = book.title,

                author = book.author,

                publication_year = book.publication_year,

                genre = book.genre
            )

            db.add(create_book)

            db.commit()

            return {
                "title": create_book.title,
                "author": create_book.author,
                "publication_year": create_book.publication_year,
                "genre": create_book.genre
            }



    @app.get("/get_all_books/", tags=["получение списка книг в библиотеке"])
    async def get_all_books():

        async with settings_db.session() as db:

            get_books = await db.execute(select(Book))

            books = get_books.scalars().all()

            if not books:

                raise HTTPException(status_code=404, detail="Список книг не найден")


            return books  

            

    @app.post("/create_user/", tags=["Создание Юзера"])
    async def create_user(user_name: str):

       async with settings_db.session() as db:

            new_user =  User(
            
              user_name = user_name
            )

            if not new_user:

                raise HTTPException(status_code=404, detail="Пользователь не создан")
            
            db.add(new_user)

            await db.commit()

            await db.refresh(new_user)

            return {
                "ID" : new_user.id,
                "Пользователь" : new_user.user_name
            }            

    @app.post("/get_book_library/", tags=["Получение книги в библиотеке"])
    async def take_book(user_name : str , title : str):


       async with settings_db.session() as db:
            


            user = await db.execute(select(User).where(User.user_name == user_name, User.id == User.id))

            get_user = user.scalars().first()

            if not get_user:

                raise HTTPException(status_code=404, detail= "пользователь не найден")

            book = await db.execute(select(Book).where(Book.title == title, Book.id == Book.id))

            get_book = book.scalars().first()

            if not get_book:

                raise HTTPException(status_code=404, detail="Книга не найдена")
            


            if get_book == title:

                raise HTTPException(status_code=404 , detail="Книга уже взята")


            user_get_book = UserGetBook(title=title, user_name=user_name, user_id=get_user.id, book_id=get_book.id)

            db.add(user_get_book)

            await db.commit()

            await db.refresh(user_get_book)

            

            return {"message": "Книга успешно взята", "title": title, "user_name": user_name}
            


    @app.delete("/delete_book/{id}", tags=["Удаление книги из БД"])
    async def delete_book_by_id(id: int):

        async with settings_db.session() as db:

            book = await db.execute(select(Book).where(Book.id == id))

            get_book = book.scalars().first()

            if not get_book:

                raise HTTPException(status_code=404, detail="ID не найдено")
            
            await db.execute(delete(Book).where(Book.id == id))

            await db.commit()

            return {
                "Книга удалена ID " : get_book.id
            }
            

