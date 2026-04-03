import lvgl as lv
import machine
import lcd_bus
import time
import axs15231b
import axs15231
from i2c import I2C

print("Touch I2C Read Test")

# Initialize LVGL
lv.init()

# Display setup
spi_bus = machine.SPI.Bus(host=1, sck=47, quad_pins=(21, 48, 40, 39))
display_bus = lcd_bus.SPIBusFast(spi_bus=spi_bus, dc=8, cs=45, freq=40000000, spi_mode=3, quad=True)

buf = bytearray(320 * 40 * 2)
display = axs15231b.AXS15231B(display_bus, 320, 480, frame_buffer1=buf, backlight_pin=1,
                               color_space=lv.COLOR_FORMAT.RGB565, rgb565_byte_swap=True,
                               backlight_on_state=axs15231b.STATE_PWM)

display.set_power(True)
display.set_backlight(100)
display.init()
display.set_rotation(lv.DISPLAY_ROTATION._90)
print("Display initialized: 480x320")

# Touch setup
i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, 0x3B, 8)

# Create touch driver with debug enabled
indev = axs15231.AXS15231(touch_i2c, debug=True)
print("Touch initialized with debug=True")

# Create UI
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x003300), 0)

label = lv.label(scr)
label.set_text("Touch I2C Read Test\n\nTouch the screen\nDebug output will show in console")
label.center()
label.set_style_text_color(lv.color_make(0, 255, 0), 0)
label.set_style_text_font(lv.font_montserrat_20, 0)
label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

print("\nTouch diagnostic running with debug enabled...")
print("Touch the screen - watch for debug output")
print("If you see 'read' messages, the driver is polling")
print("If you see touch data, the hardware is responding\n")

# Main loop
count = 0
while True:
    lv.timer_handler()
    time.sleep_ms(5)
    
    # Print status every 2 seconds
    count += 1
    if count >= 400:  # 400 * 5ms = 2 seconds
        print("Still running... (touch the screen)")
        count = 0
