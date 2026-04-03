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

1. **Upload files to board**:
   ```bash
   python3 upload_files.py
   ```

2. **Run display test** (no touch):
   ```bash
   python3 run_test.py test_display_simple
   ```

3. **Run touch test** (display + touch):
   ```bash
   python3 run_touch_test.py
   ```

4. **See detailed instructions**: Check `USAGE.md`

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