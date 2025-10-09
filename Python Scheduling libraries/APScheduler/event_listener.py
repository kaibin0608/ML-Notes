# listener_demo.py
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import (
    EVENT_JOB_ADDED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_REMOVED,
    EVENT_SCHEDULER_START, EVENT_SCHEDULER_SHUTDOWN
)

# ----- demo jobs -------------------------------------------------------------
def ok_job():
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] ok_job ran and returns 123")
    return 123  # you'll see this as event.retval

def bad_job():
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] bad_job is about to raise ValueError")
    raise ValueError("demo failure from bad_job")

# ----- event listener --------------------------------------------------------
def on_event(event):
    # event.code is a bit-mask; we check which mask it matches
    if event.code & EVENT_SCHEDULER_START:
        print("⚙️  SCHEDULER STARTED")
    elif event.code & EVENT_SCHEDULER_SHUTDOWN:
        print("🛑 SCHEDULER SHUT DOWN")

    elif event.code & EVENT_JOB_ADDED:
        print(f"➕ JOB ADDED: id={event.job_id}")
    elif event.code & EVENT_JOB_REMOVED:
        print(f"➖ JOB REMOVED: id={event.job_id}")

    elif event.code & EVENT_JOB_EXECUTED:
        print(f"✅ JOB OK: id={event.job_id}, retval={getattr(event, 'retval', None)!r}, "
              f"scheduled={getattr(event, 'scheduled_run_time', None)}")

    elif event.code & EVENT_JOB_ERROR:
        print(f"❌ JOB ERROR: id={event.job_id}, exc={getattr(event, 'exception', None)}\n"
              f"{getattr(event, 'traceback', '')}")

# ----- wire it up ------------------------------------------------------------
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # Listen to a bunch of event types by OR-combining their masks
    scheduler.add_listener(
        on_event,
        EVENT_SCHEDULER_START
        | EVENT_SCHEDULER_SHUTDOWN
        | EVENT_JOB_ADDED
        | EVENT_JOB_REMOVED
        | EVENT_JOB_EXECUTED
        | EVENT_JOB_ERROR
    )

    scheduler.start()

    # Add a success job (runs every 3s)
    scheduler.add_job(ok_job, "interval", seconds=3, id="ok_job")

    # Add a failing job (runs every 5s)
    scheduler.add_job(bad_job, "interval", seconds=5, id="bad_job")

    print("Running. Press Ctrl+C to stop…")

    try:
        # Let it run for ~20s, then remove the failing job to trigger JOB_REMOVED
        t0 = time.time()
        removed = False
        while True:
            time.sleep(1)
            if not removed and time.time() - t0 > 20:
                scheduler.remove_job("bad_job")
                removed = True
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown(wait=True)
