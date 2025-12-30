#!/usr/bin/env python3
"""
Example script - Just prints a hello message
Drop any .py or .sh file in this folder and it will appear in the app!
"""
import time
from datetime import datetime

print("=" * 50)
print(f"Hello from example script!")
print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

# Simulate some work
for i in range(5):
    print(f"Working... step {i + 1}/5")
    time.sleep(1)

print("Done!")

