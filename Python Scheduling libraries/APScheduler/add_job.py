from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
import time 
from datetime import datetime
from dotenv import load_dotenv
import os
from jobs import persistent_job,initialize_scheduler,volatile_job

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


# Configure job stores
jobstores = {
    'default': MemoryJobStore(),
    'persistent':SQLAlchemyJobStore(url=DATABASE_URL) }

# Initialize scheduler with our job stores
scheduler = initialize_scheduler(jobstores)

# Check if persistent job already exists (after restart)
existing_job = scheduler.get_job('persistent_job', jobstore='persistent')
if not existing_job:
    print("First run - adding default job")
    # Add a job to the persistent store
    scheduler.add_job(
        persistent_job, 
        'interval', 
        seconds=15, 
        id='persistent_job',
        jobstore='persistent'  # Specify the job store
    )
else:
    print("Job already exists - loaded from PostgreSQL")

# Always add the volatile job (it won't survive restarts)
scheduler.add_job(
    volatile_job, 
    'interval', 
    seconds=10, 
    id='volatile_job'
)

print("Scheduler started with both volatile and persistent jobs")
print("The persistent job will survive application restarts")
print("Press Ctrl+C to exit")

try:
    # Keep the main thread alive
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler shut down")