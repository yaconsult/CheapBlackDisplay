#!/usr/bin/env python3
"""Quick test runner - auto-detects port and runs touch test"""
import serial
import time
import glob
import sys

# Find board
ports = glob.glob('/dev/ttyACM*')
if not ports:
    print("No board found. Make sure it's plugged in.")
    sys.exit(1)

port = ports[0]
print(f"Found board at {port}")

ser = serial.Serial(port, 115200, timeout=1)
time.sleep(0.5)

# Stop any running program
ser.write(b'\x03\x03')
time.sleep(0.5)
ser.read(ser.in_waiting)

# Run touch test
print("\nRunning test_display_with_touch.py...")
ser.write(b'import test_display_with_touch\r\n')
time.sleep(3)

if ser.in_waiting:
    response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
    print(response)

print("\n" + "="*60)
print("Touch test should be running!")
print("="*60)
print("\nDisplay should show:")
print("  - Colored squares (R, G, B, W) in corners")
print("  - 'Touch Test 480x320' text in center")
print("  - 'Touch Me!' button")
print("\nTouch the button to test touch functionality.")
print("\nIf display is blank, try unplugging and replugging USB.")

ser.close()
