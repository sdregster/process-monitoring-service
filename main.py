from contextlib import asynccontextmanager

from fastapi import FastAPI
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


app = FastAPI(lifespan=lifespan)
app.include_router(process_router)
app.include_router(info_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8080)
