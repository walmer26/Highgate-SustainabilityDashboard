# -------------------------CREATES A DJANGO CONTEXT------------------------------------->
import os
import sys
import django
from pathlib import Path
from pprint import pprint

# Get the django deployment environment defaulting to development.
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"project.settings.{ENVIRONMENT}")

# Add the project path to the Python path
PROJECT_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_PATH))

# Initialize the Django application
django.setup()

# ----------------------START CAPTURING DATA FOR MEMORY STATS---------------------------->
import tracemalloc

# Start tracing memory allocations
tracemalloc.start()
# Take a snapshot of the current memory allocations
snapshot1 = tracemalloc.take_snapshot()

# -------------------------TEST YOUR CODE BELOW THIS LINE--------------------------------->








# -------------------------TEST YOUR CODE ABOVE THIS LINE---------------------------------->

# Take a second snapshot of the current memory allocations after code to test.
snapshot2 = tracemalloc.take_snapshot()
# Compares both snapshots
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

# show top memory consumed lines (20 lines in this case)
print("Top 20 memory-consuming lines:")
for stat in top_stats[:20]:
    pprint(stat)

# Display current and peak memory usage
current, peak = tracemalloc.get_traced_memory()
pprint(f"Current memory usage is {current / 10**6:.2f} MB; Peak was {peak / 10**6:.2f} MB")

# Closes trace.
tracemalloc.stop()

# Show the queries if django models are used
pprint(django.db.connection.queries)