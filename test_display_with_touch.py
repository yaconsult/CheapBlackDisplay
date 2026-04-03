import lvgl as lv
import machine
import lcd_bus
import time
import axs15231b
import axs15231
from i2c import I2C

print("Starting display + touch test...")

# Initialize LVGL
lv.init()

# Display pins for JC3248W535EN
SCLK_PIN = 47
DATA0_PIN = 21
DATA1_PIN = 48
DATA2_PIN = 40
DATA3_PIN = 39
CS_PIN = 45
DC_PIN = 8
BACKLIGHT_PIN = 1

# Touch pins
TOUCH_SDA_PIN = 4
TOUCH_SCL_PIN = 8

# Initialize QSPI bus
print("Initializing QSPI bus...")
spi_bus = machine.SPI.Bus(
    host=1,
    sck=SCLK_PIN,
    quad_pins=(DATA0_PIN, DATA1_PIN, DATA2_PIN, DATA3_PIN)
)

# Create display bus
display_bus = lcd_bus.SPIBusFast(
    spi_bus=spi_bus,
    dc=DC_PIN,
    cs=CS_PIN,
    freq=40000000,
    spi_mode=3,
    quad=True
)

# Initialize display driver
print("Initializing display driver...")

buf_size = 320 * 40 * 2
buf = bytearray(buf_size)

display = axs15231b.AXS15231B(
    display_bus,
    320,
    480,
    frame_buffer1=buf,
    backlight_pin=BACKLIGHT_PIN,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True,
    backlight_on_state=axs15231b.STATE_PWM
)

display.set_power(True)
display.set_backlight(100)
display.init()
display.set_rotation(lv.DISPLAY_ROTATION._90)
print("Display initialized in landscape mode (480x320)")

# Initialize touch controller
print("Initializing touch controller...")

# Touch controller constants (from axs15231.py)
TOUCH_I2C_ADDR = 0x3B
TOUCH_BITS = 8

i2c_bus = I2C.Bus(host=1, sda=TOUCH_SDA_PIN, scl=TOUCH_SCL_PIN)
touch_i2c = I2C.Device(i2c_bus, TOUCH_I2C_ADDR, TOUCH_BITS)

indev = axs15231.AXS15231(touch_i2c, debug=False)
print(f"Touch controller initialized")

# Create UI
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x000000), 0)

# Red square - top left
rect_r = lv.obj(scr)
rect_r.set_size(50, 50)
rect_r.set_pos(0, 0)
rect_r.set_style_bg_color(lv.color_make(255, 0, 0), 0)

label_r = lv.label(rect_r)
label_r.set_text("R")
label_r.center()
label_r.set_style_text_color(lv.color_make(255, 255, 255), 0)

# Green square - top right
rect_g = lv.obj(scr)
rect_g.set_size(50, 50)
rect_g.set_pos(430, 0)
rect_g.set_style_bg_color(lv.color_make(0, 255, 0), 0)

label_g = lv.label(rect_g)
label_g.set_text("G")
label_g.center()
label_g.set_style_text_color(lv.color_make(0, 0, 0), 0)

# Blue square - bottom left
rect_b = lv.obj(scr)
rect_b.set_size(50, 50)
rect_b.set_pos(0, 270)
rect_b.set_style_bg_color(lv.color_make(0, 0, 255), 0)

label_b = lv.label(rect_b)
label_b.set_text("B")
label_b.center()
label_b.set_style_text_color(lv.color_make(255, 255, 255), 0)

# White square - bottom right
rect_w = lv.obj(scr)
rect_w.set_size(50, 50)
rect_w.set_pos(430, 270)
rect_w.set_style_bg_color(lv.color_make(255, 255, 255), 0)

label_w = lv.label(rect_w)
label_w.set_text("W")
label_w.center()
label_w.set_style_text_color(lv.color_make(0, 0, 0), 0)

# Center label
label_center = lv.label(scr)
label_center.set_text("Touch Test\n480x320")
label_center.center()
label_center.set_style_text_color(lv.color_make(0, 255, 0), 0)
label_center.set_style_text_font(lv.font_montserrat_20, 0)

# Create a button to test touch
btn = lv.button(scr)
btn.set_size(120, 50)
btn.set_pos(180, 200)

btn_label = lv.label(btn)
btn_label.set_text("Touch Me!")
btn_label.center()

# Button event handler
def btn_event_cb(e):
    code = e.get_code()
    if code == lv.EVENT.CLICKED:
        print("Button clicked!")
        label_center.set_text("TOUCHED!")

btn.add_event_cb(btn_event_cb, lv.EVENT.ALL, None)

print("UI created with touch support. Starting main loop...")
print("Try touching the 'Touch Me!' button")

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
