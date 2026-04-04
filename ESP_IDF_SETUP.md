# ESP-IDF Setup Guide for JC3248W535

## Complete Guide for Native ESP32 Development

This guide shows how to set up the official Espressif ESP-IDF (ESP32 SDK) for developing native firmware for the JC3248W535 board.

---

## What is ESP-IDF?

**ESP-IDF** (Espressif IoT Development Framework) is the official development framework for ESP32 chips.

**Differences from Arduino:**
- **Lower level:** Direct hardware access, no Arduino abstraction
- **More control:** Full access to all ESP32 features
- **Better performance:** Optimized for ESP32 hardware
- **Professional:** Used in production firmware
- **Steeper learning curve:** More complex than Arduino

---

## Disk Space Requirements

```
ESP-IDF Framework:    ~1.5 GB
Xtensa Toolchain:     ~900 MB
Python Environment:   ~200 MB
Build Cache:          ~500 MB per project
LVGL (optional):      ~50 MB
Total:                ~3-5 GB
```

**Recommended:** 6 GB free space

---

## Prerequisites

### System Packages

```bash
# Ubuntu/Debian
sudo apt-get install git wget flex bison gperf python3 python3-pip \
  python3-venv cmake ninja-build ccache libffi-dev libssl-dev \
  dfu-util libusb-1.0-0

# Additional for USB permissions
sudo usermod -a -G dialout $USER
```

### Check Requirements

```bash
# Python 3.8 or newer
python3 --version

# Git
git --version

# CMake 3.16 or newer
cmake --version

# Free disk space (need 5+ GB)
df -h ~
```

---

## Installation

### Step 1: Clone ESP-IDF

```bash
# Create directory
mkdir -p ~/esp
cd ~/esp

# Clone ESP-IDF v5.1.2 (stable for ESP32-S3)
git clone -b v5.1.2 --recursive https://github.com/espressif/esp-idf.git

# This downloads ~1.5 GB
# Takes 5-10 minutes depending on connection
```

**Why v5.1.2?**
- Stable release
- Good ESP32-S3 support
- Compatible with LVGL v8
- Well-tested

### Step 2: Install Tools

```bash
cd ~/esp/esp-idf

# Install ESP32-S3 toolchain and tools
./install.sh esp32s3

# This downloads ~900 MB
# Takes 10-15 minutes
```

**What gets installed:**
- Xtensa GCC toolchain for ESP32-S3
- OpenOCD for debugging
- CMake, Ninja build tools
- Python packages (esptool, etc.)

**Installation location:** `~/.espressif/`

### Step 3: Set Up Environment

```bash
# Source the setup script
. ~/esp/esp-idf/export.sh

# Verify installation
idf.py --version
```

**Make it permanent:**
```bash
# Add alias to ~/.bashrc
echo 'alias get_idf=". $HOME/esp/esp-idf/export.sh"' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc

# Now you can use:
get_idf
```

---

## Create Project for JC3248W535

### Step 1: Set Up Environment

```bash
# Activate ESP-IDF environment
get_idf
# or
. ~/esp/esp-idf/export.sh
```

### Step 2: Create Project

```bash
cd ~/esp

# Create new project
idf.py create-project jc3248w535_demo

cd jc3248w535_demo

# Set target to ESP32-S3
idf.py set-target esp32s3
```

### Step 3: Configure Project

```bash
# Open configuration menu
idf.py menuconfig
```

**Navigate and configure:**

**1. Serial flasher config →**
- Flash SPI mode: `QIO`
- Flash SPI speed: `80 MHz`
- Flash size: `16 MB`

**2. Component config → ESP System Settings →**
- CPU frequency: `240 MHz`

**3. Component config → ESP32S3-Specific →**
- Support for external, SPI-connected RAM: `[*]`
- SPI RAM config →
  - Mode (QUAD/OCT): `Octal Mode PSRAM`
  - Set RAM clock speed: `80 MHz`

**4. Component config → Driver configurations → SPI configuration →**
- Maximum transfer size: `4096`

**5. Component config → FreeRTOS →**
- Tick rate (Hz): `1000`

**Save and exit:** Press `S` then `Q`

---

## Add LVGL Support

### Step 1: Add LVGL as Component

```bash
cd ~/esp/jc3248w535_demo

# Create components directory
mkdir -p components
cd components

# Clone LVGL v8.3
git clone -b release/v8.3 https://github.com/lvgl/lvgl.git

# Create LVGL component CMakeLists.txt
cat > lvgl/CMakeLists.txt << 'EOF'
idf_component_register(
    SRCS
        "src/core/lv_disp.c"
        "src/core/lv_event.c"
        "src/core/lv_group.c"
        "src/core/lv_indev.c"
        "src/core/lv_obj.c"
        "src/core/lv_obj_class.c"
        "src/core/lv_obj_draw.c"
        "src/core/lv_obj_pos.c"
        "src/core/lv_obj_scroll.c"
        "src/core/lv_obj_style.c"
        "src/core/lv_obj_tree.c"
        "src/core/lv_refr.c"
        "src/core/lv_theme.c"
        # Add more source files as needed
    INCLUDE_DIRS
        "."
        "src"
    REQUIRES
        driver
)
EOF
```

### Step 2: Configure LVGL

```bash
# Copy LVGL config template
cp components/lvgl/lv_conf_template.h main/lv_conf.h

# Edit lv_conf.h
nano main/lv_conf.h
```

**Key settings in lv_conf.h:**
```c
#if 1  // Change from #if 0

#define LV_COLOR_DEPTH 16
#define LV_COLOR_16_SWAP 1

#define LV_MEM_SIZE (128U * 1024U)

#define LV_FONT_MONTSERRAT_14 1
#define LV_FONT_MONTSERRAT_16 1
#define LV_FONT_MONTSERRAT_20 1

#define LV_USE_DEMO_WIDGETS 1
```

---

## Example Code

### main/CMakeLists.txt

```cmake
idf_component_register(
    SRCS "main.c"
    INCLUDE_DIRS "."
    REQUIRES
        driver
        esp_lcd
        lvgl
)
```

### main/main.c (Basic Display + Touch)

```c
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_lcd_panel_io.h"
#include "esp_lcd_panel_ops.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "driver/i2c.h"
#include "esp_log.h"
#include "lvgl.h"

static const char *TAG = "JC3248W535";

// Pin definitions
#define LCD_SCLK  47
#define LCD_DATA0 21
#define LCD_DATA1 48
#define LCD_DATA2 40
#define LCD_DATA3 39
#define LCD_CS    45
#define LCD_DC    8
#define LCD_BL    1

#define TOUCH_I2C_NUM I2C_NUM_0
#define TOUCH_SDA 4
#define TOUCH_SCL 8
#define TOUCH_ADDR 0x3B

#define LCD_H_RES 320
#define LCD_V_RES 480

// LVGL display buffer
static lv_disp_draw_buf_t disp_buf;
static lv_color_t buf1[LCD_H_RES * 40];
static lv_disp_drv_t disp_drv;

// Display flush callback
static void lvgl_flush_cb(lv_disp_drv_t *drv, const lv_area_t *area, lv_color_t *color_map)
{
    // Send data to display
    // ... implementation ...
    
    lv_disp_flush_ready(drv);
}

// Touch read callback
static void lvgl_touch_read_cb(lv_indev_drv_t *drv, lv_indev_data_t *data)
{
    // Read touch data from I2C
    // ... implementation ...
    
    data->state = LV_INDEV_STATE_REL;
}

// LVGL tick task
static void lvgl_tick_task(void *arg)
{
    while (1) {
        lv_tick_inc(10);
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// LVGL timer task
static void lvgl_timer_task(void *arg)
{
    while (1) {
        lv_timer_handler();
        vTaskDelay(pdMS_TO_TICKS(5));
    }
}

void app_main(void)
{
    ESP_LOGI(TAG, "JC3248W535 Demo Starting");
    
    // Initialize LVGL
    lv_init();
    
    // Initialize display
    // ... QSPI display initialization ...
    
    // Initialize touch
    // ... I2C touch initialization ...
    
    // Set up LVGL display driver
    lv_disp_draw_buf_init(&disp_buf, buf1, NULL, LCD_H_RES * 40);
    lv_disp_drv_init(&disp_drv);
    disp_drv.hor_res = LCD_H_RES;
    disp_drv.ver_res = LCD_V_RES;
    disp_drv.flush_cb = lvgl_flush_cb;
    disp_drv.draw_buf = &disp_buf;
    lv_disp_drv_register(&disp_drv);
    
    // Set up LVGL touch driver
    static lv_indev_drv_t indev_drv;
    lv_indev_drv_init(&indev_drv);
    indev_drv.type = LV_INDEV_TYPE_POINTER;
    indev_drv.read_cb = lvgl_touch_read_cb;
    lv_indev_drv_register(&indev_drv);
    
    // Create LVGL tasks
    xTaskCreate(lvgl_tick_task, "lvgl_tick", 2048, NULL, 5, NULL);
    xTaskCreate(lvgl_timer_task, "lvgl_timer", 4096, NULL, 5, NULL);
    
    // Create UI
    lv_obj_t *btn = lv_btn_create(lv_scr_act());
    lv_obj_set_size(btn, 200, 80);
    lv_obj_center(btn);
    
    lv_obj_t *label = lv_label_create(btn);
    lv_label_set_text(label, "ESP-IDF Demo!");
    lv_obj_center(label);
    
    ESP_LOGI(TAG, "Setup complete");
}
```

---

## Build and Flash

### Build Project

```bash
# Clean build
idf.py fullclean

# Build
idf.py build

# Build output in build/ directory
```

**Build time:** 2-5 minutes first time, 30 seconds incremental

### Flash to Board

```bash
# Find port
ls /dev/ttyACM*

# Flash
idf.py -p /dev/ttyACM0 flash

# Or with baud rate
idf.py -p /dev/ttyACM0 -b 460800 flash
```

### Monitor Output

```bash
# Open serial monitor
idf.py -p /dev/ttyACM0 monitor

# Exit with Ctrl+]
```

### Flash and Monitor

```bash
# Do both at once
idf.py -p /dev/ttyACM0 flash monitor
```

---

## Advanced Features

### Custom Partition Table

Create `partitions.csv`:
```csv
# Name,   Type, SubType, Offset,  Size
nvs,      data, nvs,     0x9000,  0x6000
phy_init, data, phy,     0xf000,  0x1000
factory,  app,  factory, 0x10000, 0x300000
storage,  data, spiffs,  0x310000,0xF0000
```

In `CMakeLists.txt`:
```cmake
set(PARTITION_CSV_PATH ${CMAKE_SOURCE_DIR}/partitions.csv)
```

### OTA Updates

```c
#include "esp_ota_ops.h"
#include "esp_http_client.h"

// OTA update from URL
esp_err_t do_ota_update(const char *url) {
    esp_http_client_config_t config = {
        .url = url,
    };
    
    esp_err_t ret = esp_https_ota(&config);
    if (ret == ESP_OK) {
        esp_restart();
    }
    return ret;
}
```

### WiFi Configuration

```c
#include "esp_wifi.h"
#include "esp_event.h"

void wifi_init(void) {
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();
    
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    
    wifi_config_t wifi_config = {
        .sta = {
            .ssid = "YOUR_SSID",
            .password = "YOUR_PASSWORD",
        },
    };
    
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
}
```

---

## Debugging

### Enable Debug Output

In `menuconfig`:
- Component config → Log output → Default log verbosity: `Debug`

### Use GDB Debugger

```bash
# Start OpenOCD
openocd -f board/esp32s3-builtin.cfg

# In another terminal
xtensa-esp32s3-elf-gdb build/jc3248w535_demo.elf
(gdb) target remote :3333
(gdb) monitor reset halt
(gdb) break app_main
(gdb) continue
```

---

## Comparison with Arduino

| Feature | ESP-IDF | Arduino |
|---------|---------|---------|
| **Complexity** | High | Low |
| **Performance** | Maximum | Good |
| **Code Size** | Larger | Smaller |
| **Build Time** | Slower | Faster |
| **Control** | Complete | Limited |
| **Libraries** | ESP-IDF | Arduino + ESP-IDF |
| **Learning Curve** | Steep | Gentle |
| **Production Ready** | Yes | Depends |

---

## Resources

- **ESP-IDF Documentation:** https://docs.espressif.com/projects/esp-idf/
- **ESP32-S3 Datasheet:** https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf
- **LVGL Documentation:** https://docs.lvgl.io/
- **ESP-IDF Examples:** https://github.com/espressif/esp-idf/tree/master/examples

---

## Troubleshooting

### Build Errors

**Error: "CMake not found"**
```bash
sudo apt-get install cmake
```

**Error: "Ninja not found"**
```bash
sudo apt-get install ninja-build
```

### Flash Errors

**Error: "Permission denied"**
```bash
sudo chmod 666 /dev/ttyACM0
```

**Error: "Failed to connect"**
- Hold BOOT button while flashing
- Try slower baud rate: `-b 115200`

### Runtime Issues

**Brownout detector triggered**
- Use good USB cable
- Check power supply
- May need external power

---

*Created: 2026-04-03*
*For: JC3248W535 Board with ESP-IDF*
*Version: ESP-IDF v5.1.2*
