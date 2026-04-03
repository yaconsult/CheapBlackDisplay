#!/usr/bin/env python3
"""
Upload files to MicroPython board using ampy-like approach
"""
import serial
import time
import os

def wait_for_prompt(ser, timeout=2):
    """Wait for the >>> prompt"""
    start = time.time()
    buffer = b''
    while time.time() - start < timeout:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            buffer += data
            if b'>>>' in buffer:
                return True
        time.sleep(0.01)
    return False

def upload_file_raw(ser, local_path, remote_path):
    """Upload a file using raw REPL mode"""
    print(f"Uploading {local_path} -> {remote_path}")
    
    with open(local_path, 'rb') as f:
        content = f.read()
    
    # Enter raw REPL
    ser.write(b'\x03\x03')  # Ctrl-C twice
    time.sleep(0.3)
    ser.read(ser.in_waiting)
    
    ser.write(b'\x01')  # Ctrl-A for raw REPL
    time.sleep(0.3)
    response = ser.read(ser.in_waiting)
    
    if b'raw REPL' not in response:
        print(f"Failed to enter raw REPL: {response}")
        return False
    
    # Create directory if needed
    remote_dir = os.path.dirname(remote_path)
    if remote_dir:
        cmd = f"import os\ntry:\n    os.mkdir('{remote_dir}')\nexcept:\n    pass\n"
        ser.write(cmd.encode())
        ser.write(b'\x04')  # Ctrl-D to execute
        time.sleep(0.3)
        ser.read(ser.in_waiting)
    
    # Write file content
    cmd = f"f = open('{remote_path}', 'wb')\n"
    cmd += f"f.write({repr(content)})\n"
    cmd += "f.close()\n"
    
    ser.write(cmd.encode())
    ser.write(b'\x04')  # Ctrl-D to execute
    time.sleep(0.5)
    response = ser.read(ser.in_waiting)
    
    # Exit raw REPL
    ser.write(b'\x02')  # Ctrl-B
    time.sleep(0.3)
    ser.read(ser.in_waiting)
    
    if b'OK' in response or b'>>>' in response:
        print(f"  ✓ Uploaded {len(content)} bytes")
        return True
    else:
        print(f"  ✗ Upload failed: {response}")
        return False

def main():
    port = '/dev/ttyACM0'
    baudrate = 115200
    
    print(f"Connecting to {port}...")
    ser = serial.Serial(port, baudrate, timeout=2)
    time.sleep(1)
    
    # Upload files
    files_to_upload = [
        ('task_handler.py', 'task_handler.py'),
        ('ESP32-JC3248W535-Micropython-LVGL-main/test_landscape_mode.py', 'test_landscape_mode.py'),
        ('ESP32-JC3248W535-Micropython-LVGL-main/test_portrait_mode.py', 'test_portrait_mode.py'),
    ]
    
    for local, remote in files_to_upload:
        upload_file_raw(ser, local, remote)
        time.sleep(0.5)
    
    # Verify files
    print("\nVerifying files on board:")
    ser.write(b'\x03\x03')
    time.sleep(0.3)
    ser.read(ser.in_waiting)
    
    ser.write(b'import os\r\n')
    time.sleep(0.2)
    ser.write(b'print(os.listdir("/"))\r\n')
    time.sleep(0.3)
    print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))
    
    ser.close()
    print("\n✓ Upload complete!")

if __name__ == '__main__':
    main()
