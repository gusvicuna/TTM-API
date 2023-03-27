from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from TTMAPI.routes.driver import router


app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:4200/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)
