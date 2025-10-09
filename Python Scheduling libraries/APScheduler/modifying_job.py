from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.base import JobLookupError
from jobs import persistent_job,initialize_scheduler
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time

# Define your PostgreSQL connection string
# Replace 'user', 'password', 'host', 'port', and 'database' with your actual details

env_file_path = r"C:\Users\DataMicron\Documents\Machine Learning Notes\ML-Notes\Python Scheduling libraries\env.txt"
load_dotenv(dotenv_path=env_file_path, override=True)
name = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")
DATABASE_URL =f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

jobstores = {
    "default": MemoryJobStore(),
    "persistent": SQLAlchemyJobStore(url=DATABASE_URL),
}

scheduler = initialize_scheduler(jobstores=jobstores)

# change the schedule
try:
    scheduler.reschedule_job("my_job", jobstore="persistent",trigger='interval', seconds=3)
    print("Rescheduled")
except JobLookupError:
    print("Not found")

# Change args/kwargs (what the job receives)
try:
    scheduler.modify_job(
            'persistent_job',
            jobstore='persistent',      # current store
            name='News scrapping',
            misfire_grace_time=3600,
            coalesce=True, # If your app was down (or the job was paused) and multiple runs were missed, coalesce=True tells APScheduler to collapse all those missed runs into a single catch-up run when the scheduler comes back.
            max_instances=1,
            executor='default'
            # args=['customer', 42],
            # kwargs={'dry_run': False}
        )
    print("Modified")
except JobLookupError:
    print("Not found")


try: 
    # Nudge next run (e.g., delay 10 minutes)
    scheduler.modify_job('my_job', jobstore='persistent',
                        next_run_time=datetime.now() + timedelta(minutes=10))
    print("Modified Run time")
except JobLookupError:
    print("Not found")

print("Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler shut down")
