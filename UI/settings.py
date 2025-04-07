from fastapi.templating import Jinja2Templates



class Page:

    def __init__(self, templates):

        self.templates = templates

        self.page_ = self.page()


    def page(self):

        return self.templates


new = Page(templates=Jinja2Templates(directory="templates"))


page = new.page()
