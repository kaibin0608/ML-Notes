from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.base import JobLookupError
from datetime import datetime
import time

DATABASE_URL = "postgresql+psycopg2://postgres:12341234_datamicrondb@localhost:5432/pulse"

jobstores = {
    "default": MemoryJobStore(),
    "persistent": SQLAlchemyJobStore(url=DATABASE_URL),
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

job = scheduler.get_job("persistent_job", jobstore="persistent")
print(job)                     # shows id, trigger, next run
print(job.trigger)             # trigger details
print(job.func_ref, job.args)  # target function and args
