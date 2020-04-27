import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from service.tableservice import TableService

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/")
def index(request: Request):
    tables = table_service.list_tables()
    return templates.TemplateResponse('index.html', {"request": request, 'tables': tables})


table_service = TableService()


@app.get('/data')
def data(table_name, page: int = 1, limit: int = 50):
    if page < 1:
        raise Exception('page must >1')
    if table_name is None:
        return []
    result = table_service.sql_page(table_name, page, limit)

    return {"count": table_service.count(table_name), "items": result}


if __name__ == '__main__':
    print("main start ----------------")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8081, reload=True, debug=True)
