import asyncio

# def foo():
#     print("foo")

# in normal situation, the print('tim') will not run until foo() is done, this is what we call synchronous programming, everything that we write is happening sequentially
# for asynchronous programming, we can use async and await keywords to make the code non-blocking, so that the print('tim') can run while foo() is still running
# foo()
# print('tim')

##########################################################################################
# coroutines - components that generalize subroutines for non-preemptive multitasking, by allowing execution to be suspended and resumed
# async event loop - a programming construct that waits for and dispatches events or messages in a program
##########################################################################################

# async basically tells python to create a wrapper for the function, so when we call this function it returns a coroutine object
# need await to execute the coroutine
async def main(): 
    print("tim")
    # await foo("text") 
    # print("finished") # this will run after foo() is done, but we dont want it to wait for foo() to be done, we want it to run while foo() is still running
    task = asyncio.create_task(foo('text')) # this will create a task that will run foo() in the background, and it will not block the main coroutine
    # await task # if we want to wait for foo to finish only we print 'finished', we can do this 
    # await asyncio.sleep(2) # we can also pause for 2 seconds and ket the task run
    print("finished") # this will run immediately after creating the task, without waiting for foo() to be done


async def foo(text):
    print(text)
    # this await keyword right here, is what it's required to run a coroutine, without this await keyword, the coroutine will not be executed, is just created a coroutine
    # the await keyword is what tells python to pause the execution of this coroutine until the awaitable (in this case asyncio.sleep(1)) is done
    await asyncio.sleep(1) 

# we need to define a async event-loop to run the main coroutine
asyncio.run(main())  # this is how we run the coroutine, we told asyncio to run the main coroutine, and it will take care of the event loop for us
