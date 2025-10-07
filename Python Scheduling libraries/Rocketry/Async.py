import asyncio
from rocketry import Rocketry

app = Rocketry(execution="async")

@app.task()
async def do_things():
    print("Doing things...")

async def main():
    "Launch Rocketry app (and possibly something else)"
    rocketry_task = asyncio.create_task(app.serve())
    # Start possibly other async apps
    await rocketry_task

if __name__ == "__main__":
    asyncio.run(main())

# import asyncio

# async def fetch(n):
#     await asyncio.sleep(1)   # pretend network I/O
#     return f"done {n}"

# async def main():
#     results = await asyncio.gather(*(fetch(i) for i in range(3)))
#     print(results)

# asyncio.run(main())
