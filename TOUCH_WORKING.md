# Touch Functionality - Working!

## Status: ✅ Touch is Working

The touch controller (AXS15231) is now fully functional with the display.

## Quick Test

Run the touch test:
```bash
python3 run_touch_test.py
```

This will:
1. Auto-detect the board on `/dev/ttyACM0` or `/dev/ttyACM1`
2. Run `test_display_with_touch.py`
3. Display a test pattern with a "Touch Me!" button

## What You Should See

The display shows:
- **Red square (R)** - Top-left corner
- **Green square (G)** - Top-right corner
- **Blue square (B)** - Bottom-left corner
- **White square (W)** - Bottom-right corner
- **"Touch Test 480x320"** - Center text
- **"Touch Me!" button** - Center of screen

## Testing Touch

1. Touch the "Touch Me!" button on the screen
2. The center text should change from "Touch Test 480x320" to "TOUCHED!"
3. The console will print "Button clicked!"

## Important Notes

### Module Import Issue
The `axs15231` touch driver module had import issues when loaded after soft resets. The fix:
- Import all modules at the top of the file
- Use hardcoded constants instead of importing them from the module
- Constants: `I2C_ADDR = 0x3B`, `BITS = 8`

### Serial Port Changes
The board switches between `/dev/ttyACM0` and `/dev/ttyACM1` after soft resets. Use `run_touch_test.py` which auto-detects the correct port.

## Code Example

```python
import lvgl as lv
import machine
import lcd_bus
import axs15231b
import axs15231
from i2c import I2C
import time

# Initialize LVGL
lv.init()

# Initialize display (QSPI)
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

buf = bytearray(320 * 40 * 2)
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

# Initialize touch (I2C)
i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, 0x3B, 8)
indev = axs15231.AXS15231(touch_i2c, debug=False)

# Create UI with button
scr = lv.screen_active()
btn = lv.button(scr)
btn.set_size(120, 50)
btn.center()

label = lv.label(btn)
label.set_text("Touch Me!")
label.center()

def btn_event_cb(e):
    if e.get_code() == lv.EVENT.CLICKED:
        print("Button clicked!")

btn.add_event_cb(btn_event_cb, lv.EVENT.ALL, None)

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
```

## Pin Configuration

### Touch (I2C):
- **SDA**: GPIO 4
- **SCL**: GPIO 8
- **I2C Address**: 0x3B
- **Bits**: 8

### Display (QSPI):
- **SCLK**: GPIO 47
- **DATA0-3**: GPIO 21, 48, 40, 39
- **CS**: GPIO 45
- **DC**: GPIO 8
- **Backlight**: GPIO 1

## Troubleshooting

If touch doesn't work:

1. **Re-upload axs15231.py**:
   ```bash
   python3 -c "import serial, time, glob; port = glob.glob('/dev/ttyACM*')[0]; ser = serial.Serial(port, 115200, timeout=2); ser.write(b'\x03\x03'); time.sleep(0.3); ser.read(ser.in_waiting); ser.write(b'\x01'); time.sleep(0.3); ser.read(ser.in_waiting); content = open('ESP32-JC3248W535-Micropython-LVGL-main/lib/axs15231.py', 'rb').read(); cmd = f\"f = open('/lib/axs15231.py', 'wb')\\nf.write({repr(content)})\\nf.close()\\n\"; ser.write(cmd.encode()); ser.write(b'\x04'); time.sleep(0.5); ser.read(ser.in_waiting); ser.write(b'\x02'); time.sleep(0.3); ser.close(); print('✓ Re-uploaded')"
   ```

2. **Soft reset the board**:
   - Unplug and replug USB, or
   - Send Ctrl-D via serial

3. **Check module is loaded correctly**:
   ```python
   import axs15231
   print(dir(axs15231))  # Should show 'AXS15231' class
   ```

## Next Steps

Now that touch is working, you can:
- Create interactive UI elements (buttons, sliders, etc.)
- Build custom applications with touch input
- Combine with WiFi for IoT projects
- Add sensors and create dashboards
