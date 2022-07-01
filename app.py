from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import create_tables
from api import router
from settings import settings
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import Page, add_pagination, paginate
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s [%(funcName)s:%(lineno)s] %(message)s', level=logging.INFO)


def init_cors(_app: FastAPI) -> None:
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = FastAPI(debug=True)
app.include_router(router)
init_cors(_app=app)

app.mount("/static", StaticFiles(directory="static"), name="static")
add_pagination(app)


# @app.on_event("startup")
def on_startup():
    print("on_startup..")
    create_tables()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host=settings.server_host, port=settings.server_port)
