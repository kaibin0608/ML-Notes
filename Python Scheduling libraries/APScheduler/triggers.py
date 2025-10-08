from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from datetime import datetime
def display_message(msg):
    print(f"Message: {msg}")
    # scheduler.shutdown(wait = False) # wait = false to shutdown immediately

# Initialize the rest of the application here, or before the scheduler initialization
scheduler = BlockingScheduler()

# date trigger
scheduler.add_job(display_message, 'date',run_date = datetime(2023,2,20,12,0,0), args=["Hello World"]) # this job will execute only once at the specified date and time (2023-2-20)

# we can also do this 
scheduler.add_job(display_message, 'date',run_date = "2022-4-30 08:00:00", args=["Hello World"])

## cron trigger
scheduler.add_job(display_message, 'cron', hour = 17, minute = 30, args=["Hello World"]) # execute every day at 5:30 PM
scheduler.add_job(display_message, 'cron', hour = 17, minute ='*', args=["Hello World"]) # execute every minutes at 5 PM, if second ='*', will be every second at 5pm
scheduler.add_job(display_message, 'cron', hour = 17, second ='*/5', args=["Hello World"]) # every 5 seconds
scheduler.add_job(display_message, 'cron', month = "1-3,5-8", second ='*/5', args=["Hello World"]) # execute from Jan to Mar, May to Aug every 5 seconds

scheduler.start()
