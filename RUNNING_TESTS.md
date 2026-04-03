# How to Run Tests - Complete Guide

## Quick Reference

### In PyCharm Terminal
PyCharm automatically activates the `.venv` virtual environment:
```bash
# Simple display test (no touch)
python quick_test.py

# Landscape mode test
python run_test.py test_landscape_mode

# Portrait mode test
python run_test.py test_portrait_mode

# Touch diagnostic
./run_touch_diagnostic.sh
```

### In System Terminal
```bash
cd /home/lpinard/PycharmProjects/CheapBlackDisplay

# Activate virtual environment
source .venv/bin/activate

# Run any test
python quick_test.py
python run_test.py test_display_simple
python run_test.py test_landscape_mode
python run_test.py test_portrait_mode
```

---

## Detailed Instructions

### 1. Running Tests in PyCharm

#### Opening the Terminal in PyCharm
1. Click **View** → **Tool Windows** → **Terminal** (or press `Alt+F12`)
2. The terminal opens at the bottom of the PyCharm window
3. You should be in the project directory: `/home/lpinard/PycharmProjects/CheapBlackDisplay`

#### Running Tests from PyCharm Terminal

**Simple Display Test (recommended first test):**
```bash
python3 quick_test.py
```
- Auto-detects the board on `/dev/ttyACM0` or `/dev/ttyACM1`
- Runs the display + touch test
- Shows colored squares and "Touch Me!" button

**Landscape Mode Test:**
```bash
python3 run_test.py test_landscape_mode
```
- Shows 480x320 display
- Colored squares in corners
- Diagonal lines
- Interactive slider

**Portrait Mode Test:**
```bash
python3 run_test.py test_portrait_mode
```
- Shows 320x480 display
- Same UI elements as landscape but rotated

**Touch Diagnostic:**
```bash
./run_touch_diagnostic.sh
```
- Shows touch coordinates when you touch the screen
- Monitors console for touch events

---

### 2. Running Tests from System Terminal

Open a terminal outside PyCharm:

```bash
# Navigate to project
cd /home/lpinard/PycharmProjects/CheapBlackDisplay

# Run any test
python3 quick_test.py
python3 run_test.py test_display_simple
python3 run_test.py test_landscape_mode
python3 run_test.py test_portrait_mode
```

---

## How to Upload and Run Programs on the Board

### Method 1: Using upload_files.py (Upload Multiple Files)

**Upload all library files and tests:**
```bash
python3 upload_files.py
```

This uploads:
- All files in `ESP32-JC3248W535-Micropython-LVGL-main/lib/` to `/lib` on board
- `task_handler.py` to board root
- All test scripts to board root

**What it does:**
1. Finds the board automatically
2. Uploads each file via raw REPL
3. Shows progress for each file
4. Verifies upload success

### Method 2: Using run_test.py (Upload and Run Single Test)

**Upload and run a specific test:**
```bash
python3 run_test.py test_landscape_mode
```

**What it does:**
1. Finds the board
2. Uploads the specified test file
3. Runs the test immediately
4. Shows output in terminal

### Method 3: Manual Upload (Advanced)

**Upload a single file manually:**
```python
python3 -c "
import serial
import time
import glob

# Find board
port = glob.glob('/dev/ttyACM*')[0]
ser = serial.Serial(port, 115200, timeout=2)
time.sleep(1)

# Read local file
with open('your_file.py', 'rb') as f:
    content = f.read()

# Stop any running program
ser.write(b'\x03\x03')
time.sleep(0.3)
ser.read(ser.in_waiting)

# Enter raw REPL
ser.write(b'\x01')
time.sleep(0.3)
ser.read(ser.in_waiting)

# Write file to board
cmd = f\"f = open('your_file.py', 'wb')\\nf.write({repr(content)})\\nf.close()\\n\"
ser.write(cmd.encode())
ser.write(b'\x04')
time.sleep(0.5)
ser.read(ser.in_waiting)

# Exit raw REPL
ser.write(b'\x02')
time.sleep(0.3)
ser.close()

print('File uploaded!')
"
```

---

## Running Programs on the Board

### Method 1: Using run_test.py
```bash
python3 run_test.py test_name
```
- Automatically uploads and runs the test
- Shows output in terminal

### Method 2: Using Serial REPL

**Connect to REPL:**
```bash
# Using screen
screen /dev/ttyACM0 115200

# Or using minicom
minicom -D /dev/ttyACM0 -b 115200

# Or using Python
python3 -m serial.tools.miniterm /dev/ttyACM0 115200
```

**Run a program in REPL:**
```python
>>> import test_landscape_mode
```

**Stop a running program:**
- Press `Ctrl+C`

**Soft reset the board:**
- Press `Ctrl+D`

**Exit REPL:**
- `screen`: Press `Ctrl+A` then `K` then `Y`
- `minicom`: Press `Ctrl+A` then `X`
- `miniterm`: Press `Ctrl+]`

### Method 3: Using Quick Scripts

**Quick test (auto-detects port):**
```bash
python3 quick_test.py
```

**Run specific test without REPL:**
```bash
python3 -c "
import serial, time, glob
port = glob.glob('/dev/ttyACM*')[0]
ser = serial.Serial(port, 115200, timeout=1)
time.sleep(0.5)
ser.write(b'\x03')  # Stop current program
time.sleep(0.3)
ser.read(ser.in_waiting)
ser.write(b'import test_landscape_mode\r\n')
time.sleep(3)
ser.close()
"
```

---

## Troubleshooting

### Board Not Found
```bash
# Check if board is connected
ls -la /dev/ttyACM*

# Should show: /dev/ttyACM0 or /dev/ttyACM1
```

**If not found:**
1. Check USB cable is plugged in
2. Try a different USB port
3. Check if board has power (LED should be on)

### Display Goes Black
**Workaround:**
1. Unplug USB cable
2. Wait 5 seconds
3. Plug back in
4. Run test again

See `TROUBLESHOOTING.md` for more details.

### Permission Denied
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Log out and log back in for changes to take effect
```

### Port Changes (ACM0 vs ACM1)
The board switches between `/dev/ttyACM0` and `/dev/ttyACM1` after resets.

**Solution:** Use scripts that auto-detect the port:
- `quick_test.py`
- `run_test.py`
- `run_touch_diagnostic.sh`

---

## Available Test Scripts

### On Your Computer (run these)
- `quick_test.py` - Simple test runner with auto port detection
- `run_test.py <test_name>` - Upload and run specific test
- `upload_files.py` - Upload all files to board
- `run_touch_diagnostic.sh` - Touch diagnostic with monitoring

### On the Board (these run on MicroPython)
- `test_display_simple.py` - Display only, no touch
- `test_display_with_touch.py` - Display + touch with button
- `test_landscape_mode.py` - Landscape 480x320 with UI
- `test_portrait_mode.py` - Portrait 320x480 with UI
- `test_touch_raw.py` - Touch coordinate diagnostic
- `test_backlight.py` - Backlight control test
- `task_handler.py` - LVGL task handler (library)

---

## Creating Your Own Programs

### Basic Template
```python
import lvgl as lv
import machine
import lcd_bus
import time
import axs15231b
import axs15231
from i2c import I2C

# Initialize LVGL
lv.init()

# Initialize display (copy from test_display_simple.py)
# ... display setup code ...

# Initialize touch (copy from test_display_with_touch.py)
# ... touch setup code ...

# Create your UI
scr = lv.screen_active()

# Your code here
label = lv.label(scr)
label.set_text("Hello World!")
label.center()

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
```

### Upload and Run Your Program
```bash
# Save as my_program.py
python3 run_test.py my_program
```

---

## PyCharm-Specific Tips

### Run Configuration
You can create a PyCharm run configuration:

1. **Run** → **Edit Configurations**
2. Click **+** → **Python**
3. Name: "Run Display Test"
4. Script path: `/home/lpinard/PycharmProjects/CheapBlackDisplay/quick_test.py`
5. Working directory: `/home/lpinard/PycharmProjects/CheapBlackDisplay`
6. Click **OK**

Now you can run tests with the green play button!

### Terminal Shortcuts
- Open terminal: `Alt+F12`
- New terminal tab: Click **+** in terminal toolbar
- Close terminal: `Ctrl+Shift+F4`
- Clear terminal: Type `clear` or `Ctrl+L`

### Useful PyCharm Features
- **File search**: `Ctrl+Shift+N`
- **Find in files**: `Ctrl+Shift+F`
- **Terminal**: `Alt+F12`
- **Project view**: `Alt+1`

---

## Summary of Commands

```bash
# Quick tests
python3 quick_test.py                    # Simple display + touch test
python3 run_test.py test_landscape_mode  # Landscape mode
python3 run_test.py test_portrait_mode   # Portrait mode

# Upload files
python3 upload_files.py                  # Upload all files

# Diagnostics
./run_touch_diagnostic.sh                # Touch diagnostic
python3 run_test.py test_backlight       # Backlight test

# Check board connection
ls -la /dev/ttyACM*                      # Find board device
```

---

## Next Steps

1. **Start with:** `python3 quick_test.py`
2. **If display is black:** Unplug/replug USB
3. **Try landscape mode:** `python3 run_test.py test_landscape_mode`
4. **Try portrait mode:** `python3 run_test.py test_portrait_mode`
5. **Create your own program** using the template above

For issues, see `TROUBLESHOOTING.md`
