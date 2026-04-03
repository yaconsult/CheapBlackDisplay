#!/usr/bin/env python3
"""
Upload files to MicroPython board via serial connection
"""
import serial
import time
import os
import sys

def send_command(ser, command, wait_time=0.1):
    """Send a command to the REPL and wait for response"""
    ser.write(command.encode() + b'\r\n')
    time.sleep(wait_time)
    response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
    return response

def upload_file(ser, local_path, remote_path):
    """Upload a file to the board"""
    print(f"Uploading {local_path} -> {remote_path}")
    
    with open(local_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Escape the content for Python string
    content_escaped = content.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    
    # Create directory if needed
    remote_dir = os.path.dirname(remote_path)
    if remote_dir:
        send_command(ser, f"import os")
        send_command(ser, f"try:\n    os.mkdir('{remote_dir}')\nexcept:\n    pass")
    
    # Write file in chunks to avoid buffer overflow
    chunk_size = 512
    send_command(ser, f"f = open('{remote_path}', 'w')")
    
    for i in range(0, len(content_escaped), chunk_size):
        chunk = content_escaped[i:i+chunk_size]
        send_command(ser, f"f.write('{chunk}')", wait_time=0.05)
    
    send_command(ser, "f.close()")
    print(f"  ✓ Uploaded {len(content)} bytes")

def main():
    port = '/dev/ttyACM0'
    baudrate = 115200
    
    print(f"Connecting to {port}...")
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(1)
    
    # Enter raw REPL mode
    ser.write(b'\x03\x03')  # Ctrl-C twice
    time.sleep(0.5)
    ser.read(ser.in_waiting)
    
    ser.write(b'\x01')  # Ctrl-A for raw REPL
    time.sleep(0.5)
    response = ser.read(ser.in_waiting)
    
    if b'raw REPL' not in response:
        print("Failed to enter raw REPL mode")
        print(response.decode('utf-8', errors='ignore'))
        ser.close()
        return
    
    print("Entered raw REPL mode")
    
    # Exit raw REPL to normal REPL
    ser.write(b'\x02')  # Ctrl-B
    time.sleep(0.5)
    ser.read(ser.in_waiting)
    
    # Upload lib folder files
    lib_files = [
        'ESP32-JC3248W535-Micropython-LVGL-main/lib/_axs15231b_init.py',
        'ESP32-JC3248W535-Micropython-LVGL-main/lib/axs15231.py',
        'ESP32-JC3248W535-Micropython-LVGL-main/lib/axs15231b.py',
        'ESP32-JC3248W535-Micropython-LVGL-main/lib/lv_config.py',
        'ESP32-JC3248W535-Micropython-LVGL-main/lib/lv_config_90.py',
    ]
    
    for lib_file in lib_files:
        local_path = lib_file
        remote_path = 'lib/' + os.path.basename(lib_file)
        upload_file(ser, local_path, remote_path)
    
    # Upload task_handler
    upload_file(ser, 'task_handler.py', 'task_handler.py')
    
    # Upload test files
    upload_file(ser, 'ESP32-JC3248W535-Micropython-LVGL-main/test_landscape_mode.py', 'test_landscape_mode.py')
    upload_file(ser, 'ESP32-JC3248W535-Micropython-LVGL-main/test_portrait_mode.py', 'test_portrait_mode.py')
    
    print("\n✓ All files uploaded successfully!")
    
    # List files on board
    print("\nFiles on board:")
    send_command(ser, "import os")
    response = send_command(ser, "print(os.listdir('/'))", wait_time=0.5)
    print(response)
    
    response = send_command(ser, "print(os.listdir('/lib'))", wait_time=0.5)
    print(response)
    
    ser.close()
    print("\nConnection closed")

if __name__ == '__main__':
    main()
