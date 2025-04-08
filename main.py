
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, delete, update, values
from contextDB.model import Book, User, UserGetBook
from contextDB.settings import settings_db
from fastapi import HTTPException 
from model.bookwebapi_model import Book_DTO, Book_genre
from typing import List
from http import HTTPStatus
from UI.settings import page

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

        async  with settings_db.session() as db:

            create_book = Book(

                title = book.title,

                author = book.author,

                publication_year = book.publication_year,

                genre = book.genre
            )

            db.add(create_book)

            await  db.commit()

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

    # Форма ввода пользователя 
    @app.get("/login", response_class=HTMLResponse)
    async def login_form(request : Request):

       return page.TemplateResponse("login.html", {"request": request})

    @app.post("/login", tags=["Вход пользователя в систему"])
    async def login(request: Request, user_name : str = Form()):


        async with settings_db.session() as db:

            user = await db.execute(select(User).where(User.user_name == user_name))

            get_user_login = user.scalars().first()


            if not get_user_login:

                return page.TemplateResponse("login.html", {"request": request, "error" : "Пользователь не найден"}, status_code=HTTPStatus.BAD_REQUEST)
            
            

            return page.TemplateResponse(
                "welcome.html", 
                {
                    "request": request,
                    "username": user_name
                }
            ) 




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
            

            if get_book.title == title:

                raise HTTPException(status_code=409, detail= "Данная книга на руках у пользователя")
        
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
            

    @app.get("/sort_by_genre/{genre}", tags=["Сортировка по жанру"], response_model=List[Book_genre])
    async def sort_genre(genre : str):

        async with settings_db.session() as db:

            book_genre = await db.execute(
                select(Book).where(Book.genre == genre).order_by(Book.genre))

            sort_book_genge = book_genre.scalars().all()

            if not sort_book_genge:

                raise HTTPException(status_code=404, detail="Книги с таким жанром не найдены")
            
            return sort_book_genge

                
                

           
    @app.post("/update_book/{id}", tags=["Обновление информации о книге"])
    async def update_book(id : int, author: str , title: str, publication_year: int, genre: str):

        async with settings_db.session() as db:

            update_book = await db.execute(
                update(Book)
                .where(Book.id == id)
                .values(author = author, title = title, publication_year = publication_year, genre = genre))
                        
            if not update_book:

                raise HTTPException(status_code=404, detail="Ошибка , данные книги не обновленны")
            

            await db.commit()

            

            return "Запись успешна обновлена"
            








            