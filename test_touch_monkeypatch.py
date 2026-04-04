"""
Touch test using monkey patch fix from LVGL forum
Based on kdschlosser's suggestion for JC3248W535 board
Forum: https://forum.lvgl.io/t/jc3248w535en-event-problem/21586/8
"""
import lvgl as lv
import machine
import lcd_bus
import time
from i2c import I2C
import axs15231

print("Touch Monkey Patch Test - Forum Fix")

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

print("Creating monkey-patched touch driver...")

# MONKEY PATCH FIX from kdschlosser
# This overrides the _get_coords method to fix touch state handling
class AXS15231(axs15231.AXS15231):
    def __init__(self, device, touch_cal=None, 
                 startup_rotation=lv.DISPLAY_ROTATION._0, debug=False):
        super().__init__(device, touch_cal, startup_rotation, debug)
        self.__last_x = -1
        self.__last_y = -1
        self.__last_state = self.RELEASED
        print("Monkey-patched AXS15231 initialized")
    
    def _get_coords(self):
        """Overridden _get_coords with fix for state handling"""
        touch_data = self._read_data()
        
        if touch_data:
            self.__last_x = touch_data[0].x
            self.__last_y = touch_data[0].y
            
            if touch_data[0].event == 1:
                self.__last_state = self.RELEASED
            else:
                self.__last_state = self.PRESSED
                
            if self.__last_state == self.PRESSED:
                print(f"Touch: X={self.__last_x}, Y={self.__last_y}")
        
        return self.__last_state, self.__last_x, self.__last_y

# Create touch driver with monkey patch
print("Initializing touch with monkey patch...")
indev = AXS15231(touch_i2c, debug=True)
print("Touch driver initialized!")

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
title.set_text("Monkey Patch Fix!")
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
print("MONKEY PATCH FIX TEST RUNNING!")
print("="*60)
print("This uses kdschlosser's fix from LVGL forum")
print("Touch the button - it should respond!")
print("Watch console for touch coordinates and button events\n")

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
