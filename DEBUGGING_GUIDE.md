# Debugging Guide for JC3248W535 (ESP32-S3)

## Complete Guide to Hardware Debugging

The ESP32-S3 has **built-in USB JTAG debugging** - no external hardware debugger needed! This guide shows how to use it with different development environments.

---

## Table of Contents

1. [Overview](#overview)
2. [Hardware Setup](#hardware-setup)
3. [Debugging with PlatformIO IDE](#debugging-with-platformio-ide)
4. [Debugging with PlatformIO CLI](#debugging-with-platformio-cli)
5. [Debugging with ESP-IDF](#debugging-with-esp-idf)
6. [Debugging with VS Code + ESP-IDF](#debugging-with-vs-code--esp-idf)
7. [Common Debugging Tasks](#common-debugging-tasks)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What is JTAG Debugging?

**JTAG (Joint Test Action Group)** is a hardware debugging interface that allows:
- **Breakpoints** - Pause execution at specific lines
- **Step-through** - Execute code line by line
- **Variable inspection** - View/modify variables in real-time
- **Memory viewer** - Inspect RAM/Flash contents
- **Call stack** - See function call hierarchy
- **Register viewer** - Check CPU register values

### ESP32-S3 Built-in USB JTAG

The ESP32-S3 has **USB JTAG built into the chip**:
- No external debugger needed (FTDI, J-Link, etc.)
- Uses the same USB port for programming and debugging
- Supported by OpenOCD
- Works with GDB debugger
- Free and open-source tools

### Debugging Comparison

| Method | Breakpoints | Variables | Step-through | Visual | Setup |
|--------|-------------|-----------|--------------|--------|-------|
| **Serial Print** | ❌ | ❌ | ❌ | ❌ | Easy |
| **PlatformIO CLI** | ✅ | ✅ | ✅ | ❌ | Medium |
| **PlatformIO IDE** | ✅ | ✅ | ✅ | ✅ | Easy |
| **ESP-IDF + GDB** | ✅ | ✅ | ✅ | ❌ | Hard |
| **VS Code + ESP-IDF** | ✅ | ✅ | ✅ | ✅ | Medium |
| **MicroPython** | ❌ | ❌ | ❌ | ⚠️ | Easy |

---

## Hardware Setup

### USB Connection

The JC3248W535 board has **one USB-C port** that provides:
1. **Power** - 5V to board
2. **Serial communication** - UART for programming/console
3. **JTAG debugging** - Hardware debugging interface

**No additional hardware needed!**

### USB Port Detection

When connected, the ESP32-S3 appears as:
- `/dev/ttyACM0` - Serial/UART interface
- **Built-in JTAG** - Detected by OpenOCD automatically

```bash
# Check USB devices
lsusb | grep -i espressif

# Should show:
# Bus 001 Device 010: ID 303a:1001 Espressif USB JTAG/serial debug unit
```

### Permissions

```bash
# Add user to dialout group (Fedora may also need uucp)
sudo usermod -a -G dialout $USER
sudo usermod -a -G uucp $USER  # Fedora only

# Log out and back in, or:
newgrp dialout
```

---

## Debugging with PlatformIO IDE

### Best for: Visual debugging with VS Code

### Step 1: Configure platformio.ini

```ini
[env:esp32-s3-devkitc-1]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino

# Flash configuration
board_build.arduino.memory_type = qio_opi
board_build.flash_size = 16MB
board_build.psram_type = opi

# Debugging configuration
debug_tool = esp-builtin
debug_init_break = tbreak setup
debug_speed = 12000

# Build flags for debugging
build_type = debug
build_flags = 
    -DCORE_DEBUG_LEVEL=5
    -O0
    -g3
```

**Key settings:**
- `debug_tool = esp-builtin` - Use built-in USB JTAG
- `debug_init_break = tbreak setup` - Break at setup()
- `debug_speed = 12000` - JTAG speed (12 MHz)
- `build_type = debug` - Include debug symbols
- `-O0` - No optimization (easier debugging)
- `-g3` - Maximum debug info

### Step 2: Build with Debug Symbols

```bash
# Build in debug mode
pio run

# Upload firmware
pio run -t upload
```

### Step 3: Start Debugging

**Method A: VS Code UI**
1. Open your project in VS Code
2. Set breakpoints (click left of line numbers)
3. Press **F5** or click **Run → Start Debugging**
4. Debugger starts and breaks at `setup()`

**Method B: Debug icon**
1. Click Debug icon in left sidebar
2. Select "PIO Debug (esp32-s3-devkitc-1)"
3. Click green play button

### Step 4: Use Debugger

**Breakpoints:**
- Click in gutter to set/remove breakpoints
- Red dot appears when set

**Step controls:**
- **F10** - Step Over (execute current line)
- **F11** - Step Into (enter function)
- **Shift+F11** - Step Out (exit function)
- **F5** - Continue (run until next breakpoint)

**Variable inspection:**
- Hover over variable to see value
- Variables panel shows local/global variables
- Watch panel for custom expressions

**Call stack:**
- See function call hierarchy
- Click to jump to different stack frames

**Debug console:**
- Execute GDB commands
- Print expressions

### Example Debug Session

```cpp
void setup() {
    Serial.begin(115200);
    
    int x = 10;  // Set breakpoint here
    int y = 20;
    int z = x + y;
    
    Serial.println(z);  // Set breakpoint here
}
```

1. Set breakpoint on `int x = 10;`
2. Press F5 to start debugging
3. Execution pauses at breakpoint
4. Hover over variables to see values
5. Press F10 to step to next line
6. Watch variables update in real-time
7. Press F5 to continue

---

## Debugging with PlatformIO CLI

### Best for: Command-line debugging, automation

### Step 1: Configure platformio.ini

Same as PlatformIO IDE above.

### Step 2: Start Debug Session

```bash
# Start debugger
pio debug

# This will:
# 1. Build firmware with debug symbols
# 2. Upload to board
# 3. Start OpenOCD
# 4. Start GDB
# 5. Connect to target
```

### Step 3: GDB Commands

```gdb
# Set breakpoint
(gdb) break setup
(gdb) break main.cpp:42

# Run program
(gdb) continue

# Step commands
(gdb) next      # Step over
(gdb) step      # Step into
(gdb) finish    # Step out

# Print variables
(gdb) print x
(gdb) print /x myvar  # Print in hex

# Watch variables
(gdb) watch myvar

# View backtrace
(gdb) backtrace

# List source code
(gdb) list

# Info commands
(gdb) info locals
(gdb) info registers
(gdb) info threads

# Memory inspection
(gdb) x/16x 0x3FC00000  # Examine 16 bytes in hex

# Quit
(gdb) quit
```

---

## Debugging with ESP-IDF

### Best for: Native ESP32 development, maximum control

### Step 1: Build with Debug Symbols

```bash
cd ~/esp/jc3248w535_demo

# Configure for debugging
idf.py menuconfig

# Navigate to:
# Component config → Compiler options → Optimization Level → Debug (-Og)
# Save and exit

# Build
idf.py build
```

### Step 2: Flash Firmware

```bash
idf.py -p /dev/ttyACM0 flash
```

### Step 3: Start OpenOCD

```bash
# In one terminal
openocd -f board/esp32s3-builtin.cfg

# Output should show:
# Info : [esp32s3] Target halted, PC=0x...
# Info : Listening on port 3333 for gdb connections
```

### Step 4: Start GDB in Another Terminal

```bash
# Source ESP-IDF environment
. ~/esp/esp-idf/export.sh

# Start GDB
xtensa-esp32s3-elf-gdb build/jc3248w535_demo.elf

# Connect to OpenOCD
(gdb) target remote :3333

# Reset and halt
(gdb) monitor reset halt

# Set breakpoint
(gdb) break app_main

# Continue
(gdb) continue
```

### Step 5: Debug

Use standard GDB commands (see PlatformIO CLI section above).

---

## Debugging with VS Code + ESP-IDF

### Best for: Visual debugging with ESP-IDF projects

### Step 1: Install ESP-IDF Extension

1. Open VS Code
2. Extensions → Search "ESP-IDF"
3. Install "Espressif IDF" extension

### Step 2: Configure launch.json

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "espidf",
            "name": "ESP-IDF Debug",
            "request": "launch",
            "sessionID": "jc3248w535"
        }
    ]
}
```

### Step 3: Start Debugging

1. Set breakpoints in code
2. Press F5 or Run → Start Debugging
3. Visual debugging interface appears

---

## Common Debugging Tasks

### Task 1: Find Crash Location

**Problem:** Code crashes but don't know where

**Solution:**
```gdb
# When crash occurs, GDB shows backtrace
(gdb) backtrace

# Shows call stack leading to crash
# Example output:
# #0  0x42001234 in buggy_function () at main.cpp:42
# #1  0x42005678 in setup () at main.cpp:10
```

### Task 2: Watch Variable Changes

**Problem:** Variable changes unexpectedly

**Solution:**
```gdb
# Set watchpoint
(gdb) watch myVariable

# Program breaks when myVariable changes
# Shows old and new values
```

### Task 3: Inspect Memory

**Problem:** Need to see raw memory contents

**Solution:**
```gdb
# Examine memory at address
(gdb) x/16x 0x3FC00000

# Format: x/[count][format][size] address
# Formats: x=hex, d=decimal, s=string
# Sizes: b=byte, h=halfword, w=word
```

### Task 4: Debug Touch Driver

**Problem:** Touch not working, need to see I2C data

**Solution:**
```cpp
// In axs15231.py or C code
void _read_data() {
    uint8_t data[8];
    i2c_read(data, 8);
    
    // Set breakpoint here
    printf("Touch data: %02x %02x %02x\n", data[0], data[1], data[2]);
}
```

Set breakpoint, touch screen, inspect `data` array.

### Task 5: Debug LVGL Callbacks

**Problem:** LVGL callback not being called

**Solution:**
```cpp
void lvgl_touch_read_cb(lv_indev_drv_t *drv, lv_indev_data_t *data) {
    // Set breakpoint here
    printf("Touch callback called\n");
    
    // If breakpoint never hits, LVGL isn't calling callback
    // Check input device registration
}
```

### Task 6: Monitor FreeRTOS Tasks

**Problem:** Need to see task states

**Solution:**
```gdb
# In GDB with FreeRTOS awareness
(gdb) info threads

# Shows all FreeRTOS tasks:
# * 1    Thread 1 "main" (running)
#   2    Thread 2 "IDLE" (blocked)
#   3    Thread 3 "lvgl_timer" (running)
```

---

## Troubleshooting

### Issue 1: "Could not connect to target"

**Symptoms:**
```
Error: libusb_open() failed with LIBUSB_ERROR_ACCESS
Error: esp_usb_jtag: could not find or open device!
```

**Solution:**
```bash
# Check USB permissions
ls -l /dev/ttyACM0

# Add to groups
sudo usermod -a -G dialout,uucp $USER

# Log out and back in

# Or try with sudo (not recommended)
sudo openocd -f board/esp32s3-builtin.cfg
```

### Issue 2: "Debug symbols not found"

**Symptoms:**
```
No symbol table is loaded
```

**Solution:**
```bash
# Rebuild with debug symbols
# PlatformIO:
build_type = debug
build_flags = -O0 -g3

# ESP-IDF:
idf.py menuconfig
# → Compiler options → Optimization Level → Debug (-Og)
```

### Issue 3: Breakpoints Not Working

**Symptoms:** Breakpoints set but never hit

**Possible causes:**
1. **Code optimized out** - Use `-O0`
2. **Wrong file** - Check file path matches
3. **Code not executed** - Verify code path

**Solution:**
```gdb
# Check if breakpoint is valid
(gdb) info breakpoints

# Try hardware breakpoint
(gdb) hbreak function_name
```

### Issue 4: Variables Optimized Out

**Symptoms:**
```
(gdb) print myvar
$1 = <optimized out>
```

**Solution:**
```bash
# Disable optimization
build_flags = -O0 -g3

# Or mark variable as volatile
volatile int myvar = 0;
```

### Issue 5: OpenOCD Port Already in Use

**Symptoms:**
```
Error: couldn't bind gdb to socket on port 3333
```

**Solution:**
```bash
# Kill existing OpenOCD
pkill openocd

# Or find and kill process
lsof -i :3333
kill <PID>
```

---

## Debugging Comparison Summary

### Serial Print Debugging
**Pros:**
- Simple
- Works everywhere
- No setup

**Cons:**
- No breakpoints
- Can't inspect variables
- Slow for complex issues

### PlatformIO IDE Visual Debugging
**Pros:**
- Visual interface
- Easy to use
- Point-and-click
- Best for beginners

**Cons:**
- Requires VS Code
- More disk space

### ESP-IDF + GDB
**Pros:**
- Maximum control
- Professional tool
- Command-line power

**Cons:**
- Steeper learning curve
- Command-line only
- More complex setup

---

## MicroPython Debugging Limitations

### Important: No Hardware Debugging

**MicroPython does NOT support hardware debugging:**
- ❌ No breakpoints
- ❌ No step-through debugging  
- ❌ No variable inspection via debugger
- ❌ Cannot use GDB/OpenOCD with Python code
- ❌ Built-in USB JTAG not accessible from Python

### Why?

MicroPython is an **interpreter** running on the firmware:
- Python code interpreted at runtime
- No direct mapping to machine code
- Hardware debugger sees C firmware, not Python
- Would need Python-aware debugger (doesn't exist)

### Available Methods

#### 1. Print Statements

```python
def _get_coords(self):
    print("_get_coords called", file=sys.stderr)
    print(f"x={self.x}, y={self.y}", file=sys.stderr)
    return self.state, self.x, self.y
```

#### 2. REPL (Interactive Shell)

```python
>>> import axs15231
>>> touch = axs15231.AXS15231(device)
>>> touch._get_coords()
(0, -1, -1)
```

#### 3. Exception Tracebacks

```python
Traceback (most recent call last):
  File "main.py", line 42, in <module>
  File "axs15231.py", line 67, in _get_coords
AttributeError: 'NoneType' object has no attribute 'x'
```

#### 4. Logging

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Touch data: %s", touch_data)
```

### Debugging the Touch Issue

**For the MicroPython touch bug, use print statements:**

```python
# In axs15231.py
import sys

def _get_coords(self):
    print(">>> _get_coords called", file=sys.stderr)
    # If this never prints, LVGL isn't calling the driver
    
    touch_data = self._read_data()
    if touch_data:
        print(f">>> Touch: x={touch_data[0].x}, y={touch_data[0].y}", 
              file=sys.stderr)
    
    return self.__last_state, self.__last_x, self.__last_y
```

**If `_get_coords` is never called:**
- LVGL v9 isn't polling input device
- Bug is in C firmware (pointer_framework)
- **Need to debug C code with GDB**

### Debugging C Firmware Instead

**To debug the underlying C code:**

1. Build custom firmware (see BUILD_MICROPYTHON_FIRMWARE.md)
2. Add debug output to C code
3. Use GDB to debug pointer_framework
4. Find where LVGL stops calling callbacks
5. Fix C code
6. Rebuild firmware
7. Use from Python

**This is the recommended approach for the touch bug** - the issue is in the C firmware layer, not Python code.

### Comparison

| Capability | MicroPython | C/C++ |
|------------|-------------|-------|
| Breakpoints | ❌ | ✅ |
| Step-through | ❌ | ✅ |
| Variable inspection | Print only | Real-time |
| Hardware debugging | ❌ | ✅ |
| REPL | ✅ | ❌ |
| Quick iteration | ✅ | ⚠️ |

### Recommendation

**For complex bugs like the touch issue:**
1. Use C/C++ with hardware debugging
2. Fix the firmware
3. Then use MicroPython for application code

**For simple Python bugs:**
- Print statements usually sufficient
- REPL for interactive testing
- Exception tracebacks show errors

---

## Resources

- **OpenOCD Manual:** https://openocd.org/doc/html/
- **GDB Manual:** https://sourceware.org/gdb/documentation/
- **ESP-IDF Debugging:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/jtag-debugging/
- **PlatformIO Debugging:** https://docs.platformio.org/en/latest/plus/debugging.html

---

*Created: 2026-04-03*
*For: JC3248W535 Board (ESP32-S3)*
*Hardware: Built-in USB JTAG - No external debugger needed!*
