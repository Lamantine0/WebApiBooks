from fastapi import FastAPI, Request, APIRouter
from .settings import page
from fastapi.responses import HTMLResponse

app = FastAPI()



class Create_page:


    @app.get("/login", response_class=HTMLResponse)
    async def login_form(request : Request):

       return page.TemplateResponse("login.html", {"request": request})


