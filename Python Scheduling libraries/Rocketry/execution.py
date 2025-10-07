from rocketry import Rocketry

# execution="main"

# What it is: Runs the task synchronously in the app’s main thread & process. 
# Use when: The job is quick, must run inline, or needs to touch state that only exists in the main thread (e.g., a non-thread-safe object).
# Trade-offs: Blocks the scheduler loop while it runs.

# execution="async"

# What it is: Runs an async def task on an event loop (non-blocking I/O concurrency). 
# Use when: The task is I/O-bound (HTTP calls, DB queries, file/network waits) and you’re already using asyncio or want high I/O concurrency.
# Trade-offs: CPU-heavy code will still block unless you offload it.

# execution="thread"

# What it is: Runs the task in a separate thread (same process, shared memory). 
# Use when: You want to concurrently run I/O-bound work (downloads, API calls) without blocking the main thread.
# Trade-offs: Threads share memory but are limited by Python’s GIL, so they don’t speed up CPU-bound Python code. 

# execution="process"

# What it is: Runs the task in a separate process via multiprocessing (isolated memory). 
# Use when: Work is CPU-bound (heavy compute, ML inference, big JSON parsing) and you want true parallelism beyond the GIL. 
# Trade-offs: Higher overhead (process spawn, IPC, pickling); ensure functions/args are picklable.

app = Rocketry()

@app.task(execution = 'main')
def run_main():
    print("Running in main!")

@app.task(execution = 'async')
def run_async():
    print("Running in async!")

@app.task(execution = 'thread')
def run_thread():
    print("Running in thread!")

@app.task(execution = 'process')
def run_process():
    print("Running in process!")

if __name__ == "__main__":
# Start the scheduler
    app.run()