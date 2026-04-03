#!/usr/bin/env python3
"""Monitor touch events in real-time"""
import serial
import time
import glob
import sys

# Find board
ports = glob.glob('/dev/ttyACM*')
if not ports:
    print("No board found")
    sys.exit(1)

port = ports[0]
print(f"Monitoring touch events on {port}")
print("Touch the screen - events will appear here")
print("Press Ctrl-C to stop\n")

ser = serial.Serial(port, 115200, timeout=0.1)

try:
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            if data.strip():
                # Look for touch-related output
                if any(keyword in data.lower() for keyword in ['touch', 'click', 'press', 'coord', 'x=', 'y=']):
                    print(data, end='', flush=True)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n\nStopped monitoring.")
finally:
    ser.close()
