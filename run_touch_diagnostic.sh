#!/bin/bash
# Simple script to run touch diagnostic without resets

DEVICE=$(ls /dev/ttyACM* 2>/dev/null | head -1)

if [ -z "$DEVICE" ]; then
    echo "No board found. Please plug in the board."
    exit 1
fi

echo "Found board at $DEVICE"
echo "Running touch diagnostic..."
echo ""

python3 << 'EOF'
import serial
import time
import glob
import sys

ports = glob.glob('/dev/ttyACM*')
port = ports[0] if ports else None

if not port:
    print("No board found")
    sys.exit(1)

ser = serial.Serial(port, 115200, timeout=1)
time.sleep(0.5)

# Stop current program
ser.write(b'\x03\x03')
time.sleep(0.5)
ser.read(ser.in_waiting)

# Run diagnostic
ser.write(b'import test_touch_raw\r\n')
time.sleep(3)

if ser.in_waiting:
    print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))

print("\n" + "="*60)
print("Touch diagnostic running - touch the screen!")
print("="*60)
print("\nMonitoring for touch events (Press Ctrl-C to stop)...\n")

try:
    while True:
        time.sleep(0.1)
        if ser.in_waiting:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            if data.strip():
                print(data, end='', flush=True)
except KeyboardInterrupt:
    print("\n\nStopped.")

ser.close()
EOF
