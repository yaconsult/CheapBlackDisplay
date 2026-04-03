# Cheap Black Display - JC3248W535EN MicroPython Project

## Status: ✅ Display Working!

This is a MicroPython project for the JC3248W535EN board (aka "Cheap Black Display") using LVGL for graphics.

## Hardware
- **Board**: JC3248W535EN (ESP32-S3 with 320x480 display)
- **Purchase Link**: https://www.aliexpress.us/item/3256807380001174.html
- **Connection**: USB via `/dev/ttyACM0`
- **Firmware**: MicroPython 1.25.0 with LVGL 9.2.2

## Project Structure
- `ESP32-JC3248W535-Micropython-LVGL-main/` - GitHub repository code
- `JC3248W535EN/` - Manufacturer's software and documentation
- `task_handler.py` - Custom LVGL task handler module
- `test_display_simple.py` - Working display test (✓ verified)
- `upload_files.py` - Utility to upload files to board
- `run_test.py` - Utility to run test scripts
- `USAGE.md` - Complete usage guide and examples

## Quick Start

### First Time Setup

**Note:** PyCharm automatically creates `.venv` when you open the project.

```bash
# 1. Activate virtual environment (PyCharm terminal does this automatically)
source .venv/bin/activate

# 2. Install dependencies (using uv - faster)
uv pip install -r requirements.txt

# 3. Upload all files to board
python upload_files.py
```

Or if `.venv` doesn't exist, create it first:
```bash
uv venv  # Creates .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### In PyCharm Terminal (Alt+F12)
PyCharm automatically activates `.venv`:
```bash
# Simple display + touch test
python quick_test.py

# Landscape mode (480x320)
python run_test.py test_landscape_mode

# Portrait mode (320x480)
python run_test.py test_portrait_mode
```

### 📖 Complete Documentation
- **`RUNNING_TESTS.md`** - Complete guide for running tests in PyCharm and terminal
- **`USAGE.md`** - Detailed usage examples and code samples
- **`TROUBLESHOOTING.md`** - Known issues and solutions
- **`TOUCH_WORKING.md`** - Touch functionality guide

## Resources
- **GitHub Repository**: https://github.com/de-dh/ESP32-JC3248W535-Micropython-LVGL
- **PyCharm MicroPython Tools**: https://plugins.jetbrains.com/plugin/26227-micropython-tools/
- **Manufacturer Software**: `/home/lpinard/Downloads/JC3248W535EN`

## What's Working
✅ MicroPython REPL access  
✅ Display initialization (QSPI)  
✅ LVGL graphics rendering  
✅ Landscape mode (480x320)  
✅ Portrait mode (320x480)  
✅ Backlight control  
✅ Touch controller (I2C)  
✅ Touch input with LVGL  

## Working Test Scripts
- `test_display_simple.py` - Display only test (no touch)
- `test_display_with_touch.py` - Full display + touch test with button
- `test_landscape_mode.py` - Landscape mode (480x320) with touch and UI elements
- `test_portrait_mode.py` - Portrait mode (320x480) with touch and UI elements
- `run_touch_test.py` - Helper script to run touch test (auto-detects serial port)