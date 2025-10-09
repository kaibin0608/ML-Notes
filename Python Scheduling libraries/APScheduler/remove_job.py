from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.base import JobLookupError
from datetime import datetime
import time
from dotenv import load_dotenv
import os

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

def persistent_job():
    print(f"[{datetime.now():%H:%M:%S}] Persistent job (PostgreSQL)")

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

# --- Arrange: add (idempotent) ---
scheduler.add_job(
    persistent_job, "interval", seconds=15,
    id="persistent_job", jobstore="persistent", replace_existing=True
)
print("Added/ensured job exists in 'persistent' store.")

# --- Assert 1: verify presence ---
job = scheduler.get_job("persistent_job", jobstore="persistent")
print("Exists after add? ", bool(job))

# --- Act: remove ---
try:
    scheduler.remove_job("persistent_job", jobstore="persistent")
    print("Removed job from 'persistent' store.")
except JobLookupError:
    print("Job not found during remove (unexpected in this flow).")

# --- Assert 2: verify removal ---
job = scheduler.get_job("persistent_job", jobstore="persistent")
print("Exists after remove? ", bool(job))

print("Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler shut down")
