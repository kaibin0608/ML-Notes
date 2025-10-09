"""
Script to trace and inspect all APScheduler jobs in the PostgreSQL database
This helps you understand what schedulers have been initiated and their current state
"""

from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
import os
from datetime import datetime
import pickle

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

print("=" * 80)
print("APScheduler Job Store Inspector")
print("=" * 80)
print(f"Database: {name}")
print(f"Host: {host}:{port}")
print("=" * 80)

# Check if the apscheduler_jobs table exists
inspector = inspect(engine)
tables = inspector.get_table_names()

if 'apscheduler_jobs' not in tables:
    print("\n⚠️  No apscheduler_jobs table found in database!")
    print("   The scheduler has never been run with persistent storage.")
else:
    print(f"\n✓ Found apscheduler_jobs table\n")

    # Query all jobs
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM apscheduler_jobs"))
        rows = result.fetchall()
        columns = result.keys()

        if not rows:
            print("📭 No jobs found in database")
            print("   The job store is empty - all previous jobs have been removed or none were added.")
        else:
            print(f"📊 Found {len(rows)} job(s) in database:\n")

            for i, row in enumerate(rows, 1):
                print(f"Job #{i}")
                print("-" * 60)

                # Create a dictionary from the row
                job_data = dict(zip(columns, row))

                print(f"  ID:               {job_data.get('id', 'N/A')}")

                # Try to unpickle the job_state to get more details
                try:
                    job_state = pickle.loads(job_data['job_state'])
                    print(f"  Function:         {job_state.get('func_ref', 'N/A')}")
                    print(f"  Trigger:          {job_state.get('trigger', 'N/A')}")
                    print(f"  Next Run:         {job_state.get('next_run_time', 'N/A')}")
                    print(f"  Args:             {job_state.get('args', ())}")
                    print(f"  Kwargs:           {job_state.get('kwargs', {})}")
                    print(f"  Executor:         {job_state.get('executor', 'default')}")
                    print(f"  Max Instances:    {job_state.get('max_instances', 1)}")
                    print(f"  Coalesce:         {job_state.get('coalesce', True)}")
                    print(f"  Misfire Grace:    {job_state.get('misfire_grace_time', None)} seconds")
                except Exception as e:
                    print(f"  ⚠️  Could not decode job state: {e}")
                    print(f"  Raw job_state size: {len(job_data['job_state'])} bytes")

                print(f"  Next Run Time:    {job_data.get('next_run_time', 'N/A')}")
                print()

print("\n" + "=" * 80)
print("Cleanup Options:")
print("=" * 80)
print("To clear ALL jobs from database:")
print("  DELETE FROM apscheduler_jobs;")
print("\nTo clear a specific job:")
print("  DELETE FROM apscheduler_jobs WHERE id = 'your_job_id';")
print("=" * 80)
