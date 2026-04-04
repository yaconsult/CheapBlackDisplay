# Installation Options Comparison for JC3248W535

## Complete Disk Space and Installation Guide

This document compares all installation options for flashing code to the JC3248W535 board, including disk space requirements, installation time, and use cases.

---

## Quick Comparison Table

| Method | Disk Space | Install Time | Difficulty | Best For |
|--------|-----------|--------------|------------|----------|
| **esptool.py only** | 10 MB | 1 min | Easy | Flashing pre-compiled binaries |
| **Arduino CLI** | 1.5-2 GB | 10-15 min | Medium | Command-line development |
| **Arduino IDE** | 2-3 GB | 15-20 min | Easy | GUI-based development, testing |
| **PlatformIO CLI** | 3-4 GB | 15-20 min | Medium | Professional development |
| **PlatformIO IDE** | 4-5 GB | 20-30 min | Easy | Full IDE experience |
| **ESP-IDF (Official SDK)** | 3-5 GB | 20-30 min | Hard | Native ESP32 development, maximum control |

---

## Option 1: esptool.py Only (Minimal)

### Use Case
- Only need to flash pre-compiled `.bin` files
- Don't need to compile code
- Minimal disk space available

### Disk Space Requirements
```
esptool.py:           ~10 MB
Python dependencies:  ~5 MB
Total:                ~15 MB
```

### Installation

```bash
# In your virtual environment
source .venv/bin/activate
pip install esptool
# or
uv pip install esptool
```

### What You Can Do
- ✅ Flash factory firmware
- ✅ Flash pre-compiled Arduino binaries
- ✅ Backup/restore firmware
- ✅ Erase flash
- ❌ Cannot compile code
- ❌ Cannot modify source

### Pros
- Minimal disk space
- Fast installation
- Simple to use

### Cons
- Cannot compile your own code
- Need pre-built binaries

---

## Option 2: Arduino CLI (Command Line)

### Use Case
- Command-line development
- Scripting and automation
- No GUI needed
- Moderate disk space

### Disk Space Requirements
```
Arduino CLI:          ~50 MB
ESP32 platform:       ~1.2 GB
  - Toolchain:        ~800 MB
  - Framework:        ~300 MB
  - Tools:            ~100 MB
Libraries (LVGL):     ~200 MB
Build cache:          ~500 MB
Total:                ~1.5-2 GB
```

### Installation

```bash
# Download Arduino CLI
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Add to PATH
export PATH=$PATH:$HOME/bin

# Install ESP32 platform
arduino-cli config init
arduino-cli config add board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
arduino-cli core update-index
arduino-cli core install esp32:esp32@3.0.2

# Install libraries
arduino-cli lib install "lvgl@8.3.11"
```

### What You Can Do
- ✅ Compile Arduino sketches
- ✅ Upload to board
- ✅ Manage libraries
- ✅ Script builds
- ❌ No GUI
- ❌ Manual code editing

### Pros
- Smaller than Arduino IDE
- Good for automation
- Fast compilation

### Cons
- Command-line only
- Need separate text editor
- Less beginner-friendly

---

## Option 3: Arduino IDE (GUI)

### Use Case
- Beginner-friendly
- Visual development
- Quick testing
- Learning Arduino

### Disk Space Requirements
```
Arduino IDE 2.x:      ~600 MB
  - Application:      ~400 MB
  - Runtime:          ~200 MB
ESP32 platform:       ~1.2 GB
  - Toolchain:        ~800 MB
  - Framework:        ~300 MB
  - Tools:            ~100 MB
Libraries (LVGL):     ~200 MB
Build cache:          ~500 MB
Total:                ~2.5-3 GB
```

**Location of files:**
```
~/Arduino/                    (sketches and libraries)
~/.arduino15/                 (IDE settings and platforms)
~/.arduino15/packages/esp32/  (ESP32 platform - largest)
```

### Installation

**Method A: Download AppImage (Recommended)**
```bash
# Check space
df -h ~

# Download (400 MB)
wget https://downloads.arduino.cc/arduino-ide/arduino-ide_2.3.2_Linux_64bit.AppImage
chmod +x arduino-ide_2.3.2_Linux_64bit.AppImage

# Run
./arduino-ide_2.3.2_Linux_64bit.AppImage
```

**Method B: Package Manager**
```bash
# Fedora:
sudo dnf install arduino

# Ubuntu/Debian:
sudo apt install arduino
# Older version (1.8.x), smaller size (~200 MB)
```

### What You Can Do
- ✅ Visual code editor
- ✅ Compile and upload
- ✅ Serial monitor
- ✅ Library manager
- ✅ Board manager
- ✅ Beginner-friendly

### Pros
- Easy to use
- Visual interface
- Built-in examples
- Good for learning

### Cons
- Larger disk space
- Slower than CLI
- Less automation

---

## Option 4: PlatformIO CLI

### Use Case
- Professional development
- Multiple projects
- Advanced features
- CI/CD integration

### Disk Space Requirements
```
PlatformIO Core:      ~500 MB
ESP32 platform:       ~1.5 GB
  - Toolchain:        ~900 MB
  - Framework:        ~400 MB
  - Tools:            ~200 MB
Libraries:            ~100 MB
Build cache:          ~500 MB per project
Total:                ~3-4 GB
```

**Location of files:**
```
~/.platformio/        (all PlatformIO data)
~/project/.pio/       (per-project build cache)
```

### Installation

```bash
# In virtual environment
source .venv/bin/activate

# Install PlatformIO
pip install platformio
# or
uv pip install platformio

# Verify
pio --version

# First project setup downloads platform (~1.5 GB)
pio project init -b esp32-s3-devkitc-1
```

### What You Can Do
- ✅ Advanced project management
- ✅ Multiple frameworks
- ✅ Unit testing
- ✅ Library dependency management
- ✅ CI/CD integration
- ✅ Custom build scripts

### Pros
- Professional features
- Better dependency management
- Faster builds
- Multi-platform support

### Cons
- Larger disk space
- Steeper learning curve
- Command-line focused

---

## Option 5: PlatformIO IDE (VS Code Extension)

### Use Case
- Full IDE experience
- Visual debugging
- Integrated terminal
- Professional development

### Disk Space Requirements
```
VS Code:              ~300 MB
PlatformIO Extension: ~200 MB
PlatformIO Core:      ~500 MB
ESP32 platform:       ~1.5 GB
Libraries:            ~100 MB
Build cache:          ~500 MB per project
Total:                ~4-5 GB
```

### Installation

```bash
# Install VS Code
wget https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64
sudo dpkg -i code_*.deb

# Or use snap
sudo snap install code --classic

# Open VS Code
code

# Install PlatformIO extension:
# 1. Click Extensions (Ctrl+Shift+X)
# 2. Search "PlatformIO IDE"
# 3. Click Install
# 4. Restart VS Code
```

### What You Can Do
- ✅ Full IDE features
- ✅ Visual debugging
- ✅ IntelliSense
- ✅ Git integration
- ✅ Terminal integration
- ✅ Project management

### Pros
- Best development experience
- Visual debugging
- Integrated tools
- Professional features

### Cons
- Largest disk space
- Most complex setup
- Resource intensive

---

## Option 6: ESP-IDF (Official Espressif SDK)

### Use Case
- Native ESP32 development
- Maximum performance and control
- Access to all ESP32 features
- Professional embedded development
- No Arduino abstraction layer

### Disk Space Requirements
```
ESP-IDF Framework:    ~1.5 GB
  - Core framework:   ~800 MB
  - Components:       ~500 MB
  - Tools:            ~200 MB
Xtensa Toolchain:     ~900 MB
Python packages:      ~200 MB
Build cache:          ~500 MB per project
LVGL (if used):       ~50 MB
Total:                ~3-5 GB
```

**Location of files:**
```
~/esp/esp-idf/        (ESP-IDF framework)
~/.espressif/         (toolchain and tools)
~/project/build/      (build artifacts)
```

### Installation

**Prerequisites:**

**For Fedora:**
```bash
sudo dnf install git wget flex bison gperf python3 python3-pip \
  python3-virtualenv cmake ninja-build ccache libffi-devel openssl-devel \
  dfu-util libusb1-devel gcc gcc-c++ make

# USB permissions
sudo usermod -a -G dialout,uucp $USER
```

**For Ubuntu/Debian:**
```bash
sudo apt-get install git wget flex bison gperf python3 python3-pip \
  python3-venv cmake ninja-build ccache libffi-dev libssl-dev \
  dfu-util libusb-1.0-0

# USB permissions
sudo usermod -a -G dialout $USER
```

**Install ESP-IDF:**
```bash
# Create esp directory
mkdir -p ~/esp
cd ~/esp

# Clone ESP-IDF (v5.1 recommended for ESP32-S3)
git clone -b v5.1.2 --recursive https://github.com/espressif/esp-idf.git

# Install tools (downloads ~900 MB)
cd esp-idf
./install.sh esp32s3

# Set up environment
. ./export.sh

# Add to ~/.bashrc for permanent setup
echo 'alias get_idf=". $HOME/esp/esp-idf/export.sh"' >> ~/.bashrc
```

**Installation time:** 20-30 minutes (depending on connection speed)

### Create Project for JC3248W535

```bash
# Set up environment
. ~/esp/esp-idf/export.sh

# Create project from template
cd ~/esp
idf.py create-project jc3248w535_demo

cd jc3248w535_demo

# Configure for ESP32-S3
idf.py set-target esp32s3

# Open menuconfig
idf.py menuconfig
```

**Key Configuration Settings:**

In menuconfig, configure:
1. **Serial flasher config**
   - Flash size: 16 MB
   - Flash mode: QIO
   - Flash frequency: 80 MHz

2. **Component config → ESP32S3-Specific**
   - Support for external, SPI-connected RAM: Yes
   - SPI RAM config → Mode: Octal Mode PSRAM
   - SPI RAM config → Speed: 80 MHz

3. **Component config → Driver configurations**
   - SPI configuration for QSPI display
   - I2C configuration for touch

### Example main.c for Display + Touch

```c
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_lcd_panel_io.h"
#include "esp_lcd_panel_ops.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "driver/i2c.h"
#include "lvgl.h"

// Pin definitions
#define LCD_SCLK  47
#define LCD_DATA0 21
#define LCD_DATA1 48
#define LCD_DATA2 40
#define LCD_DATA3 39
#define LCD_CS    45
#define LCD_DC    8
#define LCD_BL    1

#define TOUCH_SDA 4
#define TOUCH_SCL 8
#define TOUCH_ADDR 0x3B

void app_main(void)
{
    // Initialize LVGL
    lv_init();
    
    // Initialize display (QSPI)
    // ... display initialization code ...
    
    // Initialize touch (I2C)
    // ... touch initialization code ...
    
    // Create UI
    lv_obj_t *btn = lv_btn_create(lv_scr_act());
    lv_obj_t *label = lv_label_create(btn);
    lv_label_set_text(label, "Hello ESP-IDF!");
    
    // LVGL task loop
    while (1) {
        lv_timer_handler();
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
```

### Build and Flash

```bash
# Build project
idf.py build

# Flash to board
idf.py -p /dev/ttyACM0 flash

# Monitor output
idf.py -p /dev/ttyACM0 monitor

# Or do all at once
idf.py -p /dev/ttyACM0 flash monitor
```

### What You Can Do
- ✅ Full ESP32 hardware access
- ✅ Maximum performance
- ✅ FreeRTOS control
- ✅ All ESP32 peripherals
- ✅ WiFi, Bluetooth, etc.
- ✅ Custom partition tables
- ✅ OTA updates
- ❌ More complex than Arduino
- ❌ Steeper learning curve

### Pros
- Maximum control and performance
- Official Espressif support
- Access to all ESP32 features
- Professional development
- Best documentation
- Active community

### Cons
- Largest learning curve
- More code required
- No Arduino libraries
- Complex build system
- Longer development time

### Disk Space Breakdown

**ESP-IDF Components:**
```
esp-idf/components/          ~800 MB
  - FreeRTOS:                ~50 MB
  - WiFi/BT stack:           ~200 MB
  - Driver libraries:        ~300 MB
  - Other components:        ~250 MB

.espressif/tools/            ~900 MB
  - xtensa-gcc:              ~600 MB
  - openocd:                 ~100 MB
  - cmake, ninja:            ~100 MB
  - python packages:         ~100 MB

.espressif/python_env/       ~200 MB
  - Python virtual env:      ~150 MB
  - ESP-IDF Python deps:     ~50 MB

project/build/               ~500 MB
  - Compiled objects:        ~300 MB
  - Libraries:               ~100 MB
  - Binaries:                ~100 MB
```

### Integration with LVGL

**Add LVGL as component:**
```bash
cd ~/esp/jc3248w535_demo
mkdir -p components
cd components

# Clone LVGL
git clone -b release/v8.3 https://github.com/lvgl/lvgl.git

# Create lv_conf.h
cp lvgl/lv_conf_template.h ../main/lv_conf.h
```

**In CMakeLists.txt:**
```cmake
idf_component_register(
    SRCS "main.c"
    INCLUDE_DIRS "."
    REQUIRES lvgl
)
```

### Comparison with Arduino

| Feature | ESP-IDF | Arduino |
|---------|---------|---------|
| **Setup Complexity** | High | Low |
| **Code Complexity** | High | Low |
| **Performance** | Maximum | Good |
| **Control** | Complete | Limited |
| **Libraries** | ESP-IDF only | Arduino + ESP-IDF |
| **Build Time** | Slower | Faster |
| **Debugging** | Advanced | Basic |
| **Documentation** | Excellent | Good |

### When to Use ESP-IDF

**Use ESP-IDF if:**
- Need maximum performance
- Require full hardware control
- Building production firmware
- Need advanced features (custom bootloader, OTA, etc.)
- Professional embedded development
- Want official Espressif support

**Use Arduino if:**
- Rapid prototyping
- Learning/hobby projects
- Need Arduino libraries
- Want simpler development
- Quick testing

---

## Detailed Disk Space Breakdown

### ESP32 Platform Components

**What takes up space in ESP32 support:**

```
Xtensa GCC Toolchain:     ~800-900 MB
  - Compiler (gcc):       ~400 MB
  - Linker (ld):          ~200 MB
  - Libraries (libc):     ~200 MB
  - Tools (objcopy, etc): ~100 MB

ESP32 Arduino Framework:  ~300-400 MB
  - Core libraries:       ~150 MB
  - WiFi/BT libraries:    ~100 MB
  - Peripheral drivers:   ~50 MB
  - Examples:             ~50 MB

Platform Tools:           ~100-200 MB
  - esptool.py:           ~10 MB
  - mkspiffs:             ~20 MB
  - Other utilities:      ~70 MB
```

### Build Cache

**Per-project build artifacts:**

```
Compiled objects (.o):    ~200 MB
Linked binaries (.elf):   ~50 MB
Flash images (.bin):      ~2-5 MB
Dependency cache:         ~100 MB
Temporary files:          ~50 MB

Total per project:        ~400-500 MB
```

**Tip:** Clean build cache regularly:
```bash
# Arduino IDE: Sketch → Clean Build Folder
# Arduino CLI: rm -rf build/
# PlatformIO: pio run -t clean
```

---

## Recommendations by Use Case

### Just Testing (Flash Demo)
**Recommended:** Arduino IDE
- **Space:** 2-3 GB
- **Time:** 15-20 min
- **Difficulty:** Easy
- See: `FLASH_ARDUINO_DEMO.md`

### Learning Arduino
**Recommended:** Arduino IDE
- **Space:** 2-3 GB
- **Time:** 15-20 min
- **Difficulty:** Easy
- Best for beginners

### Professional Development
**Recommended:** PlatformIO CLI or IDE
- **Space:** 3-5 GB
- **Time:** 20-30 min
- **Difficulty:** Medium
- See: `PLATFORMIO_SETUP.md`

### Automation/CI/CD
**Recommended:** Arduino CLI or PlatformIO CLI
- **Space:** 1.5-4 GB
- **Time:** 10-20 min
- **Difficulty:** Medium
- Good for scripts

### Minimal Setup (Flash Only)
**Recommended:** esptool.py
- **Space:** 10 MB
- **Time:** 1 min
- **Difficulty:** Easy
- Cannot compile code

---

## Space-Saving Tips

### Clean Build Cache Regularly

```bash
# Arduino IDE
# Sketch → Clean Build Folder

# Arduino CLI
rm -rf ~/Arduino/build/

# PlatformIO
pio run -t clean
# Or remove entire build folder
rm -rf .pio/
```

### Remove Unused Platforms

```bash
# Arduino CLI
arduino-cli core uninstall <platform>

# PlatformIO
pio platform uninstall <platform>
```

### Use Shared Libraries

```bash
# PlatformIO: Use global lib_dir instead of per-project
# In platformio.ini:
lib_extra_dirs = ~/.platformio/lib
```

### Compress Old Projects

```bash
# Archive completed projects
tar -czf project_backup.tar.gz project_folder/
rm -rf project_folder/
```

---

## Installation Time Estimates

| Step | Arduino IDE | Arduino CLI | PlatformIO |
|------|-------------|-------------|------------|
| Download tool | 5 min | 1 min | 1 min |
| Install tool | 2 min | 1 min | 5 min |
| Download ESP32 | 10 min | 10 min | 10 min |
| Install ESP32 | 3 min | 3 min | 3 min |
| Install libraries | 2 min | 2 min | 2 min |
| **Total** | **~20 min** | **~15 min** | **~20 min** |

*Times based on 10 Mbps connection*

---

## Checking Available Disk Space

### Before Installation

```bash
# Check free space
df -h ~

# Check specific directory
du -sh ~/.arduino15/
du -sh ~/.platformio/

# Find large files
du -h ~ | sort -rh | head -20
```

### After Installation

```bash
# Arduino IDE
du -sh ~/.arduino15/
du -sh ~/Arduino/

# PlatformIO
du -sh ~/.platformio/
du -sh ~/project/.pio/

# Total for all Arduino/PlatformIO
du -sh ~/.arduino15/ ~/.platformio/ ~/Arduino/
```

---

## Minimum Requirements Summary

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Free Disk Space** | 2 GB | 5-6 GB |
| **RAM** | 2 GB | 4-8 GB |
| **Internet Speed** | 1 Mbps | 10 Mbps |
| **USB Ports** | 1 | 2 |

**Note:** ESP-IDF requires more RAM during compilation (4-8 GB recommended)

---

## What to Install for Your Situation

### Situation 1: "I just want to test if touch works"
→ **Arduino IDE** (2-3 GB, easy)
- Follow `FLASH_ARDUINO_DEMO.md`
- Quick test, no development needed

### Situation 2: "I want to develop my own application"
→ **PlatformIO** (3-4 GB, best features)
- Follow `PLATFORMIO_SETUP.md`
- Professional development environment

### Situation 3: "I have limited disk space"
→ **Arduino CLI** (1.5-2 GB, minimal)
- Command-line only
- Can still compile and upload

### Situation 4: "I only need to flash firmware"
→ **esptool.py** (10 MB, minimal)
- Just for flashing binaries
- Cannot compile code

### Situation 5: "I need maximum control and performance"
→ **ESP-IDF** (3-5 GB, advanced)
- Native ESP32 development
- Professional embedded projects
- Maximum hardware access

---

*Created: 2026-04-03*
*Purpose: Help choose installation method based on disk space and needs*
