# JC3248W535EN Display Usage Guide

## Project Status: ✓ Display Working

The ESP32-JC3248W535 board is successfully running MicroPython with LVGL and the display is operational.

## Hardware Setup

- **Board**: JC3248W535EN (ESP32-S3 with 320x480 display)
- **Connection**: USB via `/dev/ttyACM0`
- **Display**: AXS15231B controller, QSPI interface
- **Resolution**: 320x480 (portrait) or 480x320 (landscape with 90° rotation)
- **Firmware**: MicroPython 1.25.0 with LVGL 9.2.2

## Files on Board

### `/lib/` folder:
- `_axs15231b_init.py` - Display initialization routines
- `axs15231.py` - Touch controller driver
- `axs15231b.py` - Display driver
- `lv_config.py` - Portrait mode configuration (320x480)
- `lv_config_90.py` - Landscape mode configuration (480x320)

### Root directory:
- `task_handler.py` - LVGL task handler for timer-based updates
- `test_display_simple.py` - Working simple display test (no touch)
- `test_landscape_mode.py` - Full test with touch (requires touch config fix)
- `test_portrait_mode.py` - Portrait mode test

## Quick Start

### 1. Upload Files to Board
```bash
python3 upload_files.py
```

### 2. Run Display Test
```bash
python3 run_test.py test_display_simple
```

### 3. Connect to REPL Manually
```bash
python3 -c "import serial; ser = serial.Serial('/dev/ttyACM0', 115200); 
import sys; 
while True: 
    if ser.in_waiting: 
        sys.stdout.write(ser.read(ser.in_waiting).decode('utf-8', errors='ignore')); 
        sys.stdout.flush()"
```

Or use a terminal program like `screen`:
```bash
screen /dev/ttyACM0 115200
```

## Display Test Pattern

The `test_display_simple.py` creates:
- **Red square (R)** - Top-left corner
- **Green square (G)** - Top-right corner
- **Blue square (B)** - Bottom-left corner
- **White square (W)** - Bottom-right corner
- **Center text** - "Display Test 480x320"

## Creating Your Own Display Programs

### Minimal Example:
```python
import lvgl as lv
import machine
import lcd_bus
import axs15231b
import time

# Initialize LVGL
lv.init()

# Setup QSPI bus
spi_bus = machine.SPI.Bus(
    host=1,
    sck=47,
    quad_pins=(21, 48, 40, 39)
)

display_bus = lcd_bus.SPIBusFast(
    spi_bus=spi_bus,
    dc=8,
    cs=45,
    freq=40000000,
    spi_mode=3,
    quad=True
)

# Allocate buffer
buf = bytearray(320 * 40 * 2)

# Create display
display = axs15231b.AXS15231B(
    display_bus,
    320, 480,
    frame_buffer1=buf,
    backlight_pin=1,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True,
    backlight_on_state=axs15231b.STATE_PWM
)

display.set_power(True)
display.set_backlight(100)
display.init()
display.set_rotation(lv.DISPLAY_ROTATION._90)  # Landscape mode

# Create UI
scr = lv.screen_active()
label = lv.label(scr)
label.set_text("Hello World!")
label.center()

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
```

## Known Issues

1. **Touch controller configuration** - The `lv_config.py` and `lv_config_90.py` files have issues with touch initialization. Use `test_display_simple.py` as a template for display-only applications.

2. **Import statement** - Line 128 in both config files has `import axs15231 as axs15231` which may cause issues. The touch controller needs debugging.

## Pin Configuration

### Display (QSPI):
- SCLK: GPIO 47
- DATA0-3: GPIO 21, 48, 40, 39
- CS: GPIO 45
- DC: GPIO 8
- Backlight: GPIO 1

### Touch (I2C):
- SDA: GPIO 4
- SCL: GPIO 8
- Address: 0x3B

## Utilities

- `upload_to_board.py` - Upload files to board (initial version)
- `upload_files.py` - Improved file upload utility
- `run_test.py` - Run test scripts and view output

## Next Steps

To add touch functionality:
1. Debug the touch controller initialization in `lv_config.py`
2. Test touch input with the full test scripts
3. Calibrate touch coordinates if needed

## Resources

- GitHub Repo: https://github.com/de-dh/ESP32-JC3248W535-Micropython-LVGL
- LVGL Docs: https://docs.lvgl.io/
- MicroPython Docs: https://docs.micropython.org/
