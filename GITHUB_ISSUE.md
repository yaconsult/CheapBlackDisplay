# GitHub Issue for Firmware Developer

## Issue Title

Touch input device not working - LVGL never calls touch callbacks

## Issue Body

### Summary

Touch hardware is fully functional (verified via direct I2C polling), but LVGL v9 in the MicroPython firmware never calls the registered touch input device callbacks, making touch completely non-functional.

### Environment

- **Board:** JC3248W535EN
- **Firmware:** ESP32-JC3248W535-Micropython-LVGL (from this repository)
- **MicroPython:** 1.25.0
- **LVGL:** 9.2.2
- **Firmware Build:** lvgl_micropython commit af5263c
- **Touch Controller:** AXS15231 (I2C address 0x3B)

### Expected Behavior

When using the touch driver with LVGL:
1. Touch controller initializes successfully ✅
2. Input device registers with LVGL ✅
3. LVGL's task system polls the touch driver ❌ **NOT HAPPENING**
4. Touch events trigger UI responses ❌ **NOT HAPPENING**

### Actual Behavior

- Touch controller initializes without errors
- `pointer_framework.PointerDriver` can be instantiated
- LVGL never calls `_get_coords()` or `_read_data()` methods
- No touch events reach LVGL
- UI elements don't respond to touch

### Hardware Verification

Touch hardware is **100% functional**. Verified by direct I2C polling:

```python
# Direct I2C test - WORKS PERFECTLY
from i2c import I2C

i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, 0x3B, 8)

tx_buf = bytearray([0xB5, 0xAB, 0xA5, 0x5A, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00])
rx_buf = bytearray(8)

while True:
    touch_i2c.write(tx_buf)
    touch_i2c.read(buf=rx_buf)
    
    num_points = rx_buf[1]
    if num_points > 0:
        x = ((rx_buf[2] & 0x0F) << 8) | rx_buf[3]
        y = ((rx_buf[4] & 0x0F) << 8) | rx_buf[5]
        print(f"Touch: X={x}, Y={y}")  # WORKS - hundreds of touches captured
```

**Result:** Successfully captured hundreds of accurate touch coordinates. Touch hardware is perfect.

### Attempted Solutions (All Failed)

#### 1. Standard pointer_framework Approach
```python
import axs15231
from i2c import I2C

i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, 0x3B, 8)
indev = axs15231.AXS15231(touch_i2c, debug=True)
```
**Result:** No debug output, LVGL never calls driver methods.

#### 2. Manual Input Device Registration
```python
def touch_read_cb(drv, data):
    # Read touch and update data
    return False

indev = lv.indev_create()
indev.set_type(lv.INDEV_TYPE.POINTER)
indev.set_read_cb(touch_read_cb)
```
**Result:** Callback never called by LVGL.

#### 3. Background Threading
```python
import _thread

def touch_polling_thread():
    while True:
        read_touch_and_update_state()
        time.sleep_ms(10)

_thread.start_new_thread(touch_polling_thread, ())
```
**Result:** Thread runs, state updates, but LVGL callback still never called.

#### 4. Forum Fixes Attempted

Based on https://forum.lvgl.io/t/jc3248w535en-event-problem/21586:

- ❌ Monkey patch `_get_coords()` override
- ❌ 20ms timing fix for sensor reads
- ❌ Thread worker pattern

**None of these work because LVGL never calls the callbacks in the first place.**

### Root Cause Analysis

The issue appears to be in LVGL v9's input device integration with MicroPython:

1. **LVGL v8 (Arduino) - WORKS:**
   - Uses `lv_indev_drv_register()`
   - LVGL task continuously polls input devices
   - Touch works perfectly

2. **LVGL v9 (MicroPython) - BROKEN:**
   - Uses `lv.indev_create()`
   - Input device can be registered
   - **LVGL task never polls input devices**
   - Callbacks never called

**Hypothesis:** LVGL v9 migration changed input device polling mechanism, and the MicroPython bindings weren't fully updated to match.

### Comparison with Arduino

Arduino firmware (`JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/`) has **working touch** using LVGL v8:

```c
// Arduino - WORKING
static void lvgl_port_touchpad_read(lv_indev_drv_t *indev_drv, lv_indev_data_t *data)
{
    esp_lcd_touch_read_data(touch_ctx->handle);
    bool touchpad_pressed = esp_lcd_touch_get_coordinates(...);
    if (touchpad_pressed) {
        data->point.x = touchpad_x[0];
        data->point.y = touchpad_y[0];
        data->state = LV_INDEV_STATE_PRESSED;
    }
}

lv_indev_drv_register(&touch_ctx->indev_drv);  // LVGL v8 API
```

This proves the hardware and drivers work correctly with proper LVGL integration.

### Questions

1. **Does touch work for you with this firmware?**
   - If yes, what initialization steps are we missing?
   - Can you share a working test script?

2. **Status of PR #454 (touch fix)?**
   - README mentions this was included
   - What does this fix actually address?
   - Is it compatible with LVGL v9?

3. **Input device polling in LVGL v9:**
   - How should input devices be registered in LVGL v9 with MicroPython?
   - Is there a configuration flag needed to enable input polling?
   - Is `pointer_framework` compatible with LVGL v9?

### Complete Investigation

Full research documentation with all tests, findings, and forum references:
- Repository: https://github.com/yaconsult/CheapBlackDisplay
- Research doc: `TOUCH_RESEARCH.md`
- Test files: `test_touch_*.py` (8 different approaches tested)

### Request

Could you please:
1. Confirm whether touch is working in your testing
2. Provide a working example if touch works
3. Investigate why LVGL v9 doesn't poll input devices
4. Consider if this is a known issue with LVGL v9 migration

### Workaround

Currently using Arduino firmware as it has working touch. Would prefer to use MicroPython if touch can be fixed.

---

**Thank you for creating this firmware!** The display works beautifully, and we've confirmed the touch hardware is perfect. Just need help getting LVGL to poll the touch driver.
