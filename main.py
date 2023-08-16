from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from TTMAPI.routes.driver import router as driver_router
from TTMAPI.routes.process import router as process_router


app = FastAPI()
app.include_router(driver_router, prefix="/drivers")
app.include_router(process_router, prefix="/process")

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
