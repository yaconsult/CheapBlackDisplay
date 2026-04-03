import lvgl as lv
import machine
import lcd_bus
import time
from i2c import I2C

print("Touch Event Injection Test")

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

print("Touch I2C initialized")

# Create UI first
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
title.set_text("Touch Event Injection")
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
status.set_text("Touch anywhere on screen")
status.align(lv.ALIGN.CENTER, 0, 100)
status.set_style_text_color(lv.color_make(255, 255, 0), 0)

# Coordinate display
coord_label = lv.label(scr)
coord_label.set_text("X: ---, Y: ---")
coord_label.set_pos(10, 10)
coord_label.set_style_text_color(lv.color_make(255, 255, 255), 0)

# Click counter
click_count = [0]
last_was_pressed = [False]

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
print("Touch event injection test running")
print("="*60)
print("Touch the screen - coordinates will update")
print("Touch the button - it should respond\n")

# Main loop with manual touch polling and event injection
poll_count = 0
while True:
    # Poll touch every cycle
    try:
        touch_i2c.write(tx_buf)
        touch_i2c.read(buf=rx_buf)
        
        num_points = rx_buf[1]
        
        if num_points > 0 and num_points < 10:
            x = ((rx_buf[2] & 0x0F) << 8) | rx_buf[3]
            y = ((rx_buf[4] & 0x0F) << 8) | rx_buf[5]
            event = (rx_buf[2] >> 6) & 0x03
            
            # Update coordinate display
            coord_label.set_text(f"X: {x}, Y: {y}")
            
            is_pressed = (event != 1)
            
            if is_pressed:
                # Check if touch is on button
                btn_x = 150  # Button center X (240 - 90)
                btn_y = 125  # Button center Y (160 - 35)
                
                if abs(x - btn_x) < 90 and abs(y - btn_y) < 35:
                    if not last_was_pressed[0]:
                        print(f"Touch on button at X={x}, Y={y}")
                        # Manually send pressed event
                        btn.send_event(lv.EVENT.PRESSED, None)
                    last_was_pressed[0] = True
                else:
                    if last_was_pressed[0]:
                        last_was_pressed[0] = False
            else:
                # Release
                if last_was_pressed[0]:
                    print(f"Touch released at X={x}, Y={y}")
                    # Manually send clicked event
                    btn.send_event(lv.EVENT.CLICKED, None)
                    last_was_pressed[0] = False
                    
    except Exception as e:
        poll_count += 1
        if poll_count % 100 == 0:
            print(f"Touch poll error: {e}")
    
    lv.timer_handler()
    time.sleep_ms(10)
