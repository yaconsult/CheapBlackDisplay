# Building Custom MicroPython Firmware for JC3248W535

## Complete Guide to Build MicroPython with LVGL and Touch Support

This guide provides detailed instructions for building a custom MicroPython firmware with LVGL v9 support for the JC3248W535 board, including display and touch functionality.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Disk Space Requirements](#disk-space-requirements)
4. [Environment Setup](#environment-setup)
5. [Clone lvgl_micropython](#clone-lvgl_micropython)
6. [Board Configuration](#board-configuration)
7. [Add Display Driver](#add-display-driver)
8. [Add Touch Driver](#add-touch-driver)
9. [Build Firmware](#build-firmware)
10. [Flash and Test](#flash-and-test)
11. [Debugging Touch Issues](#debugging-touch-issues)
12. [Troubleshooting](#troubleshooting)

---

## Overview

### What You'll Build

A custom MicroPython firmware that includes:
- **MicroPython 1.25.0+** - Latest MicroPython
- **LVGL 9.2.2** - Graphics library
- **AXS15231B driver** - QSPI display support
- **AXS15231 driver** - I2C touch support
- **pointer_framework** - Touch integration with LVGL
- **Board-specific configuration** - JC3248W535 settings

### Why Build Custom Firmware?

**Current situation:**
- Existing firmware has touch input device bug
- LVGL v9 doesn't call touch callbacks
- Need to fix or debug the integration

**Goals:**
1. Understand how firmware is built
2. Add debug output to find touch issue
3. Potentially fix touch integration
4. Create working firmware for this board

### Build Time

- **First build:** 30-60 minutes
- **Incremental builds:** 5-10 minutes
- **Total process:** 2-4 hours (including setup and testing)

---

## Prerequisites

### System Requirements

- **OS:** Linux (Fedora, Ubuntu, or other)
- **RAM:** 4 GB minimum, 8 GB recommended
- **Disk Space:** 10-15 GB free
- **Internet:** Stable connection for downloads

### Required Software

**For Fedora:**
```bash
# Install build dependencies
sudo dnf install -y \
    git wget flex bison gperf python3 python3-pip python3-virtualenv \
    cmake ninja-build ccache libffi-devel openssl-devel dfu-util \
    libusb1-devel gcc gcc-c++ make readline-devel ncurses-devel \
    xz-devel tk-devel libxml2-devel xmlsec1-devel \
    libffi-devel xz-devel
```

**For Ubuntu/Debian:**
```bash
# Update package list
sudo apt-get update

# Install build dependencies
sudo apt-get install -y \
    git wget flex bison gperf python3 python3-pip python3-venv \
    cmake ninja-build ccache libffi-dev libssl-dev dfu-util \
    libusb-1.0-0 build-essential libreadline-dev libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev
```

### Python Version

```bash
# Need Python 3.8 or newer
python3 --version

# If older, install Python 3.10
# Fedora:
sudo dnf install python3.10

# Ubuntu/Debian:
sudo apt-get install python3.10 python3.10-venv
```

---

## Disk Space Requirements

### Build Environment

```
lvgl_micropython repo:      ~500 MB
ESP-IDF (included):         ~1.5 GB
Toolchain:                  ~900 MB
Build artifacts:            ~2 GB
MicroPython source:         ~200 MB
LVGL source:                ~100 MB
Total:                      ~5-6 GB

Recommended free space:     10-15 GB
```

### Breakdown

```
~/lvgl_micropython/
├── lib/
│   ├── lv_bindings/        ~100 MB (LVGL bindings)
│   ├── lvgl/               ~100 MB (LVGL library)
│   └── micropython/        ~200 MB (MicroPython)
├── .espressif/             ~900 MB (ESP32 toolchain)
├── esp-idf/                ~1.5 GB (ESP-IDF framework)
└── build/                  ~2 GB (build artifacts)
```

---

## Environment Setup

### Step 1: Install ESP-IDF

The lvgl_micropython project includes ESP-IDF as a submodule, but we need to set it up properly.

```bash
# Create workspace
mkdir -p ~/micropython_build
cd ~/micropython_build

# Install ESP-IDF dependencies
# Fedora:
sudo dnf install -y git wget flex bison gperf python3 \
  python3-pip python3-virtualenv cmake ninja-build ccache \
  libffi-devel openssl-devel dfu-util libusb1-devel

# Ubuntu/Debian:
# sudo apt-get install -y git wget flex bison gperf python3 \
#   python3-pip python3-venv cmake ninja-build ccache \
#   libffi-dev libssl-dev dfu-util libusb-1.0-0
```

### Step 2: Check Available Space

```bash
# Check free space
df -h ~

# Should show at least 10-15 GB free
```

---

## Clone lvgl_micropython

### Step 1: Clone Repository

```bash
cd ~/micropython_build

# Clone the repository (this is the one used by firmware developer)
git clone --recursive https://github.com/lvgl-micropython/lvgl_micropython.git

cd lvgl_micropython

# Checkout the commit used by de-dh (from firmware README)
git checkout af5263c7c0618ebd791e1fe2904fde9bb6234e7c

# Update submodules
git submodule update --init --recursive
```

**This downloads:**
- lvgl_micropython framework
- MicroPython source
- LVGL library
- ESP-IDF framework
- Build tools

**Time:** 10-20 minutes depending on connection

### Step 2: Verify Submodules

```bash
# Check submodules are initialized
git submodule status

# Should show:
# - lib/lv_bindings
# - lib/lvgl
# - lib/micropython
# - esp-idf (if using ESP32)
```

---

## Board Configuration

### Understanding the Build System

The lvgl_micropython project uses:
- **make.py** - Main build script
- **Board definitions** - In `boards/` directory
- **ESP-IDF** - For ESP32 compilation
- **lv_bindings** - LVGL Python bindings

### Step 1: Check Existing Board Definitions

```bash
cd ~/micropython_build/lvgl_micropython

# List available boards
ls boards/

# Look for ESP32-S3 boards
ls boards/ | grep -i s3
```

### Step 2: Create Board Definition for JC3248W535

```bash
# Create board directory
mkdir -p boards/ESP32_GENERIC_S3_JC3248W535

cd boards/ESP32_GENERIC_S3_JC3248W535
```

### Step 3: Create sdkconfig.board

Create `sdkconfig.board` with ESP32-S3 specific settings:

```ini
# ESP32-S3 Configuration for JC3248W535

# Flash configuration
CONFIG_ESPTOOLPY_FLASHSIZE_16MB=y
CONFIG_ESPTOOLPY_FLASHMODE_QIO=y
CONFIG_ESPTOOLPY_FLASHFREQ_80M=y

# PSRAM configuration (Octal PSRAM)
CONFIG_SPIRAM=y
CONFIG_SPIRAM_MODE_OCT=y
CONFIG_SPIRAM_SPEED_80M=y
CONFIG_SPIRAM_USE_MALLOC=y
CONFIG_SPIRAM_MALLOC_ALWAYSINTERNAL=16384

# USB configuration
CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y
CONFIG_ESP_CONSOLE_SECONDARY_NONE=y

# CPU configuration
CONFIG_ESP32S3_DEFAULT_CPU_FREQ_240=y

# Partition table
CONFIG_PARTITION_TABLE_CUSTOM=y
CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions.csv"
```

### Step 4: Create mpconfigboard.cmake

Create `mpconfigboard.cmake`:

```cmake
set(IDF_TARGET esp32s3)

set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    boards/sdkconfig.spiram_sx
    boards/sdkconfig.usb
    boards/ESP32_GENERIC_S3_JC3248W535/sdkconfig.board
)

set(MICROPY_FROZEN_MANIFEST ${MICROPY_BOARD_DIR}/manifest.py)
```

### Step 5: Create mpconfigboard.h

Create `mpconfigboard.h`:

```c
// JC3248W535 Board Configuration

#define MICROPY_HW_BOARD_NAME               "ESP32S3 JC3248W535"
#define MICROPY_HW_MCU_NAME                 "ESP32-S3"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable SPIRAM
#define MICROPY_HW_SPIRAM_SIZE              (8 * 1024 * 1024)  // 8MB

// I2C
#define MICROPY_HW_I2C0_SCL                 (8)
#define MICROPY_HW_I2C0_SDA                 (4)

// SPI (for QSPI display)
#define MICROPY_HW_SPI1_SCK                 (47)
#define MICROPY_HW_SPI1_MOSI                (21)  // DATA0
#define MICROPY_HW_SPI1_MISO                (48)  // DATA1

// Display pins
#define MICROPY_HW_LCD_CS                   (45)
#define MICROPY_HW_LCD_DC                   (8)
#define MICROPY_HW_LCD_BL                   (1)

// Touch pins (I2C)
#define MICROPY_HW_TOUCH_SDA                (4)
#define MICROPY_HW_TOUCH_SCL                (8)
```

### Step 6: Create manifest.py

Create `manifest.py` to include drivers:

```python
include("$(PORT_DIR)/boards/manifest.py")

# Freeze drivers
freeze("$(BOARD_DIR)/modules")
```

### Step 7: Create Partition Table

Create `partitions.csv`:

```csv
# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,  0x6000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 0x300000,
vfs,      data, fat,     0x310000,0xCF0000,
```

---

## Add Display Driver

### Step 1: Copy AXS15231B Driver

```bash
cd ~/micropython_build/lvgl_micropython

# Create drivers directory
mkdir -p boards/ESP32_GENERIC_S3_JC3248W535/modules

# Copy driver from existing firmware
cp ~/PycharmProjects/CheapBlackDisplay/ESP32-JC3248W535-Micropython-LVGL-main/lib/axs15231b.py \
   boards/ESP32_GENERIC_S3_JC3248W535/modules/

# Copy initialization
cp ~/PycharmProjects/CheapBlackDisplay/ESP32-JC3248W535-Micropython-LVGL-main/lib/_axs15231b_init.py \
   boards/ESP32_GENERIC_S3_JC3248W535/modules/
```

### Step 2: Verify Driver Files

```bash
ls -la boards/ESP32_GENERIC_S3_JC3248W535/modules/

# Should show:
# axs15231b.py
# _axs15231b_init.py
```

---

## Add Touch Driver

### Step 1: Copy AXS15231 Touch Driver

```bash
# Copy touch driver
cp ~/PycharmProjects/CheapBlackDisplay/ESP32-JC3248W535-Micropython-LVGL-main/lib/axs15231.py \
   boards/ESP32_GENERIC_S3_JC3248W535/modules/
```

### Step 2: Add Debug Output to Touch Driver

**This is critical for debugging the touch issue!**

Edit `boards/ESP32_GENERIC_S3_JC3248W535/modules/axs15231.py`:

```python
# Add at the top
import sys

class AXS15231(pointer_framework.PointerDriver):

    def __init__(self, device, touch_cal=None, 
                 startup_rotation=lv.DISPLAY_ROTATION._0, debug=False):
        print("AXS15231.__init__ called", file=sys.stderr)
        self._device = device
        super().__init__(touch_cal, startup_rotation, debug)
        
        # ... rest of init ...
        
        print("AXS15231 initialized successfully", file=sys.stderr)

    def _read_data(self):
        print("AXS15231._read_data called", file=sys.stderr)
        # ... existing code ...
        return touch_points

    def _get_coords(self):
        print("AXS15231._get_coords called", file=sys.stderr)
        touch_data = self._read_data()
        
        if touch_data:
            print(f"Touch detected: x={touch_data[0].x}, y={touch_data[0].y}", 
                  file=sys.stderr)
        
        # ... rest of method ...
        return self.__last_state, self.__last_x, self.__last_y
```

**Why add debug output:**
- See if `__init__` is called (driver instantiated)
- See if `_get_coords` is called (LVGL polling driver)
- See if `_read_data` is called (I2C communication)
- Identify where the touch chain breaks

---

## Build Firmware

### Step 1: Set Up Build Environment

```bash
cd ~/micropython_build/lvgl_micropython

# Make build script executable
chmod +x make.py

# Set up ESP-IDF environment
cd esp-idf
./install.sh esp32s3
source export.sh
cd ..
```

### Step 2: Build for JC3248W535

```bash
# Build firmware
python3 make.py esp32 BOARD=ESP32_GENERIC_S3_JC3248W535 BOARD_VARIANT=SPIRAM_OCT --flash-size=16

# This will:
# 1. Configure ESP-IDF
# 2. Build MicroPython
# 3. Build LVGL bindings
# 4. Link everything together
# 5. Create firmware .bin file
```

**Build time:** 30-60 minutes first time

**Output location:**
```
build/ESP32_GENERIC_S3_JC3248W535-SPIRAM_OCT-16/firmware.bin
```

### Step 3: Monitor Build Progress

The build process has several stages:

1. **ESP-IDF configuration** (2-3 min)
2. **MicroPython compilation** (10-15 min)
3. **LVGL compilation** (15-20 min)
4. **Binding generation** (5-10 min)
5. **Linking** (2-3 min)

**Watch for errors:**
- Configuration errors (check sdkconfig)
- Compilation errors (check driver syntax)
- Linking errors (check dependencies)

---

## Flash and Test

### Step 1: Flash Firmware

```bash
cd ~/micropython_build/lvgl_micropython

# Find serial port
ls /dev/ttyACM*

# Flash firmware
python3 -m esptool --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m \
  --erase-all 0x0 build/ESP32_GENERIC_S3_JC3248W535-SPIRAM_OCT-16/firmware.bin
```

### Step 2: Test Basic Functionality

```bash
# Connect to REPL
screen /dev/ttyACM0 115200
# or
picocom /dev/ttyACM0 -b 115200

# Test MicroPython
>>> print("Hello from custom firmware!")

# Test LVGL
>>> import lvgl as lv
>>> lv.init()
>>> print(lv.version_info())

# Test display driver
>>> import axs15231b
>>> print(dir(axs15231b))

# Test touch driver
>>> import axs15231
>>> print(dir(axs15231))
```

### Step 3: Test Touch with Debug Output

Create test file `test_touch_debug.py`:

```python
import lvgl as lv
import machine
import lcd_bus
from i2c import I2C
import sys

print("=== Touch Debug Test ===", file=sys.stderr)

# Initialize LVGL
lv.init()

# Display setup
spi_bus = machine.SPI.Bus(host=1, sck=47, quad_pins=(21, 48, 40, 39))
display_bus = lcd_bus.SPIBusFast(spi_bus=spi_bus, dc=8, cs=45, 
                                  freq=40000000, spi_mode=3, quad=True)

buf = bytearray(320 * 40 * 2)
display = __import__('axs15231b').AXS15231B(
    display_bus, 320, 480, frame_buffer1=buf, backlight_pin=1,
    color_space=lv.COLOR_FORMAT.RGB565, rgb565_byte_swap=True,
    backlight_on_state=__import__('axs15231b').STATE_PWM
)

display.set_power(True)
display.set_backlight(100)
display.init()
display.set_rotation(lv.DISPLAY_ROTATION._90)

print("Display initialized", file=sys.stderr)

# Touch setup
i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, 0x3B, 8)

print("Creating touch driver...", file=sys.stderr)
import axs15231
indev = axs15231.AXS15231(touch_i2c, debug=True)
print("Touch driver created", file=sys.stderr)

# Create simple UI
scr = lv.screen_active()
btn = lv.button(scr)
btn.set_size(200, 80)
btn.center()

label = lv.label(btn)
label.set_text("Touch Me!")
label.center()

print("UI created", file=sys.stderr)
print("Watch for _get_coords calls when touching screen", file=sys.stderr)

# Main loop
import time
while True:
    lv.timer_handler()
    time.sleep_ms(5)
```

Upload and run:
```bash
# Upload test file
# ... use your upload method ...

# Run and watch debug output
import test_touch_debug
```

**Watch for:**
- `AXS15231.__init__ called` - Driver initialized
- `AXS15231._get_coords called` - LVGL polling (THIS IS KEY!)
- `Touch detected: x=..., y=...` - Touch data read

**If you DON'T see `_get_coords called`:**
- LVGL is not polling the input device
- This confirms the bug
- Need to investigate pointer_framework registration

---

## Debugging Touch Issues

### Issue 1: LVGL Not Calling _get_coords

**Symptom:** No `_get_coords called` messages when touching

**Possible causes:**
1. Input device not registered with LVGL
2. LVGL task not running
3. pointer_framework bug in LVGL v9

**Debug steps:**

#### Check pointer_framework Source

```bash
cd ~/micropython_build/lvgl_micropython

# Find pointer_framework
find . -name "pointer_framework.py"

# Examine it
cat ./lib/lv_bindings/driver/generic/pointer_framework.py
```

Look for:
- How `PointerDriver` registers with LVGL
- If it calls `lv.indev_create()`
- If it sets up callbacks correctly

#### Add Debug to pointer_framework

Edit `lib/lv_bindings/driver/generic/pointer_framework.py`:

```python
import sys

class PointerDriver:
    def __init__(self, touch_cal=None, startup_rotation=lv.DISPLAY_ROTATION._0, debug=False):
        print("PointerDriver.__init__ called", file=sys.stderr)
        
        # ... existing code ...
        
        # Look for input device registration
        # Add debug output before/after registration
        print("Registering input device with LVGL...", file=sys.stderr)
        # ... registration code ...
        print("Input device registered", file=sys.stderr)
```

#### Rebuild with Debug

```bash
# Rebuild firmware with debug output
python3 make.py esp32 BOARD=ESP32_GENERIC_S3_JC3248W535 BOARD_VARIANT=SPIRAM_OCT --flash-size=16 clean
python3 make.py esp32 BOARD=ESP32_GENERIC_S3_JC3248W535 BOARD_VARIANT=SPIRAM_OCT --flash-size=16

# Flash and test again
```

### Issue 2: Input Device Registration

**Check if LVGL v9 API is used correctly:**

In pointer_framework, look for:

**LVGL v8 (old):**
```python
lv.indev_drv_register(drv)
```

**LVGL v9 (new):**
```python
indev = lv.indev_create()
indev.set_type(lv.INDEV_TYPE.POINTER)
indev.set_read_cb(callback)
```

**If using v8 API with v9 LVGL:**
- This is the bug!
- Need to update pointer_framework to v9 API

### Issue 3: Manual Fix

If pointer_framework is broken, bypass it:

Edit `axs15231.py` to NOT use pointer_framework:

```python
import lvgl as lv

class AXS15231:  # Don't inherit from PointerDriver
    def __init__(self, device, debug=False):
        self._device = device
        self._debug = debug
        
        # ... init code ...
        
        # Manually register with LVGL v9
        self._indev = lv.indev_create()
        self._indev.set_type(lv.INDEV_TYPE.POINTER)
        self._indev.set_read_cb(self._lvgl_read_cb)
        
        print("Touch manually registered with LVGL v9", file=sys.stderr)
    
    def _lvgl_read_cb(self, drv, data):
        """LVGL callback - called by LVGL task"""
        state, x, y = self._get_coords()
        data.point.x = x
        data.point.y = y
        data.state = lv.INDEV_STATE.PRESSED if state == self.PRESSED else lv.INDEV_STATE.RELEASED
        return False
    
    # ... rest of class ...
```

---

## Troubleshooting

### Build Errors

#### Error: "ESP-IDF not found"

```bash
cd ~/micropython_build/lvgl_micropython/esp-idf
./install.sh esp32s3
source export.sh
```

#### Error: "Submodule not initialized"

```bash
git submodule update --init --recursive
```

#### Error: "Python version too old"

```bash
# Install Python 3.10
# Fedora:
sudo dnf install python3.10

# Ubuntu/Debian:
sudo apt-get install python3.10 python3.10-venv

# Use it for build
python3.10 make.py ...
```

#### Error: "Out of memory during build"

```bash
# Reduce parallel jobs
export MAKEFLAGS="-j2"  # Use only 2 cores

# Or increase swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Flash Errors

#### Error: "Failed to connect"

```bash
# Hold BOOT button while flashing
# Or try slower baud rate
python3 -m esptool ... -b 115200 ...
```

#### Error: "Permission denied"

```bash
sudo chmod 666 /dev/ttyACM0
# Or add to dialout group
sudo usermod -a -G dialout $USER
```

### Runtime Errors

#### Error: "ImportError: no module named axs15231"

```bash
# Driver not frozen into firmware
# Check manifest.py includes modules directory
# Rebuild firmware
```

#### Error: "MemoryError"

```bash
# Not enough PSRAM
# Check sdkconfig has SPIRAM enabled
# Check SPIRAM_OCT mode selected
```

---

## Advanced: Fixing pointer_framework

If you want to fix the pointer_framework for LVGL v9:

### Step 1: Locate pointer_framework

```bash
cd ~/micropython_build/lvgl_micropython
find . -name "pointer_framework.py"
```

### Step 2: Update for LVGL v9

Edit the file to use LVGL v9 API:

```python
class PointerDriver:
    def __init__(self, touch_cal=None, startup_rotation=lv.DISPLAY_ROTATION._0, debug=False):
        self._debug = debug
        self._touch_cal = touch_cal
        self._rotation = startup_rotation
        
        # LVGL v9 API - create input device
        self._indev = lv.indev_create()
        self._indev.set_type(lv.INDEV_TYPE.POINTER)
        self._indev.set_read_cb(self._read_cb_wrapper)
        
        if debug:
            print("PointerDriver registered with LVGL v9")
    
    def _read_cb_wrapper(self, drv, data):
        """Wrapper called by LVGL"""
        if self._debug:
            print("PointerDriver._read_cb_wrapper called")
        
        # Call subclass _get_coords
        state, x, y = self._get_coords()
        
        # Apply calibration if needed
        if self._touch_cal:
            x, y = self._touch_cal(x, y)
        
        # Update LVGL data
        data.point.x = x
        data.point.y = y
        data.state = lv.INDEV_STATE.PRESSED if state == self.PRESSED else lv.INDEV_STATE.RELEASED
        
        return False
    
    def _get_coords(self):
        """Override in subclass"""
        raise NotImplementedError
```

### Step 3: Rebuild and Test

```bash
# Clean build
python3 make.py esp32 BOARD=ESP32_GENERIC_S3_JC3248W535 BOARD_VARIANT=SPIRAM_OCT --flash-size=16 clean

# Build with fix
python3 make.py esp32 BOARD=ESP32_GENERIC_S3_JC3248W535 BOARD_VARIANT=SPIRAM_OCT --flash-size=16

# Flash and test
```

---

## Summary

### What You've Built

- Custom MicroPython firmware for JC3248W535
- LVGL v9 graphics support
- Display driver (AXS15231B QSPI)
- Touch driver (AXS15231 I2C)
- Debug output to diagnose touch issues

### Next Steps

1. **Test the firmware** - See if touch works
2. **Check debug output** - Identify where touch breaks
3. **Fix pointer_framework** - Update to LVGL v9 API if needed
4. **Share findings** - Report to firmware developer
5. **Contribute fix** - Submit PR if you fix it

### Resources

- **lvgl_micropython:** https://github.com/lvgl-micropython/lvgl_micropython
- **MicroPython docs:** https://docs.micropython.org/
- **LVGL docs:** https://docs.lvgl.io/
- **ESP-IDF docs:** https://docs.espressif.com/projects/esp-idf/

---

*Created: 2026-04-03*
*Purpose: Build custom MicroPython firmware with working touch*
*Difficulty: Advanced*
