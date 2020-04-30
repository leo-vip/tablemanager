import json

import uvicorn
from fastapi import FastAPI, status

from starlette.requests import Request
from starlette.responses import Response
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


@app.get("/column_data")
def column_data(column, value, table_name):
    return table_service.query_data_by_id(column, value, table_name)


@app.get("/column_update")
def column_data(name=None, value=None, table_name=None, columns=None):

    table_service.update_column(name, value, table_name, json.loads(columns))
    return "SUCCESS"
    # return table_service.query_data_by_id(column, value, table_name)


@app.get('/data')
def data(response: Response, table_name=None, page: int = 1, limit: int = 50, where: str = None):
    try:
        if table_name is None or len(table_name) == 0:
            tables = table_service.list_tables()
            items = []
            for table in tables:
                item = table_service.show_table_column(table)
                item.insert(0, table)
                items.append(item)
            return {"count": len(tables), "items": items}
        if page < 1:
            raise Exception('page must >1')
        if table_name is None:
            return []

        result = table_service.sql_page(table_name, page, limit, where)

        return {"count": table_service.count(table_name), "PK": table_service.getPK(table_name), "items": result}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'errors': f"{e}"}


if __name__ == '__main__':
    print("main start ----------------")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8081, reload=True, debug=True)
