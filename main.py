from fastapi import FastAPI

from TTMAPI.routes.driver import router


app = FastAPI()
app.include_router(router)
