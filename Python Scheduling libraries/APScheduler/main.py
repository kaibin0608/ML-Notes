from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def display():
    print("Message:")
    # print("This function has beed executed")
    # job_id.remove() # remove the job after execution
    scheduler.shutdown(wait = False) # wait = false to shutdown immediately

# Initialize the rest of the application here, or before the scheduler initialization
scheduler = BlockingScheduler()
# job_id = scheduler.add_job(display, 'interval', seconds=5)
# job_id = scheduler.add_job(display, 'interval', seconds=1)
# scheduler.add_job(display, 'interval', seconds=5, args=['job 1'])

scheduler.start()
# print("Hello World")
