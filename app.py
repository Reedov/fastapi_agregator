from fastapi import FastAPI, Depends,Request
from fastapi.middleware.cors import CORSMiddleware
from models.database import create_tables
from api import router
from settings import settings
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import Page, add_pagination, paginate
from services.logger import LogRequestService
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


async def log_request(request: Request, service: LogRequestService = Depends()):
    service.create(client_host=request.client.host,
                   url=request.url.path)


app = FastAPI(debug=True)
app.include_router(router, dependencies=[Depends(log_request)])
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
