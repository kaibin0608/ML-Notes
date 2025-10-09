from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def volatile_job():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Volatile job (in-memory)")

def persistent_job():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Persistent job (in PostgresSQL)")

def initialize_scheduler(jobstores):
    # Initialize the scheduler with the configured job stores
    scheduler = BackgroundScheduler(jobstores=jobstores)
    # Start the scheduler
    scheduler.start()
    return scheduler