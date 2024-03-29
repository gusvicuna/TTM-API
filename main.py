from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from TTMAPI.jobs.create_descriptions_job import create_descriptions

from TTMAPI.jobs.process_answers_job import process_answers
from TTMAPI.routes.driver import router as driver_router
from TTMAPI.routes.process import router as process_router
from TTMAPI.routes.survey import router as survey_router
from TTMAPI.routes.prompt import router as prompt_router


app = FastAPI()

app.include_router(driver_router, prefix="/drivers")
app.include_router(process_router, prefix="/process")
app.include_router(survey_router, prefix='/surveys')
app.include_router(prompt_router, prefix='/prompt')

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

start_jobs = True
scheduler = BackgroundScheduler()
if start_jobs:
    scheduler.add_job(process_answers, trigger="interval", seconds=30)
    scheduler.add_job(create_descriptions, trigger="interval", seconds=300)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
