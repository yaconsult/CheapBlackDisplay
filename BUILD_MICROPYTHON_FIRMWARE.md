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
```

### Step 3: Install ESP-IDF

**ESP-IDF is NOT included as a submodule and must be installed separately.**

```bash
# You should be in lvgl_micropython root
cd ~/micropython_build/lvgl_micropython

# Verify you're in the right place
pwd
# Should show: .../micropython_build/lvgl_micropython

# Clone ESP-IDF v5.0.4 (required version)
git clone -b v5.0.4 --recursive https://github.com/espressif/esp-idf.git

# Navigate to ESP-IDF directory
cd esp-idf

# Install ESP-IDF tools for ESP32-S3
# Use python3.11 if you have Python 3.12+
python3.11 ./install.sh esp32s3

# This will download and install:
# - Xtensa ESP32-S3 toolchain
# - ESP32-S3 build tools
# - Python dependencies
# Time: 5-10 minutes

# Verify installation completed
ls -la
# Should show: install.sh, export.sh, components/, tools/, etc.

# Return to lvgl_micropython root
cd ~/micropython_build/lvgl_micropython

# Verify esp-idf directory exists
ls -la esp-idf/
```

**Important:** You must run `source esp-idf/export.sh` before every build to set up the toolchain environment.

---

## Board Configuration

### Understanding the Build System

The lvgl_micropython repository has this structure:

```
~/micropython_build/lvgl_micropython/
├── lib/
│   └── micropython/              # MicroPython submodule
│       └── ports/
│           └── esp32/
│               └── boards/       # <-- Board definitions go here
│                   ├── ESP32_GENERIC/
│                   ├── ESP32_GENERIC_S3/
│                   └── ... (other boards)
├── ext_mod/
└── ...
```

**Important:** Board definitions are NOT in `lvgl_micropython/boards/`, they are in:
```
lvgl_micropython/lib/micropython/ports/esp32/boards/
```

### Step 1: Navigate to the Boards Directory

```bash
# From lvgl_micropython root
cd ~/micropython_build/lvgl_micropython

# Navigate to the ESP32 boards directory
cd lib/micropython/ports/esp32/boards

# Verify you're in the right place
pwd
# Should show: .../lvgl_micropython/lib/micropython/ports/esp32/boards

# List available boards
ls
# Should show: ESP32_GENERIC, ESP32_GENERIC_S3, etc.
```

### Step 2: Create Board Directory

```bash
# Create new board directory (you should still be in the boards/ directory)
mkdir ESP32_GENERIC_S3_JC3248W535

# Create modules subdirectory for drivers
mkdir ESP32_GENERIC_S3_JC3248W535/modules

# Verify structure
ls -la ESP32_GENERIC_S3_JC3248W535/
# Should show the modules/ directory
```

**Note:** All subsequent paths in this guide are relative to:
```
~/micropython_build/lvgl_micropython/lib/micropython/ports/esp32/
```

### Step 3: Create sdkconfig.board

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/sdkconfig.board`

```bash
# Navigate to your board directory
cd ~/micropython_build/lvgl_micropython/lib/micropython/ports/esp32/boards/ESP32_GENERIC_S3_JC3248W535

# Verify you're in the right place
pwd
# Should show: .../boards/ESP32_GENERIC_S3_JC3248W535

# Create the file
nano sdkconfig.board
```

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

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/mpconfigboard.cmake`

```bash
# You should still be in the board directory
pwd
# Should show: .../boards/ESP32_GENERIC_S3_JC3248W535

# Create the file
nano mpconfigboard.cmake
```

Create `mpconfigboard.cmake` with this content:

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

### Step 6: Create mpconfigboard.h

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/mpconfigboard.h`

```bash
# You should still be in the board directory
pwd
# Should show: .../boards/ESP32_GENERIC_S3_JC3248W535

# Create the file
nano mpconfigboard.h
```

Create `mpconfigboard.h` with all pin definitions from Arduino code:

```c
// JC3248W535 Board Configuration
// Based on esp_bsp.h from Arduino demo

#define MICROPY_HW_BOARD_NAME               "ESP32S3 JC3248W535"
#define MICROPY_HW_MCU_NAME                 "ESP32-S3"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable SPIRAM
#define MICROPY_HW_SPIRAM_SIZE              (8 * 1024 * 1024)  // 8MB

// I2C Configuration (from esp_bsp.h)
#define MICROPY_HW_I2C0_NUM                 (0)  // I2C_NUM_0
#define MICROPY_HW_I2C0_SCL                 (8)  // EXAMPLE_PIN_NUM_QSPI_TOUCH_SCL
#define MICROPY_HW_I2C0_SDA                 (4)  // EXAMPLE_PIN_NUM_QSPI_TOUCH_SDA
#define MICROPY_HW_I2C0_SPEED               (400000)  // 400kHz (BSP_I2C_CLK_SPEED_HZ)

// QSPI Display Pins (from esp_bsp.h)
#define MICROPY_HW_LCD_QSPI_HOST            (2)  // SPI2_HOST
#define MICROPY_HW_LCD_CS                   (45)  // EXAMPLE_PIN_NUM_QSPI_CS
#define MICROPY_HW_LCD_PCLK                 (47)  // EXAMPLE_PIN_NUM_QSPI_PCLK
#define MICROPY_HW_LCD_DATA0                (21)  // EXAMPLE_PIN_NUM_QSPI_DATA0
#define MICROPY_HW_LCD_DATA1                (48)  // EXAMPLE_PIN_NUM_QSPI_DATA1
#define MICROPY_HW_LCD_DATA2                (40)  // EXAMPLE_PIN_NUM_QSPI_DATA2
#define MICROPY_HW_LCD_DATA3                (39)  // EXAMPLE_PIN_NUM_QSPI_DATA3
#define MICROPY_HW_LCD_DC                   (8)   // EXAMPLE_PIN_NUM_QSPI_DC
#define MICROPY_HW_LCD_TE                   (38)  // EXAMPLE_PIN_NUM_QSPI_TE (Tear Effect)
#define MICROPY_HW_LCD_BL                   (1)   // EXAMPLE_PIN_NUM_QSPI_BL (Backlight)
#define MICROPY_HW_LCD_RST                  (-1)  // No reset pin

// Display Resolution
#define MICROPY_HW_LCD_H_RES                (320)
#define MICROPY_HW_LCD_V_RES                (480)

// Touch Controller Pins (I2C)
#define MICROPY_HW_TOUCH_SDA                (4)   // EXAMPLE_PIN_NUM_QSPI_TOUCH_SDA
#define MICROPY_HW_TOUCH_SCL                (8)   // EXAMPLE_PIN_NUM_QSPI_TOUCH_SCL
#define MICROPY_HW_TOUCH_RST                (-1)  // No reset pin
#define MICROPY_HW_TOUCH_INT                (-1)  // No interrupt pin
#define MICROPY_HW_TOUCH_I2C_ADDR           (0x3B)  // AXS15231 I2C address

// Backlight PWM Configuration (from esp_bsp.c)
#define MICROPY_HW_LCD_BL_PWM_FREQ          (5000)  // 5kHz
#define MICROPY_HW_LCD_BL_PWM_RESOLUTION    (10)    // 10-bit (0-1023)
```

### Step 7: Create lv_conf.h for LVGL Configuration

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/lv_conf.h`

```bash
# You should still be in the board directory
pwd
# Should show: .../boards/ESP32_GENERIC_S3_JC3248W535

# Create the file
nano lv_conf.h
```

Create `lv_conf.h` with board-specific LVGL settings from Arduino:

```c
/**
 * LVGL Configuration for JC3248W535
 * Based on Arduino demo lv_conf.h
 */

#if 1 /*Set it to "1" to enable content*/

#ifndef LV_CONF_H
#define LV_CONF_H

/*====================
   COLOR SETTINGS
 *====================*/

/* Color depth: 16 (RGB565) - CRITICAL for this display */
#define LV_COLOR_DEPTH 16

/* Swap the 2 bytes of RGB565 color - REQUIRED for QSPI interface */
#define LV_COLOR_16_SWAP 1

/* Enable transparent background support */
#define LV_COLOR_SCREEN_TRANSP 1

/* Color mix rounding */
#define LV_COLOR_MIX_ROUND_OFS 0

/* Chroma key color (pure green) */
#define LV_COLOR_CHROMA_KEY lv_color_hex(0x00ff00)

/*=========================
   MEMORY SETTINGS
 *=========================*/

/* Use custom malloc/free (system malloc) */
#define LV_MEM_CUSTOM 1
#if LV_MEM_CUSTOM == 1
    #define LV_MEM_CUSTOM_INCLUDE <stdlib.h>
    #define LV_MEM_CUSTOM_ALLOC   malloc
    #define LV_MEM_CUSTOM_FREE    free
    #define LV_MEM_CUSTOM_REALLOC realloc
#endif

/* Number of intermediate memory buffers */
#define LV_MEM_BUF_MAX_NUM 16

/* Use standard memcpy/memset */
#define LV_MEMCPY_MEMSET_STD 1

/*====================
   HAL SETTINGS
 *====================*/

/* Display refresh period - 30ms (33 FPS) */
#define LV_DISP_DEF_REFR_PERIOD 30

/* Input device read period - 30ms */
#define LV_INDEV_DEF_READ_PERIOD 30

/* DPI setting for this display */
#define LV_DPI_DEF 130

/*=======================
 * FEATURE CONFIGURATION
 *=======================*/

/* Enable complex draw engine (shadows, gradients, etc.) */
#define LV_DRAW_COMPLEX 1

/* Layer buffer sizes for transparency */
#define LV_LAYER_SIMPLE_BUF_SIZE          (24 * 1024)
#define LV_LAYER_SIMPLE_FALLBACK_BUF_SIZE (3 * 1024)

/* Image cache (disabled for memory savings) */
#define LV_IMG_CACHE_DEF_SIZE 0

/* Gradient settings */
#define LV_GRADIENT_MAX_STOPS 2
#define LV_GRAD_CACHE_DEF_SIZE 0
#define LV_DITHER_GRADIENT 0

/* Rotation buffer */
#define LV_DISP_ROT_MAX_BUF (10*1024)

/* GPU acceleration (none for ESP32-S3) */
#define LV_USE_GPU_ARM2D 0
#define LV_USE_GPU_STM32_DMA2D 0

/*==================
 * FONT USAGE
 *==================*/

/* Enable fonts needed for demos */
#define LV_FONT_MONTSERRAT_8  0
#define LV_FONT_MONTSERRAT_10 0
#define LV_FONT_MONTSERRAT_12 0
#define LV_FONT_MONTSERRAT_14 1
#define LV_FONT_MONTSERRAT_16 1
#define LV_FONT_MONTSERRAT_18 0
#define LV_FONT_MONTSERRAT_20 1
#define LV_FONT_MONTSERRAT_22 0
#define LV_FONT_MONTSERRAT_24 0
#define LV_FONT_MONTSERRAT_26 0
#define LV_FONT_MONTSERRAT_28 0
#define LV_FONT_MONTSERRAT_30 0
#define LV_FONT_MONTSERRAT_32 0
#define LV_FONT_MONTSERRAT_34 0
#define LV_FONT_MONTSERRAT_36 0
#define LV_FONT_MONTSERRAT_38 0
#define LV_FONT_MONTSERRAT_40 0
#define LV_FONT_MONTSERRAT_42 0
#define LV_FONT_MONTSERRAT_44 0
#define LV_FONT_MONTSERRAT_46 0
#define LV_FONT_MONTSERRAT_48 0

/* Default font */
#define LV_FONT_DEFAULT &lv_font_montserrat_14

/*=================
 * THEME USAGE
 *=================*/

/* Enable default theme */
#define LV_USE_THEME_DEFAULT 1
#if LV_USE_THEME_DEFAULT
    /* Dark mode by default */
    #define LV_THEME_DEFAULT_DARK 0
    /* Enable grow on press */
    #define LV_THEME_DEFAULT_GROW 1
    /* Default transition time */
    #define LV_THEME_DEFAULT_TRANSITION_TIME 80
#endif

/*==================
 * WIDGET USAGE
 *==================*/

/* Enable all standard widgets for demos */
#define LV_USE_ARC        1
#define LV_USE_BAR        1
#define LV_USE_BTN        1
#define LV_USE_BTNMATRIX  1
#define LV_USE_CANVAS     1
#define LV_USE_CHECKBOX   1
#define LV_USE_DROPDOWN   1
#define LV_USE_IMG        1
#define LV_USE_LABEL      1
#define LV_USE_LINE       1
#define LV_USE_ROLLER     1
#define LV_USE_SLIDER     1
#define LV_USE_SWITCH     1
#define LV_USE_TEXTAREA   1
#define LV_USE_TABLE      1

/*==================
 * DEMO USAGE
 *==================*/

/* Enable widgets demo */
#define LV_USE_DEMO_WIDGETS 1

#endif /*LV_CONF_H*/
#endif /*End of "Content enable"*/
```

**Key LVGL settings for this board:**
- **LV_COLOR_DEPTH 16** - RGB565 color format
- **LV_COLOR_16_SWAP 1** - CRITICAL: Byte swap for QSPI interface
- **LV_INDEV_DEF_READ_PERIOD 30** - Touch polling every 30ms
- **LV_DPI_DEF 130** - DPI setting for 320x480 display
- **LV_MEM_CUSTOM 1** - Use system malloc (PSRAM available)

### Step 8: Create manifest.py

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/manifest.py`

```bash
# You should still be in the board directory
pwd
# Should show: .../boards/ESP32_GENERIC_S3_JC3248W535

# Create the file
nano manifest.py
```

Create `manifest.py` to include drivers:

```python
include("$(PORT_DIR)/boards/manifest.py")

# Freeze drivers
freeze("$(BOARD_DIR)/modules")
```

### Step 9: Create Partition Table

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/partitions.csv`

```bash
# You should still be in the board directory
pwd
# Should show: .../boards/ESP32_GENERIC_S3_JC3248W535

# Create the file
nano partitions.csv
```

Create `partitions.csv` with this content:

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

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/modules/`

```bash
# Navigate back to the ESP32 port directory
cd ~/micropython_build/lvgl_micropython/lib/micropython/ports/esp32

# Verify you're in the right place
pwd
# Should show: .../lvgl_micropython/lib/micropython/ports/esp32

# Create modules directory if it doesn't exist
mkdir -p boards/ESP32_GENERIC_S3_JC3248W535/modules

# Verify the modules directory exists
ls -la boards/ESP32_GENERIC_S3_JC3248W535/modules/

# Copy driver from existing firmware
cp ~/PycharmProjects/CheapBlackDisplay/ESP32-JC3248W535-Micropython-LVGL-main/lib/axs15231b.py \
   boards/ESP32_GENERIC_S3_JC3248W535/modules/

# Copy initialization
cp ~/PycharmProjects/CheapBlackDisplay/ESP32-JC3248W535-Micropython-LVGL-main/lib/_axs15231b_init.py \
   boards/ESP32_GENERIC_S3_JC3248W535/modules/

# Verify files were copied
ls -la boards/ESP32_GENERIC_S3_JC3248W535/modules/
# Should show: axs15231b.py and _axs15231b_init.py
```

### Step 2: Add Display Configuration

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/modules/axs15231b_config.py`

The Arduino code includes extensive display initialization commands.

```bash
# You should be in the esp32 port directory
cd boards/ESP32_GENERIC_S3_JC3248W535/modules
nano axs15231b_config.py
```

Create `axs15231b_config.py` with this content:

```python
"""
AXS15231B Display Initialization Commands
Derived from Arduino demo esp_bsp.c
"""

# Display initialization commands from C code
# These are the exact commands used by the working Arduino firmware
LCD_INIT_CMDS = [
    # Format: (register, data_bytes, delay_ms)
    (0xBB, bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5A, 0xA5]), 0),
    (0xA0, bytes([0xC0, 0x10, 0x00, 0x02, 0x00, 0x00, 0x04, 0x3F, 0x20, 0x05, 
                  0x3F, 0x3F, 0x00, 0x00, 0x00, 0x00, 0x00]), 0),
    # ... (67 total initialization commands from esp_bsp.c)
    # See full list in Arduino code
]

# I2C Configuration
I2C_SPEED_HZ = 400000  # 400kHz from BSP_I2C_CLK_SPEED_HZ

# Display Resolution
LCD_H_RES = 320
LCD_V_RES = 480

# Backlight PWM
BL_PWM_FREQ = 5000      # 5kHz
BL_PWM_RESOLUTION = 10  # 10-bit (0-1023)

# Tear Effect Configuration (from esp_bsp.c)
# TE pin is GPIO 38, triggers on negative edge
TE_GPIO = 38
TE_INTR_TYPE = 'negedge'  # GPIO_INTR_NEGEDGE

# SPI/QSPI Configuration
QSPI_FREQ_HZ = 80000000  # 80MHz (common for this display)
QSPI_MODE = 3            # SPI mode 3
```

**Note:** The full 67 initialization commands are in `esp_bsp.c` lines 34-67. These configure:
- Display timing
- Gamma correction
- Power settings
- Interface mode (QSPI)
- Color settings

### Step 3: Verify Driver Files

```bash
# Navigate back to esp32 port directory
cd ~/micropython_build/lvgl_micropython/lib/micropython/ports/esp32

# List module files
ls -la boards/ESP32_GENERIC_S3_JC3248W535/modules/

# Should show:
# axs15231b.py
# _axs15231b_init.py
# axs15231b_config.py (new)
```

---

## Add Touch Driver

### Step 1: Copy AXS15231 Touch Driver

```bash
# Make sure you're in the esp32 port directory
cd ~/micropython_build/lvgl_micropython/lib/micropython/ports/esp32

# Copy touch driver
cp ~/PycharmProjects/CheapBlackDisplay/ESP32-JC3248W535-Micropython-LVGL-main/lib/axs15231.py \
   boards/ESP32_GENERIC_S3_JC3248W535/modules/
```

### Step 1b: Add Touch Configuration

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/modules/axs15231_config.py`

```bash
cd boards/ESP32_GENERIC_S3_JC3248W535/modules
nano axs15231_config.py
```

Create `axs15231_config.py` with this content:

```python
"""
AXS15231 Touch Controller Configuration
Derived from Arduino demo esp_bsp.c
"""

# I2C Configuration (from esp_bsp.c bsp_i2c_init)
I2C_NUM = 0              # I2C_NUM_0 (BSP_I2C_NUM)
I2C_SDA = 4              # EXAMPLE_PIN_NUM_QSPI_TOUCH_SDA
I2C_SCL = 8              # EXAMPLE_PIN_NUM_QSPI_TOUCH_SCL
I2C_SPEED = 400000       # 400kHz (BSP_I2C_CLK_SPEED_HZ)
I2C_ADDR = 0x3B          # AXS15231 I2C address

# Touch Configuration (from esp_bsp.c bsp_touch_new)
TOUCH_X_MAX = 320        # EXAMPLE_LCD_QSPI_H_RES
TOUCH_Y_MAX = 480        # EXAMPLE_LCD_QSPI_V_RES
TOUCH_RST_GPIO = -1      # EXAMPLE_PIN_NUM_QSPI_TOUCH_RST (not used)
TOUCH_INT_GPIO = -1      # EXAMPLE_PIN_NUM_QSPI_TOUCH_INT (not used)

# Touch Flags (from esp_bsp.c tp_cfg.flags)
TOUCH_SWAP_XY = False    # swap_xy = 0
TOUCH_MIRROR_X = False   # mirror_x = 0
TOUCH_MIRROR_Y = False   # mirror_y = 0

# Rotation Handling (from esp_bsp.c bsp_touch_process_points_cb)
# The Arduino code handles rotation in bsp_touch_process_points_cb
# For LV_DISP_ROT_90 (our default):
#   x_new = y
#   y_new = x_max - x
```

### Step 2: Add Debug Output to Touch Driver

**This is critical for debugging the touch issue!**

**Location:** `boards/ESP32_GENERIC_S3_JC3248W535/modules/axs15231.py`

```bash
# You should be in the modules directory
nano axs15231.py
```

Edit the file to add debug output:

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

### Step 1: Navigate to Build Directory

```bash
# Navigate to the lvgl_micropython root
cd ~/micropython_build/lvgl_micropython

# Verify you're in the right place
pwd
# Should show: .../micropython_build/lvgl_micropython
```

### Step 2: Initialize Submodules (if not done already)

```bash
# Initialize all submodules
git submodule update --init --recursive
```

### Step 3: Build MicroPython Cross-Compiler

```bash
# You should be in lvgl_micropython root
# Build mpy-cross with warnings disabled (newer GCC versions are strict)
make -C lib/micropython/mpy-cross CFLAGS_EXTRA="-Wno-error"
```

**Note:** The `-Wno-error` flag prevents warnings from being treated as errors. This is needed for newer GCC versions (GCC 12+) that have stricter warnings like "truncates null terminator".

### Step 4: Set Up ESP-IDF Environment

**CRITICAL:** You must source the ESP-IDF environment before building:

```bash
# Navigate to ESP-IDF directory
cd ~/micropython_build/lvgl_micropython/esp-idf

# Source the environment (sets up toolchain paths)
source export.sh

# You should see output like:
# "Done! You can now compile ESP-IDF projects."

# Return to lvgl_micropython root
cd ~/micropython_build/lvgl_micropython

# Verify you're back in the right place
pwd
# Should show: .../micropython_build/lvgl_micropython
```

### Step 5: Build for JC3248W535

```bash
# You should be in lvgl_micropython root
# Build for our custom board
# Use python3.11 if you have Python 3.12+
python3.11 make.py esp32 BOARD=ESP32_GENERIC_S3_JC3248W535 BOARD_VARIANT=SPIRAM_OCT --flash-size=16
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

## Important Configuration Details from Arduino Code

### What We Learned from esp_bsp.c

The Arduino demo provides critical configuration details:

#### 1. I2C Configuration
```c
// From esp_bsp.c lines 96-103
.mode = I2C_MODE_MASTER,
.sda_io_num = 4,              // GPIO 4
.scl_io_num = 8,              // GPIO 8
.sda_pullup_en = DISABLE,     // No internal pullup
.scl_pullup_en = DISABLE,     // No internal pullup
.master.clk_speed = 400000    // 400kHz
```

**Key insight:** No internal pullups - board has external pullups.

#### 2. Display Initialization
```c
// From esp_bsp.c lines 34-67
// 67 initialization commands configure:
// - Display timing and sync
// - Gamma correction curves
// - Power management
// - QSPI interface mode
// - Color depth and format
```

**These commands are critical** - they configure the AXS15231B display controller for proper operation.

#### 3. Tear Effect (TE) Synchronization
```c
// From esp_bsp.c lines 266-304
.te_gpio_num = 38,                    // GPIO 38
.tear_intr_type = GPIO_INTR_NEGEDGE,  // Trigger on falling edge
.time_Tvdl = calculated,              // Display update time
.time_Tvdh = calculated,              // Display idle time
```

**Purpose:** Prevents tearing by synchronizing display updates with panel refresh.

#### 4. Backlight PWM
```c
// From esp_bsp.c lines 125-143
.gpio_num = 1,                        // GPIO 1
.speed_mode = LEDC_LOW_SPEED_MODE,
.timer_num = 1,
.duty_resolution = LEDC_TIMER_10_BIT, // 10-bit (0-1023)
.freq_hz = 5000,                      // 5kHz PWM
```

**Brightness control:** 0-100% maps to 0-1023 duty cycle.

#### 5. Touch Processing
```c
// From esp_bsp.c lines 407-427
// Rotation handled in bsp_touch_process_points_cb
// For 90° rotation:
x_new = y
y_new = x_max - x

// For 180° rotation:
x_new = x_max - x
y_new = y_max - y

// For 270° rotation:
x_new = y_max - y
y_new = x
```

**Important:** Touch coordinates must be rotated to match display rotation.

#### 6. LVGL Integration
```c
// From esp_bsp.c lines 498-511
// Touch added to LVGL with:
lvgl_port_touch_cfg_t touch_cfg = {
    .disp = disp,
    .handle = tp,
    .touch_wait_cb = bsp_touch_sync_cb,  // Synchronization callback
};
return lvgl_port_add_touch(&touch_cfg);
```

**Key:** `touch_wait_cb` provides synchronization between touch interrupts and LVGL polling.

### Configuration Checklist

When building MicroPython firmware, ensure:

- ✅ **I2C speed:** 400kHz (not default 100kHz)
- ✅ **I2C pullups:** Disabled (external pullups on board)
- ✅ **Display init commands:** All 67 commands from esp_bsp.c
- ✅ **Tear effect:** GPIO 38, negative edge trigger
- ✅ **Backlight PWM:** 5kHz, 10-bit resolution
- ✅ **Touch rotation:** Coordinate transformation for display rotation
- ✅ **Touch I2C address:** 0x3B
- ✅ **QSPI mode:** 4-wire QSPI, not standard SPI

### Missing from MicroPython Firmware?

**Possible issues:**
1. **Display init commands** - May be incomplete or incorrect
2. **Tear effect sync** - May not be implemented
3. **Touch synchronization** - `touch_wait_cb` equivalent missing?
4. **I2C speed** - May be using wrong speed
5. **Rotation handling** - Touch coordinates may not be transformed

**This is why touch might not work** - the MicroPython firmware may be missing critical configuration from the Arduino code.

### LVGL Configuration from Arduino

The Arduino `lv_conf.h` provides critical LVGL settings:

#### Color Configuration
```c
// From lv_conf.h lines 27-30
#define LV_COLOR_DEPTH 16          // RGB565 format
#define LV_COLOR_16_SWAP 1         // CRITICAL: Byte swap for QSPI
```

**Why LV_COLOR_16_SWAP is critical:**
- QSPI interface expects bytes in specific order
- Without swap, colors will be wrong (red/blue swapped)
- This is display hardware-specific

#### Display Settings
```c
// From display.h lines 26-38
#define BSP_LCD_COLOR_FORMAT    ESP_LCD_COLOR_FORMAT_RGB565
#define BSP_LCD_BIGENDIAN       1
#define BSP_LCD_BITS_PER_PIXEL  16
#define BSP_LCD_COLOR_SPACE     ESP_LCD_COLOR_SPACE_RGB
#define EXAMPLE_LCD_QSPI_H_RES  320
#define EXAMPLE_LCD_QSPI_V_RES  480
```

#### Timing Configuration
```c
// From lv_conf.h lines 81-84
#define LV_DISP_DEF_REFR_PERIOD 30    // Display refresh every 30ms
#define LV_INDEV_DEF_READ_PERIOD 30   // Touch read every 30ms
#define LV_DPI_DEF 130                // DPI for this display size
```

**Touch polling period is critical:**
- 30ms = ~33 Hz polling rate
- Too fast may overwhelm I2C
- Too slow may miss touches

#### Tear Effect Timing
```c
// From display.h lines 49-50
.time_Tvdl = 13,    // Display update time (ms)
.time_Tvdh = 3,     // Display idle time (ms)
```

**Purpose:** Synchronize display updates to prevent tearing.

#### Memory Configuration
```c
// From lv_conf.h lines 49, 139-140
#define LV_MEM_CUSTOM 1                          // Use system malloc
#define LV_LAYER_SIMPLE_BUF_SIZE (24 * 1024)     // 24KB layer buffer
#define LV_LAYER_SIMPLE_FALLBACK_BUF_SIZE (3 * 1024)  // 3KB fallback
```

**With 8MB PSRAM:** Can use system malloc instead of LVGL's internal allocator.

### LVGL Configuration Checklist

When building MicroPython firmware with LVGL, ensure:

- ✅ **LV_COLOR_DEPTH:** 16 (RGB565)
- ✅ **LV_COLOR_16_SWAP:** 1 (CRITICAL for QSPI)
- ✅ **LV_INDEV_DEF_READ_PERIOD:** 30ms (touch polling)
- ✅ **LV_DISP_DEF_REFR_PERIOD:** 30ms (display refresh)
- ✅ **LV_DPI_DEF:** 130 (for 320x480 display)
- ✅ **LV_MEM_CUSTOM:** 1 (use system malloc with PSRAM)
- ✅ **Buffer sizes:** 24KB layer buffer, 3KB fallback
- ✅ **Fonts:** Enable Montserrat 14, 16, 20 for demos

### Why These Settings Matter

**LV_COLOR_16_SWAP:**
- Most critical setting
- QSPI interface byte order
- Wrong setting = wrong colors

**Touch polling (30ms):**
- Matches display refresh
- Prevents I2C bus overload
- Balances responsiveness vs performance

**Memory settings:**
- PSRAM allows larger buffers
- Smoother animations
- Better performance

**Missing any of these in MicroPython firmware could cause:**
1. Wrong colors (no byte swap)
2. Touch not responding (wrong polling period)
3. Memory errors (wrong buffer sizes)
4. Poor performance (wrong refresh rate)

---

## Debugging MicroPython Firmware

### Important Limitation

**MicroPython does NOT support hardware debugging:**
- ❌ No breakpoints
- ❌ No step-through debugging
- ❌ No variable inspection via debugger
- ❌ Cannot use GDB/OpenOCD
- ❌ Built-in USB JTAG not accessible from Python

### Why No Hardware Debugging?

MicroPython runs as an **interpreter** on top of the firmware:
- Python code is interpreted at runtime
- No direct mapping to machine code
- Hardware debugger sees C firmware, not Python code
- Would need Python-aware debugger (doesn't exist for MicroPython)

### Available Debugging Methods

#### 1. REPL (Read-Eval-Print Loop)

**Interactive Python shell:**
```python
>>> import lvgl as lv
>>> lv.init()
>>> print(lv.version_info())
```

**Pros:**
- Interactive testing
- Immediate feedback
- Inspect objects

**Cons:**
- No breakpoints
- No step-through
- Manual process

#### 2. Print Statements

**Add debug output:**
```python
def _get_coords(self):
    print("_get_coords called", file=sys.stderr)
    state, x, y = self._read_data()
    print(f"Touch: state={state}, x={x}, y={y}", file=sys.stderr)
    return state, x, y
```

**Pros:**
- Simple
- Works everywhere
- Can log to file

**Cons:**
- Clutters code
- Slow for complex issues
- No variable inspection

#### 3. Exception Tracebacks

**Python shows stack trace on errors:**
```python
Traceback (most recent call last):
  File "main.py", line 42, in <module>
  File "axs15231.py", line 67, in _get_coords
AttributeError: 'NoneType' object has no attribute 'x'
```

**Helpful for:**
- Finding crash location
- Understanding call stack
- Identifying error types

#### 4. Logging Module

**Structured logging:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def _get_coords(self):
    logger.debug("_get_coords called")
    logger.debug(f"Touch data: {touch_data}")
    return state, x, y
```

#### 5. Memory Profiling

**Check memory usage:**
```python
import gc
import micropython

# Show memory info
micropython.mem_info()

# Garbage collection
gc.collect()
print(f"Free memory: {gc.mem_free()} bytes")
```

#### 6. Timing Analysis

**Measure execution time:**
```python
import time

start = time.ticks_ms()
# ... code to measure ...
elapsed = time.ticks_diff(time.ticks_ms(), start)
print(f"Took {elapsed} ms")
```

### Debugging Touch Issue in MicroPython

**Since we can't use hardware debugger, use print statements:**

```python
# In axs15231.py
import sys

class AXS15231(pointer_framework.PointerDriver):
    
    def __init__(self, device, touch_cal=None, 
                 startup_rotation=lv.DISPLAY_ROTATION._0, debug=False):
        print("=== AXS15231.__init__ START ===", file=sys.stderr)
        self._device = device
        
        super().__init__(touch_cal, startup_rotation, debug)
        
        print("=== AXS15231.__init__ END ===", file=sys.stderr)
    
    def _read_data(self):
        print("_read_data called", file=sys.stderr)
        
        self._device.write(self._tx_mv)
        self._device.read(buf=self._sensor_data_buffer)
        
        print(f"I2C data: {[hex(b) for b in self._sensor_data_buffer]}", 
              file=sys.stderr)
        
        # ... rest of method ...
        
        return touch_points
    
    def _get_coords(self):
        print("_get_coords called", file=sys.stderr)
        
        touch_data = self._read_data()
        
        if touch_data:
            print(f"Touch detected: x={touch_data[0].x}, y={touch_data[0].y}", 
                  file=sys.stderr)
        else:
            print("No touch detected", file=sys.stderr)
        
        return self.__last_state, self.__last_x, self.__last_y
```

**Watch serial output to see:**
1. Is `__init__` called? (driver created)
2. Is `_get_coords` called? (LVGL polling)
3. Is `_read_data` called? (I2C communication)
4. What data is received? (I2C bytes)

### Comparison: MicroPython vs C/C++ Debugging

| Feature | MicroPython | C/C++ (Arduino/ESP-IDF) |
|---------|-------------|------------------------|
| **Breakpoints** | ❌ No | ✅ Yes |
| **Step-through** | ❌ No | ✅ Yes |
| **Variable inspection** | ⚠️ Print only | ✅ Real-time |
| **Call stack** | ⚠️ Exception only | ✅ Always |
| **Memory viewer** | ❌ No | ✅ Yes |
| **Register viewer** | ❌ No | ✅ Yes |
| **REPL** | ✅ Yes | ❌ No |
| **Interactive testing** | ✅ Yes | ❌ No |
| **Quick iteration** | ✅ Fast | ⚠️ Slower |

### When to Use Each

**Use MicroPython when:**
- Rapid prototyping
- Python expertise
- Quick iteration important
- **Can debug with print statements**

**Use C/C++ when:**
- Need hardware debugging
- Complex bugs
- Performance critical
- **Need breakpoints and step-through**

### Alternative: Debug C Firmware, Use from Python

**Best of both worlds:**

1. **Debug C driver with GDB:**
   - Build custom firmware with debug symbols
   - Set breakpoints in C code
   - Step through pointer_framework
   - Find where LVGL stops calling callbacks

2. **Use from Python:**
   - Once C code works, use from MicroPython
   - Python code is simpler
   - Faster development

**This is why we created BUILD_MICROPYTHON_FIRMWARE.md** - to enable debugging the C firmware layer where the touch bug likely exists.

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
