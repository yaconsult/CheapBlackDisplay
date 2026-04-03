import lvgl as lv
import machine
import lcd_bus
import time

print("Starting simple display test...")

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
import axs15231b

# Allocate frame buffer
buf_size = 320 * 40 * 2  # 40 lines buffer, RGB565 = 2 bytes per pixel
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

# Power on and initialize
display.set_power(True)
display.set_backlight(100)
display.init()

# Set landscape mode (90 degree rotation)
display.set_rotation(lv.DISPLAY_ROTATION._90)
print("Display initialized in landscape mode (480x320)")

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
label_center.set_text("Display Test\n480x320")
label_center.center()
label_center.set_style_text_color(lv.color_make(0, 255, 0), 0)
label_center.set_style_text_font(lv.font_montserrat_20, 0)

print("UI created. Starting main loop...")
print("You should see colored squares in the corners and text in the center.")

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
