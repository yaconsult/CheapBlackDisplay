import lvgl as lv
import machine
import lcd_bus
import time
from i2c import I2C

print("Manual Touch Registration Test")

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
last_x = 0
last_y = 0
last_state = lv.INDEV_STATE.RELEASED

def read_touch():
    """Read touch data directly from I2C"""
    global last_x, last_y, last_state
    
    try:
        touch_i2c.write(tx_buf)
        touch_i2c.read(buf=rx_buf)
        
        num_points = rx_buf[1]
        
        if num_points > 0:
            # Parse touch data
            x = ((rx_buf[2] & 0x0F) << 8) | rx_buf[3]
            y = ((rx_buf[4] & 0x0F) << 8) | rx_buf[5]
            event = (rx_buf[2] >> 6) & 0x03
            
            last_x = x
            last_y = y
            
            if event == 1:  # Release
                last_state = lv.INDEV_STATE.RELEASED
            else:  # Press or move
                last_state = lv.INDEV_STATE.PRESSED
                print(f"Touch: X={x}, Y={y}, Event={event}")
    except Exception as e:
        print(f"Touch read error: {e}")

def touch_read_cb(drv, data):
    """LVGL touch read callback"""
    read_touch()
    data.point.x = last_x
    data.point.y = last_y
    data.state = last_state
    return False

# Manually create and register touch input device
print("Manually registering touch input device with LVGL...")
indev = lv.indev_create()
indev.set_type(lv.INDEV_TYPE.POINTER)
indev.set_read_cb(touch_read_cb)
print("Touch input device registered")

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

# Center label
label = lv.label(scr)
label.set_text("Manual Touch Test\n480x320")
label.align(lv.ALIGN.CENTER, 0, -60)
label.set_style_text_color(lv.color_make(0, 255, 0), 0)
label.set_style_text_font(lv.font_montserrat_20, 0)
label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

# Touch button
btn = lv.button(scr)
btn.set_size(150, 60)
btn.center()

btn_label = lv.label(btn)
btn_label.set_text("Touch Me!")
btn_label.center()

status_label = lv.label(scr)
status_label.set_text("Waiting for touch...")
status_label.align(lv.ALIGN.CENTER, 0, 80)
status_label.set_style_text_color(lv.color_make(255, 255, 0), 0)

def btn_event_cb(e):
    code = e.get_code()
    if code == lv.EVENT.CLICKED:
        print("*** BUTTON CLICKED! ***")
        status_label.set_text("BUTTON CLICKED!")
        status_label.set_style_text_color(lv.color_make(0, 255, 0), 0)
    elif code == lv.EVENT.PRESSED:
        print("Button pressed")
        status_label.set_text("Button pressed...")
        status_label.set_style_text_color(lv.color_make(255, 255, 0), 0)

btn.add_event_cb(btn_event_cb, lv.EVENT.ALL, None)

print("\nManual touch test running!")
print("Touch the button - events should appear")
print("Touch coordinates will be printed to console\n")

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
