# PlatformIO Setup Guide for JC3248W535 Board

## Complete Guide for Arduino Development with PlatformIO

This guide provides detailed steps to set up PlatformIO for developing Arduino code on the JC3248W535 board with working display and touch.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install PlatformIO](#install-platformio)
3. [Create New Project](#create-new-project)
4. [Configure platformio.ini](#configure-platformioini)
5. [Set Up Libraries](#set-up-libraries)
6. [Port DEMO_LVGL Code](#port-demo_lvgl-code)
7. [Build and Upload](#build-and-upload)
8. [Troubleshooting](#troubleshooting)
9. [Example Projects](#example-projects)

---

## Prerequisites

### System Requirements

- **OS:** Linux (tested on your system), Windows, or macOS
- **Python:** 3.6 or newer (already have via `.venv`)
- **USB:** Working USB connection to board
- **Permissions:** Access to serial ports

### Disk Space Requirements

**PlatformIO Installation:**
- **PlatformIO Core:** ~500 MB
- **ESP32 Platform:** ~1.5 GB (includes toolchain, frameworks)
- **LVGL Library:** ~50 MB
- **Project files:** ~100 MB
- **Build artifacts:** ~200-500 MB per project
- **Total recommended:** **3-4 GB free space**

**Breakdown:**
```
~/.platformio/          1.5-2 GB  (platforms, toolchains, packages)
~/project/lib/          50-100 MB (libraries)
~/project/.pio/         200-500 MB (build cache, dependencies)
```

**Compared to alternatives:**
- Arduino IDE: ~2-3 GB (IDE + ESP32 support + libraries)
- Arduino CLI: ~1.5-2 GB (toolchain + libraries, no GUI)
- PlatformIO: ~3-4 GB (most comprehensive, includes build cache)

### Check Python Version

```bash
python --version
# Should show Python 3.6+
```

### Serial Port Permissions (Linux)

```bash
# Add your user to dialout group
sudo usermod -a -G dialout $USER

# Log out and back in for changes to take effect
# Or use:
newgrp dialout

# Verify permissions
ls -l /dev/ttyACM*

# On Fedora, you may also need to add to uucp group:
sudo usermod -a -G uucp $USER
```

---

## Install PlatformIO

### Option 1: Install with pip (Recommended)

```bash
# Activate your virtual environment
cd /home/lpinard/PycharmProjects/CheapBlackDisplay
source .venv/bin/activate

# Install PlatformIO
pip install platformio

# Or with uv
uv pip install platformio

# Verify installation
pio --version
```

### Option 2: Install PlatformIO Core Standalone

```bash
# Download and install
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py -o get-platformio.py
python get-platformio.py

# Add to PATH (add to ~/.bashrc)
export PATH=$PATH:~/.platformio/penv/bin

# Verify
pio --version
```

### Option 3: Install PlatformIO IDE Extension (VS Code/PyCharm)

**For VS Code:**
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search "PlatformIO IDE"
4. Click Install

**For PyCharm:**
1. File → Settings → Plugins
2. Search "PlatformIO"
3. Install and restart

---

## Create New Project

### Method 1: Command Line

```bash
cd /home/lpinard/PycharmProjects/CheapBlackDisplay

# Create new PlatformIO project
pio project init --board esp32-s3-devkitc-1 --project-option "framework=arduino"

# This creates:
# - platformio.ini (configuration file)
# - src/ (source code folder)
# - lib/ (libraries folder)
# - include/ (header files)
```

### Method 2: PlatformIO IDE

1. Click PlatformIO icon in sidebar
2. Click "New Project"
3. **Name:** JC3248W535_Demo
4. **Board:** ESP32-S3-DevKitC-1
5. **Framework:** Arduino
6. Click "Finish"

---

## Configure platformio.ini

Create or edit `platformio.ini` with the following configuration:

```ini
[env:esp32-s3-devkitc-1]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino

; Board-specific settings for JC3248W535
board_build.arduino.memory_type = qio_opi
board_build.flash_mode = qio
board_build.flash_size = 16MB
board_build.psram_type = opi
board_upload.flash_size = 16MB

; Upload settings
upload_speed = 921600
monitor_speed = 115200

; Build flags
build_flags = 
    -DBOARD_HAS_PSRAM
    -DARDUINO_ESP32S3_DEV
    -DARDUINO_USB_MODE=1
    -DARDUINO_USB_CDC_ON_BOOT=1
    ; LVGL configuration
    -DLV_CONF_INCLUDE_SIMPLE
    -DLV_CONF_PATH="${PROJECT_DIR}/include/lv_conf.h"
    ; Display configuration
    -DEXAMPLE_LCD_QSPI_H_RES=320
    -DEXAMPLE_LCD_QSPI_V_RES=480
    ; Increase stack size for LVGL
    -DCONFIG_ESP_MAIN_TASK_STACK_SIZE=8192

; Library dependencies
lib_deps = 
    lvgl/lvgl@^8.3.11
    bodmer/TFT_eSPI@^2.5.43

; Extra scripts (optional)
; extra_scripts = pre:scripts/copy_libs.py
```

### Important Configuration Notes

**Memory Type:** `qio_opi`
- This board has Octal SPIRAM
- Must match the memory configuration

**Flash Size:** 16MB
- JC3248W535 has 16MB flash
- Critical for proper operation

**PSRAM:** OPI (Octal)
- Board has 8MB Octal PSRAM
- Required for LVGL frame buffers

**USB CDC:** Enabled
- Allows serial communication over USB
- Required for Serial.print() debugging

---

## Set Up Libraries

### Required Libraries

1. **LVGL** - Graphics library
2. **ESP32 Arduino Core** - ESP32 support
3. **Board-specific drivers** - Display and touch

### Method 1: Copy from Arduino Demo

The easiest way is to copy the working libraries from the Arduino demo:

```bash
cd /home/lpinard/PycharmProjects/CheapBlackDisplay

# Create lib directory if it doesn't exist
mkdir -p lib

# Copy LVGL library
cp -r JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/libraries/lvgl lib/

# Copy board support files
cp -r JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/display.h include/
cp -r JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/esp_bsp.h include/
cp -r JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/esp_bsp.c src/
cp -r JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/lv_port.h include/
cp -r JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/lv_port.c src/
```

### Method 2: Use Library Manager

```bash
# Install LVGL
pio lib install "lvgl/lvgl@^8.3.11"

# Note: Board-specific drivers still need to be copied manually
```

### Create lv_conf.h

Copy LVGL configuration:

```bash
cp JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/lv_conf.h include/
```

Or create `include/lv_conf.h`:

```c
#ifndef LV_CONF_H
#define LV_CONF_H

#define LV_COLOR_DEPTH 16
#define LV_COLOR_16_SWAP 1

#define LV_MEM_CUSTOM 0
#define LV_MEM_SIZE (128U * 1024U)

#define LV_USE_PERF_MONITOR 1
#define LV_USE_MEM_MONITOR 1

#define LV_FONT_MONTSERRAT_12 1
#define LV_FONT_MONTSERRAT_14 1
#define LV_FONT_MONTSERRAT_16 1
#define LV_FONT_MONTSERRAT_20 1

#define LV_USE_DEMO_WIDGETS 1

#endif
```

---

## Port DEMO_LVGL Code

### Project Structure

```
your_project/
├── platformio.ini
├── include/
│   ├── lv_conf.h
│   ├── display.h
│   ├── esp_bsp.h
│   └── lv_port.h
├── src/
│   ├── main.cpp          # Your main code
│   ├── esp_bsp.c         # Board support
│   └── lv_port.c         # LVGL port
└── lib/
    └── lvgl/             # LVGL library
```

### Create src/main.cpp

```cpp
#include <Arduino.h>
#include <lvgl.h>
#include "display.h"
#include "esp_bsp.h"
#include "lv_port.h"

// Rotation: 0, 90, 180, or 270
#define LVGL_PORT_ROTATION_DEGREE (90)

void setup()
{
    Serial.begin(115200);
    Serial.println("JC3248W535 LVGL Demo Starting...");

    // Initialize display and touch
    Serial.println("Initialize panel device");
    bsp_display_cfg_t cfg = {
        .lvgl_port_cfg = ESP_LVGL_PORT_INIT_CONFIG(),
        .buffer_size = EXAMPLE_LCD_QSPI_H_RES * EXAMPLE_LCD_QSPI_V_RES,
#if LVGL_PORT_ROTATION_DEGREE == 90
        .rotate = LV_DISP_ROT_90,
#elif LVGL_PORT_ROTATION_DEGREE == 270
        .rotate = LV_DISP_ROT_270,
#elif LVGL_PORT_ROTATION_DEGREE == 180
        .rotate = LV_DISP_ROT_180,
#else
        .rotate = LV_DISP_ROT_NONE,
#endif
    };

    bsp_display_start_with_config(&cfg);
    bsp_display_backlight_on();

    Serial.println("Create UI");
    bsp_display_lock(0);

    // Run LVGL demo
    lv_demo_widgets();

    bsp_display_unlock();

    Serial.println("Setup complete - touch should work!");
}

void loop()
{
    // LVGL task handler runs in background
    delay(1000);
}
```

---

## Build and Upload

### Build Project

```bash
# Clean build
pio run --target clean

# Build
pio run

# Or specify environment
pio run -e esp32-s3-devkitc-1
```

### Upload to Board

```bash
# Find serial port
ls /dev/ttyACM*

# Upload (auto-detects port)
pio run --target upload

# Or specify port
pio run --target upload --upload-port /dev/ttyACM0
```

### Monitor Serial Output

```bash
# Open serial monitor
pio device monitor

# Or with specific baud rate
pio device monitor -b 115200

# Exit with Ctrl+C
```

### Build, Upload, and Monitor (One Command)

```bash
pio run --target upload && pio device monitor
```

---

## Troubleshooting

### Serial Port Not Found

```bash
# Check if board is connected
lsusb | grep -i esp

# Check serial ports
ls -l /dev/ttyACM*

# Add permissions
sudo chmod 666 /dev/ttyACM0

# Or add to dialout group
sudo usermod -a -G dialout $USER
```

### Upload Failed

```bash
# Hold BOOT button while uploading
# Or try slower baud rate in platformio.ini:
upload_speed = 115200

# Erase flash first
esptool.py --chip esp32s3 --port /dev/ttyACM0 erase_flash
```

### Compilation Errors

**Missing lv_conf.h:**
```bash
# Make sure lv_conf.h is in include/ directory
cp JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/lv_conf.h include/
```

**PSRAM errors:**
```ini
; Add to platformio.ini build_flags:
-DBOARD_HAS_PSRAM
-DCONFIG_SPIRAM_USE_MALLOC=1
```

**Stack overflow:**
```ini
; Increase stack size in platformio.ini:
-DCONFIG_ESP_MAIN_TASK_STACK_SIZE=8192
```

### Display Issues

**Black screen:**
- Check backlight pin configuration
- Verify QSPI pins in display.h
- Check power supply (use good USB cable)

**Wrong colors:**
```c
// In lv_conf.h, try toggling:
#define LV_COLOR_16_SWAP 1  // or 0
```

**Wrong rotation:**
```cpp
// In main.cpp, change:
#define LVGL_PORT_ROTATION_DEGREE (90)  // Try 0, 90, 180, 270
```

### Touch Not Working

**Check I2C pins:**
```c
// In esp_bsp.c, verify:
#define TOUCH_I2C_SDA 4
#define TOUCH_I2C_SCL 8
```

**Enable touch debug:**
```c
// In touch initialization, add:
touch_cfg.debug = true;
```

---

## Example Projects

### Minimal Touch Test

Create `src/main.cpp`:

```cpp
#include <Arduino.h>
#include <lvgl.h>
#include "esp_bsp.h"
#include "lv_port.h"

static int click_count = 0;

static void btn_event_cb(lv_event_t * e)
{
    lv_event_code_t code = lv_event_get_code(e);
    if(code == LV_EVENT_CLICKED) {
        click_count++;
        Serial.printf("Button clicked! Count: %d\n", click_count);
    }
}

void setup()
{
    Serial.begin(115200);
    Serial.println("Touch Test Starting...");

    // Initialize display and touch
    bsp_display_cfg_t cfg = {
        .lvgl_port_cfg = ESP_LVGL_PORT_INIT_CONFIG(),
        .buffer_size = 320 * 480,
        .rotate = LV_DISP_ROT_90,
    };
    bsp_display_start_with_config(&cfg);
    bsp_display_backlight_on();

    bsp_display_lock(0);

    // Create button
    lv_obj_t * btn = lv_btn_create(lv_scr_act());
    lv_obj_set_size(btn, 200, 80);
    lv_obj_center(btn);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_ALL, NULL);

    // Button label
    lv_obj_t * label = lv_label_create(btn);
    lv_label_set_text(label, "Touch Me!");
    lv_obj_center(label);

    bsp_display_unlock();

    Serial.println("Touch the button!");
}

void loop()
{
    delay(1000);
}
```

### Custom UI with Touch

```cpp
#include <Arduino.h>
#include <lvgl.h>
#include "esp_bsp.h"
#include "lv_port.h"

void setup()
{
    Serial.begin(115200);
    
    bsp_display_cfg_t cfg = {
        .lvgl_port_cfg = ESP_LVGL_PORT_INIT_CONFIG(),
        .buffer_size = 320 * 480,
        .rotate = LV_DISP_ROT_90,
    };
    bsp_display_start_with_config(&cfg);
    bsp_display_backlight_on();

    bsp_display_lock(0);

    // Create your custom UI here
    lv_obj_t * scr = lv_scr_act();
    lv_obj_set_style_bg_color(scr, lv_color_hex(0x000000), 0);

    // Title
    lv_obj_t * title = lv_label_create(scr);
    lv_label_set_text(title, "My Custom App");
    lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 20);

    // Add your widgets here
    // Buttons, sliders, charts, etc.

    bsp_display_unlock();
}

void loop()
{
    delay(100);
}
```

---

## Advanced Configuration

### Optimize for Performance

```ini
; In platformio.ini
build_flags = 
    -O2
    -DCORE_DEBUG_LEVEL=0
    -DCONFIG_FREERTOS_HZ=1000
```

### Enable OTA Updates

```ini
upload_protocol = espota
upload_port = 192.168.1.100  ; Board IP address
```

### Use Custom Partition Table

```ini
board_build.partitions = partitions.csv
```

Create `partitions.csv`:
```csv
# Name,   Type, SubType, Offset,  Size
nvs,      data, nvs,     0x9000,  0x5000
otadata,  data, ota,     0xe000,  0x2000
app0,     app,  ota_0,   0x10000, 0x300000
app1,     app,  ota_1,   0x310000,0x300000
spiffs,   data, spiffs,  0x610000,0x9F0000
```

---

## Quick Reference

### Common PlatformIO Commands

```bash
# Initialize project
pio project init -b esp32-s3-devkitc-1

# Install library
pio lib install "library-name"

# Build
pio run

# Upload
pio run -t upload

# Clean
pio run -t clean

# Monitor
pio device monitor

# Update platforms
pio platform update

# List devices
pio device list
```

### Pin Definitions for JC3248W535

```c
// Display QSPI
#define LCD_SCLK  47
#define LCD_DATA0 21
#define LCD_DATA1 48
#define LCD_DATA2 40
#define LCD_DATA3 39
#define LCD_CS    45
#define LCD_DC    8
#define LCD_BL    1

// Touch I2C
#define TOUCH_SDA 4
#define TOUCH_SCL 8
#define TOUCH_ADDR 0x3B

// Audio I2S (if using)
#define I2S_BCLK  7
#define I2S_WS    5
#define I2S_DOUT  6
```

---

## Next Steps

1. **Build and test DEMO_LVGL** - Verify touch works
2. **Create custom UI** - Build your application
3. **Add features** - WiFi, sensors, etc.
4. **Optimize** - Tune performance and memory

## Resources

- **PlatformIO Docs:** https://docs.platformio.org/
- **LVGL Docs:** https://docs.lvgl.io/
- **ESP32-S3 Docs:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/
- **This Board:** JC3248W535EN documentation in your folder

---

*Created: 2026-04-03*
*For: JC3248W535 Board with Arduino + LVGL + Touch*
