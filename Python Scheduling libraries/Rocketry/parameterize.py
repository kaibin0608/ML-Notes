from rocketry import Rocketry
from rocketry.conds import every
from rocketry.args import Arg

# What is “parameterizing”?
# Making code accept values from the outside (function parameters, config, env vars) instead of hard-coding them. It turns rigid code into reusable, testable code whose behavior you can change without editing source. 
# In Rocketry specifically
# Rocketry lets you set session parameters and inject them into tasks at run time with arguments like Arg('name'). That’s late-binding: the value is resolved right before the task runs.

app = Rocketry()  # default (sync) is fine for a demo

# Session-level param
app.params(my_arg="Hello world")

# Fire every 5 seconds so you can see it run
@app.task(every("5 seconds"))
def do_things(item=Arg("my_arg")):
    print("do_things says session level:", item)

from rocketry.args import FuncArg

def get_item():
    return 'hello world'

@app.task(every("5 seconds"))
def do_things_func(item = FuncArg(get_item)):
    print("do_things says function arg:", item)

if __name__ == "__main__":
    app.run()
