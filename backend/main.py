from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from database.exceptions import NotFoundException, DatabaseException
from services.exceptions import JWTException


app = FastAPI()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.exception_handler(NotFoundException)
def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={'detail': exc.message})


@app.exception_handler(DatabaseException)
def not_found_handler(request: Request, exc: DatabaseException):
    return JSONResponse(status_code=400, content={'detail': exc.message})


@app.exception_handler(JWTException)
def token_handler(request: Request, exc: JWTException):
    return JSONResponse(status_code=401, content={'detail': exc.message})


# @app.on_event('startup')
# async def startup_event():
#     cluster = await initialize_cluster()
#     ClusterHolder.cluster = cluster
#     await initialize_buckets()
