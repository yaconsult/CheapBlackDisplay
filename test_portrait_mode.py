import lvgl as lv
import machine
import lcd_bus
import time
import axs15231b
import axs15231
from i2c import I2C

print("Starting Portrait Mode Test (320x480)")

# Initialize LVGL
lv.init()

# Display pins
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
TOUCH_I2C_ADDR = 0x3B
TOUCH_BITS = 8

# Display dimensions (portrait)
WIDTH = 320
HEIGHT = 480

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
display.set_backlight(80)
display.init()
# No rotation for portrait mode (0 degrees)
print(f"Display initialized: {WIDTH}x{HEIGHT}")

# Initialize touch controller
print("Initializing touch controller...")
i2c_bus = I2C.Bus(host=1, sda=TOUCH_SDA_PIN, scl=TOUCH_SCL_PIN)
touch_i2c = I2C.Device(i2c_bus, TOUCH_I2C_ADDR, TOUCH_BITS)
indev = axs15231.AXS15231(touch_i2c, debug=False)
print("Touch controller initialized")

# UI parameters
size_x = 50
size_y = 50
slide_x = 200
slide_y = 40
text_y = -150

print('Creating UI...')

scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x000000), 0)

# Left TOP - Red
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(0, 0)
rect.set_style_bg_color(lv.color_make(255, 0, 0), 0)

label = lv.label(rect)
label.set_text("R")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Right TOP - Green
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(WIDTH-size_x, 0)
rect.set_style_bg_color(lv.color_make(0, 255, 0), 0)

label = lv.label(rect)
label.set_text("G")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Left BOTTOM - Blue
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(0, HEIGHT-size_y)
rect.set_style_bg_color(lv.color_make(0, 0, 255), 0)

label = lv.label(rect)
label.set_text("B")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Right BOTTOM - White
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(WIDTH-size_x, HEIGHT-size_y)
rect.set_style_bg_color(lv.color_make(255, 255, 255), 0)

label = lv.label(rect)
label.set_text("W")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Draw cross lines
line1 = lv.line(scr)
line2 = lv.line(scr)

points1 = [
    {"x": size_x, "y": size_y},
    {"x": WIDTH - size_x, "y": HEIGHT - size_y}
]
points2 = [
    {"x": WIDTH - size_x, "y": size_y},
    {"x": size_x, "y": HEIGHT - size_y}
]

line1.set_points(points1, 2)
line2.set_points(points2, 2)

line1.set_style_line_color(lv.color_make(255, 255, 255), 0)
line2.set_style_line_color(lv.color_make(255, 255, 255), 0)

line1.set_style_line_width(2, 0)
line2.set_style_line_width(2, 0)

# Slider
slider = lv.slider(scr)
slider.set_size(slide_x, slide_y)
slider.center()

# Resolution label
label = lv.label(scr)
label.set_text(f"{WIDTH}x{HEIGHT}")
label.align(lv.ALIGN.CENTER, 0, text_y)
label.set_style_text_font(lv.font_montserrat_16, 0)
label.set_style_text_color(lv.color_make(0, 255, 0), 0)

print('UI created. Starting main loop...')
print('Touch the slider to test touch functionality')

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
