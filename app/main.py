from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
import uvicorn

from database import create_tables, delete_tables
from router import process_router, info_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print("Previous tables has been dropped")
    await create_tables()
    print("Tables has been recreated")
    yield
    print("Application is down")


description = """Lorem ipsum dolor sit amet. Quo culpa consequatur aut harum ratione sed itaque laudantium. Aut labore labore ut dolore praesentium aut adipisci eius ex nemo perferendis nam molestias sint. Et magnam incidunt sit totam magnam id voluptatibus ipsa est incidunt ipsam in necessitatibus culpa eos harum voluptate? Est maiores perspiciatis ea galisum doloribus et aliquid totam et consequatur laborum."""

app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    title="Микро-сервис по отслеживанию процессов",
    description=description,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(process_router)
app.include_router(info_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=6001)
