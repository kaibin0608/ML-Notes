from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def display():
    print("This function has beed executed")
    job_id.remove() # remove the job after execution, but the blocking schedular still running ,need to shut down
    scheduler.shutdown(wait = False) # wait = false to shutdown immediately
    # print("Message:")

def display_message(msg):
    print(f"Message: {msg}")

# Initialize the rest of the application here, or before the scheduler initialization
scheduler = BlockingScheduler()

# add job to scheduler
# scheduler.add_job(display, 'interval', seconds=1)

# if want to remove the job after execution, store the job id in a variable
# job_id = scheduler.add_job(display, 'interval', seconds=5)

# to pass in arguments to the job function, use args parameter
# job_id = scheduler.add_job(display_message, 'interval', seconds=5, args=["Hello World"])

# to schedule multiple jobs, just add more jobs
scheduler.add_job(display_message, 'interval', seconds=5, args=["Hello World"])
scheduler.add_job(display_message, 'interval', seconds=3, args=["Hello World 2"])


scheduler.start()
# print("Hello World")
