import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as router_auth
from app.routes.user import router as router_user
from app import parameters

# uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

if parameters.APP_MODE == parameters.APP_MODE_DEV:

    logging.basicConfig(level=logging.DEBUG)

else:

    logging.basicConfig(level=logging.WARNING)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_auth)
app.include_router(router=router_user)
