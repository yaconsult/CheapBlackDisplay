import lvgl as lv
import machine
import lcd_bus
import time
from i2c import I2C

print("Touch Working Test - Integrated Polling")

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

# Touch data buffers
tx_buf = bytearray([0xB5, 0xAB, 0xA5, 0x5A, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00])
rx_buf = bytearray(8)

# Touch state
touch_state = {
    'x': 0,
    'y': 0,
    'pressed': False
}

def read_touch_data():
    """Read touch data from I2C and update state"""
    try:
        touch_i2c.write(tx_buf)
        touch_i2c.read(buf=rx_buf)
        
        num_points = rx_buf[1]
        
        if num_points > 0 and num_points < 10:  # Valid touch
            x = ((rx_buf[2] & 0x0F) << 8) | rx_buf[3]
            y = ((rx_buf[4] & 0x0F) << 8) | rx_buf[5]
            event = (rx_buf[2] >> 6) & 0x03
            
            touch_state['x'] = x
            touch_state['y'] = y
            touch_state['pressed'] = (event != 1)  # Not release
            
            return True
        else:
            touch_state['pressed'] = False
            return False
    except:
        return False

def touch_read_cb(drv, data):
    """LVGL touch callback"""
    read_touch_data()
    data.point.x = touch_state['x']
    data.point.y = touch_state['y']
    data.state = lv.INDEV_STATE.PRESSED if touch_state['pressed'] else lv.INDEV_STATE.RELEASED
    return False

# Create and register touch input device
print("Registering touch input device...")
indev = lv.indev_create()
indev.set_type(lv.INDEV_TYPE.POINTER)
indev.set_read_cb(touch_read_cb)
print("Touch registered!")

# Create UI
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x000000), 0)

# Colored squares in corners
rect_r = lv.obj(scr)
rect_r.set_size(50, 50)
rect_r.set_pos(0, 0)
rect_r.set_style_bg_color(lv.color_make(255, 0, 0), 0)
label_r = lv.label(rect_r)
label_r.set_text("R")
label_r.center()

rect_g = lv.obj(scr)
rect_g.set_size(50, 50)
rect_g.set_pos(430, 0)
rect_g.set_style_bg_color(lv.color_make(0, 255, 0), 0)
label_g = lv.label(rect_g)
label_g.set_text("G")
label_g.center()

rect_b = lv.obj(scr)
rect_b.set_size(50, 50)
rect_b.set_pos(0, 270)
rect_b.set_style_bg_color(lv.color_make(0, 0, 255), 0)
label_b = lv.label(rect_b)
label_b.set_text("B")
label_b.center()

rect_w = lv.obj(scr)
rect_w.set_size(50, 50)
rect_w.set_pos(430, 270)
rect_w.set_style_bg_color(lv.color_make(255, 255, 255), 0)
label_w = lv.label(rect_w)
label_w.set_text("W")
label_w.center()

# Title
title = lv.label(scr)
title.set_text("Touch Working! 480x320")
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
status.set_text("Ready - Touch the button!")
status.align(lv.ALIGN.CENTER, 0, 100)
status.set_style_text_color(lv.color_make(255, 255, 0), 0)

# Click counter
click_count = [0]

def btn_event_cb(e):
    code = e.get_code()
    if code == lv.EVENT.CLICKED:
        click_count[0] += 1
        print(f"*** BUTTON CLICKED! (Count: {click_count[0]}) ***")
        status.set_text(f"CLICKED! Count: {click_count[0]}")
        status.set_style_text_color(lv.color_make(0, 255, 0), 0)
    elif code == lv.EVENT.PRESSED:
        print("Button pressed")
        status.set_text("Button pressed...")
        status.set_style_text_color(lv.color_make(255, 128, 0), 0)
    elif code == lv.EVENT.RELEASED:
        print("Button released")

btn.add_event_cb(btn_event_cb, lv.EVENT.ALL, None)

print("\n" + "="*60)
print("Touch is WORKING!")
print("="*60)
print("Touch the button - it should respond!")
print("Click count will appear on screen and in console\n")

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
