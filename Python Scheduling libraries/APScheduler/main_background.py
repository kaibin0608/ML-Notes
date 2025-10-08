from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def display_message(msg):
    print(f"Message: {msg}")
    # scheduler.shutdown(wait = False) # wait = false to shutdown immediately

# Initialize the rest of the application here, or before the scheduler initialization
# background scheduler will run in the background and allow the main program to continue running, if the main program ends its execution before the schedular, the schedular will also stop
# blocking scheduler will block the main program from running, and the main program will wait for the schedular to finish its execution
# scheduler = BlockingScheduler()
scheduler = BackgroundScheduler()

# to schedule multiple jobs, just add more jobs
scheduler.add_job(display_message, 'interval', seconds=5, args=["Hello World"])
scheduler.add_job(display_message, 'interval', seconds=3, args=["Hello World 2"])


scheduler.start()
sleep(10)

# to show the difference between background and blocking scheduler
print("hihihi") # this is not showing when we use blocking schedular, to show this with blocking scheduler, we need to shut down the scheduler