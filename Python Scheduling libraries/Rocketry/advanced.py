from rocketry import Rocketry
from rocketry.conds import every
import os


app = Rocketry(execution = "main")

# Define a condition function to check if a file exists
@app.cond()
def file_exists(file):
    if os.path.isfile(file):
        with open(file) as f:
            print(f.read())
        return True
    else:
        print("No file exists")
        return False

@app.task(every('1 seconds') & file_exists('test.txt'))
def process_file():
    print("Processing file!")

if __name__ =='__main__':
    app.run()