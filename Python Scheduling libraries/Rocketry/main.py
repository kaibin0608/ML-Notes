from rocketry import Rocketry
from rocketry.args import Return

app = Rocketry(execution='async')

@app.task('daily')
def do_daily():
    print("This function runs once a day")

@app.task('every 5 seconds')
def do_every_5_seconds():
    print("This function runs every 5 seconds")
    
@app.task('every 1 hour')
def do_every_hour():
    print("This function runs every hour")

@app.task('minutely')
def do_every_min():
    print("This function runs every minute")

@app.task('daily between 08:00 and 10:00')
def do_every_min():
    print("This function runs every mmorning")

if __name__ == "__main__":
    # Start the scheduler
    app.run()