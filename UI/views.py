from fastapi import FastAPI, Request
from .settings import page
from fastapi.responses import HTMLResponse

app = FastAPI()


class Create_page:


    @app.get("/login_form", response_class=HTMLResponse)
    async def login(request : Request):

       return page.TemplateResponse("login.html", {"request": request})


