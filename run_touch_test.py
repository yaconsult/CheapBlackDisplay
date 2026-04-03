#!/usr/bin/env python3
"""
Run the touch test on the board, auto-detecting the correct serial port
"""
import serial
import time
import sys
import glob

def find_board():
    """Find the board's serial port"""
    ports = glob.glob('/dev/ttyACM*')
    if not ports:
        print("No board found on /dev/ttyACM*")
        return None
    
    # Try each port
    for port in ports:
        try:
            ser = serial.Serial(port, 115200, timeout=1)
            ser.close()
            return port
        except:
            continue
    
    return None

def main():
    port = find_board()
    if not port:
        print("Error: Could not find board")
        sys.exit(1)
    
    print(f"Found board at {port}")
    
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(0.5)
    
    # Stop any running program
    ser.write(b'\x03\x03')
    time.sleep(0.5)
    ser.read(ser.in_waiting)
    
    # Run the touch test
    print("\nRunning test_display_with_touch.py...")
    ser.write(b'import test_display_with_touch\r\n')
    time.sleep(5)
    
    # Read output
    try:
        if ser.in_waiting:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(response)
    except Exception as e:
        print(f"Note: {e}")
    
    print("\n" + "="*60)
    print("Touch test is running!")
    print("="*60)
    print("\nDisplay should show:")
    print("  - Colored squares (R, G, B, W) in corners")
    print("  - 'Touch Test 480x320' text in center")
    print("  - 'Touch Me!' button in the middle")
    print("\nTry touching the button - the text should change to 'TOUCHED!'")
    print("\nPress Ctrl-C on the board to stop the test")
    
    ser.close()

if __name__ == '__main__':
    main()
