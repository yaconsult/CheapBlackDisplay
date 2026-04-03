import lvgl as lv
import machine
import lcd_bus
import time
from i2c import I2C
import _thread

print("Touch Test - LVGL v9 with Threading")

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

# Touch state - shared between threads
touch_state = {
    'x': 0,
    'y': 0,
    'pressed': False,
    'lock': _thread.allocate_lock()
}

def touch_polling_thread():
    """Background thread that continuously polls touch controller"""
    print("Touch polling thread started")
    while True:
        try:
            # Read touch data
            touch_i2c.write(tx_buf)
            touch_i2c.read(buf=rx_buf)
            
            num_points = rx_buf[1]
            
            with touch_state['lock']:
                if num_points > 0 and num_points < 10:
                    x = ((rx_buf[2] & 0x0F) << 8) | rx_buf[3]
                    y = ((rx_buf[4] & 0x0F) << 8) | rx_buf[5]
                    event = (rx_buf[2] >> 6) & 0x03
                    
                    touch_state['x'] = x
                    touch_state['y'] = y
                    touch_state['pressed'] = (event != 1)
                else:
                    touch_state['pressed'] = False
                    
        except Exception as e:
            pass
            
        time.sleep_ms(10)

def touch_read_cb(drv, data):
    """LVGL touch callback - called by LVGL"""
    with touch_state['lock']:
        data.point.x = touch_state['x']
        data.point.y = touch_state['y']
        data.state = lv.INDEV_STATE.PRESSED if touch_state['pressed'] else lv.INDEV_STATE.RELEASED
    return False

# Start touch polling thread
print("Starting touch polling thread...")
_thread.start_new_thread(touch_polling_thread, ())
time.sleep(0.5)

# Create and register touch input device (LVGL v9 API)
print("Registering touch input device with LVGL v9...")
indev = lv.indev_create()
indev.set_type(lv.INDEV_TYPE.POINTER)
indev.set_read_cb(touch_read_cb)
print("Touch registered!")

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
title.set_text("Touch with Threading!")
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

btn.add_event_cb(btn_event_cb, lv.EVENT.ALL, None)

print("\n" + "="*60)
print("Touch with threading test running!")
print("="*60)
print("Touch the button - it should respond!")
print("Background thread is polling touch controller\n")

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
