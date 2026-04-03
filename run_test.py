#!/usr/bin/env python3
"""
Run test scripts on the MicroPython board
"""
import serial
import time
import sys

def run_script(port, script_name, baudrate=115200):
    """Run a script on the board and display output"""
    print(f"\n{'='*60}")
    print(f"Running {script_name} on the board...")
    print(f"{'='*60}\n")
    
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(1)
    
    # Send Ctrl-C to interrupt any running program
    ser.write(b'\x03\x03')
    time.sleep(0.5)
    ser.read(ser.in_waiting)
    
    # Import and run the script
    command = f"import {script_name.replace('.py', '')}\r\n"
    ser.write(command.encode())
    
    print(f"Sent command: {command.strip()}")
    print("\nBoard output:")
    print("-" * 60)
    
    # Read output for a few seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            try:
                text = data.decode('utf-8', errors='ignore')
                print(text, end='')
                sys.stdout.flush()
            except:
                pass
        time.sleep(0.1)
    
    print("\n" + "-" * 60)
    print("\n✓ Script is running on the board")
    print("The display should now show the test pattern.")
    print("\nPress Ctrl-C on the board to stop the script.")
    
    ser.close()

def main():
    port = '/dev/ttyACM0'
    
    if len(sys.argv) > 1:
        script = sys.argv[1]
    else:
        script = 'test_landscape_mode'
    
    run_script(port, script)

if __name__ == '__main__':
    main()
