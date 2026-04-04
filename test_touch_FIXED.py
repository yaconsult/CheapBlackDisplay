"""
FIXED Touch Test - Solution from LVGL Forum
Based on dzario's fix: https://forum.lvgl.io/t/jc3248w535en-event-problem/21586

The AXS15231 sensor needs 20ms minimum between I2C reads.
This version uses the fixed driver with proper timing.
"""
import lvgl as lv
import machine
import lcd_bus
import time
from i2c import I2C

print("FIXED Touch Test - 20ms Timing Solution")

# Initialize LVGL
lv.init()

# Display setup
spi_bus = machine.SPI.Bus(host=1, sck=47, quad_pins=(21, 48, 40, 39))
display_bus = lcd_bus.SPIBusFast(spi_bus=spi_bus, dc=8, cs=45, freq=40000000, spi_mode=3, quad=True)

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
print("Display initialized: 480x320")

# Touch I2C setup
i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, 0x3B, 8)

print("Loading FIXED touch driver...")
# Import the fixed driver
import axs15231_fixed

print("Initializing touch with FIXED driver (20ms timing)...")
indev = axs15231_fixed.AXS15231(touch_i2c, debug=True)
print("Touch driver initialized with fix!")

# Create UI
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x000000), 0)

# Colored squares
rect_r = lv.obj(scr)
rect_r.set_size(50, 50)
rect_r.set_pos(0, 0)
rect_r.set_style_bg_color(lv.color_make(255, 0, 0), 0)

rect_g = lv.obj(scr)
rect_g.set_size(50, 50)
rect_g.set_pos(430, 0)
rect_g.set_style_bg_color(lv.color_make(0, 255, 0), 0)

rect_b = lv.obj(scr)
rect_b.set_size(50, 50)
rect_b.set_pos(0, 270)
rect_b.set_style_bg_color(lv.color_make(0, 0, 255), 0)

rect_w = lv.obj(scr)
rect_w.set_size(50, 50)
rect_w.set_pos(430, 270)
rect_w.set_style_bg_color(lv.color_make(255, 255, 255), 0)

# Title
title = lv.label(scr)
title.set_text("TOUCH FIXED!")
title.align(lv.ALIGN.CENTER, 0, -80)
title.set_style_text_color(lv.color_make(0, 255, 0), 0)
title.set_style_text_font(lv.font_montserrat_20, 0)

# Touch button
btn = lv.button(scr)
btn.set_size(180, 70)
btn.center()

btn_label = lv.label(btn)
btn_label.set_text("Touch Me!")
btn_label.center()
btn_label.set_style_text_font(lv.font_montserrat_20, 0)

# Status label
status = lv.label(scr)
status.set_text("Touch the button!")
status.align(lv.ALIGN.CENTER, 0, 100)
status.set_style_text_color(lv.color_make(255, 255, 0), 0)

# Click counter
click_count = [0]

def btn_event_cb(e):
    code = e.get_code()
    if code == lv.EVENT.CLICKED:
        click_count[0] += 1
        print(f"*** BUTTON CLICKED! Count: {click_count[0]} ***")
        status.set_text(f"CLICKED! Count: {click_count[0]}")
        status.set_style_text_color(lv.color_make(0, 255, 0), 0)
    elif code == lv.EVENT.PRESSED:
        print("Button pressed")
        status.set_text("Button PRESSED")
        status.set_style_text_color(lv.color_make(255, 128, 0), 0)
    elif code == lv.EVENT.RELEASED:
        print("Button released")

btn.add_event_cb(btn_event_cb, lv.EVENT.ALL, None)

print("\n" + "="*60)
print("TOUCH SHOULD BE WORKING NOW!")
print("="*60)
print("Using fixed driver with 20ms minimum read interval")
print("Touch the button - it should respond properly!")
print("Watch console for button events\n")

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
