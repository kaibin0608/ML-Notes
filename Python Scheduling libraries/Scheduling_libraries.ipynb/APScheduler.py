from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def display(msg):
    print("Message:",msg)
    # print("This function has beed executed")
    # job_id.remove() # remove the job after execution
    # scheduler.shutdown(wait = False) # wait = false to shutdown immediately


# Initialize the rest of the application here, or before the scheduler initialization
scheduler = BlockingScheduler()
# job_id = scheduler.add_job(display, 'interval', seconds=5)
scheduler.add_job(display, 'job 1', seconds=5)
scheduler.add_job(display, 'job 2', seconds=3)

scheduler.start()
print("Hello World")