import asyncio 

async def fetch_data():
    print("start fetching")
    await asyncio.sleep(2)  # simulating a network delay
    print("done fetching") 
    return {'data': 1}

async def print_numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.5)  # simulate some processing delay, the done fetching will print after 8 numbers because the 2 seconds delay is done

async def main():
    task1 = asyncio.create_task(fetch_data()) # these tasks is a subclass called Task, which is a subclass of Future, which is a low-level awaitable object that represents a result that may not be available yet
    task2 = asyncio.create_task(print_numbers())

    value = await task1 # to assign the output from coroutine task1 to value, if we dont put await here, the coroutine will think that after getting the value , then is finished
    print(value)
    await task2

asyncio.run(main())