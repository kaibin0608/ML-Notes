"""
Script to decode and understand the job_state column in APScheduler table
The job_state is a pickled binary object that contains all job configuration details
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pickle
from pprint import pprint
from datetime import datetime

# Load environment variables
env_file_path = r"C:\Users\DataMicron\Documents\Machine Learning Notes\ML-Notes\Python Scheduling libraries\env.txt"
load_dotenv(dotenv_path=env_file_path, override=True)
name = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

# Create engine
engine = create_engine(DATABASE_URL)

print("=" * 100)
print("APScheduler Job State Decoder")
print("=" * 100)
print("This script decodes the 'job_state' column which is a pickled Python object")
print("=" * 100)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, next_run_time, job_state FROM apscheduler_jobs"))
    rows = result.fetchall()

    if not rows:
        print("\n📭 No jobs found in the database")
    else:
        print(f"\n📊 Found {len(rows)} job(s). Decoding job_state column...\n")

        for i, row in enumerate(rows, 1):
            job_id = row[0]
            next_run_time = row[1]
            job_state_binary = row[2]

            print(f"\n{'=' * 100}")
            print(f"JOB #{i}: {job_id}")
            print("=" * 100)

            print(f"\n📅 Next Run Time (from table): {next_run_time}")
            print(f"\n📦 Job State Binary Size: {len(job_state_binary)} bytes")

            try:
                # Unpickle the job_state
                job_state = pickle.loads(job_state_binary)

                print("\n" + "-" * 100)
                print("DECODED JOB STATE (Complete Dictionary):")
                print("-" * 100)

                # Pretty print the entire job state
                pprint(job_state, width=100, indent=2)

                print("\n" + "-" * 100)
                print("KEY FIELDS EXPLAINED:")
                print("-" * 100)

                # Extract and explain key fields
                fields = {
                    'version': ('APScheduler Version', job_state.get('version', 'N/A')),
                    'id': ('Job ID', job_state.get('id', 'N/A')),
                    'func': ('Function Reference (module:function)', job_state.get('func', 'N/A')),
                    'trigger': ('Trigger Type & Settings', job_state.get('trigger', 'N/A')),
                    'executor': ('Executor Name', job_state.get('executor', 'default')),
                    'args': ('Positional Arguments', job_state.get('args', ())),
                    'kwargs': ('Keyword Arguments', job_state.get('kwargs', {})),
                    'name': ('Job Name', job_state.get('name', 'N/A')),
                    'misfire_grace_time': ('Misfire Grace Time (seconds)', job_state.get('misfire_grace_time', None)),
                    'coalesce': ('Coalesce (combine missed runs)', job_state.get('coalesce', True)),
                    'max_instances': ('Max Concurrent Instances', job_state.get('max_instances', 1)),
                    'next_run_time': ('Next Scheduled Run', job_state.get('next_run_time', 'N/A')),
                }

                for key, (description, value) in fields.items():
                    print(f"\n  {key:20} │ {description}")
                    print(f"  {' ' * 20} │ Value: {value}")

                # Special handling for trigger details
                if 'trigger' in job_state and job_state['trigger']:
                    trigger = job_state['trigger']
                    print(f"\n\n{'─' * 100}")
                    print("TRIGGER DETAILS:")
                    print("─" * 100)
                    print(f"  Type: {type(trigger).__name__}")

                    # Check trigger type and display relevant info
                    trigger_str = str(trigger)
                    print(f"  Configuration: {trigger_str}")

                    if hasattr(trigger, '__dict__'):
                        print("\n  Trigger Attributes:")
                        for attr, val in trigger.__dict__.items():
                            print(f"    {attr:25} = {val}")

            except Exception as e:
                print(f"\n❌ ERROR decoding job_state: {e}")
                print(f"   This might happen if the job was created with a different APScheduler version")

print("\n\n" + "=" * 100)
print("SUMMARY:")
print("=" * 100)
print("""
The job_state column contains a pickled Python dictionary with these key components:

1. func/func_ref  - Points to the Python function to execute (e.g., "module_name:function_name")
2. trigger        - Defines when the job runs (interval, cron, date, etc.)
3. args/kwargs    - Arguments passed to the function when it executes
4. next_run_time  - When the job will run next
5. executor       - Which executor will run the job (default, threadpool, processpool)
6. max_instances  - How many instances can run concurrently
7. coalesce       - Whether to combine multiple missed runs into one
8. misfire_grace_time - How late a job can start before being considered missed

The scheduler reads this binary data to restore jobs after restart.
""")
print("=" * 100)
