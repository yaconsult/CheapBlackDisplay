import lvgl as lv
import machine
import lcd_bus
import time
from i2c import I2C

print("Touch I2C Polling Test - Raw Data")

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

# Create UI
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x001100), 0)

label = lv.label(scr)
label.set_text("Touch I2C Polling Test\n\nTouch the screen\nRaw I2C data will appear below")
label.set_pos(10, 10)
label.set_style_text_color(lv.color_make(0, 255, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

data_label = lv.label(scr)
data_label.set_pos(10, 120)
data_label.set_style_text_color(lv.color_make(255, 255, 0), 0)
data_label.set_style_text_font(lv.font_montserrat_14, 0)
data_label.set_text("Waiting for touch data...")

print("\nPolling touch controller every 100ms")
print("Touch the screen - raw I2C data will be shown")
print("Format: [byte0, byte1, byte2, byte3, byte4, byte5, byte6, byte7]")
print("byte1 = number of touch points")
print("If byte1 > 0, touch is detected\n")

count = 0
last_data = None

while True:
    lv.timer_handler()
    time.sleep_ms(100)
    
    try:
        # Send read command
        touch_i2c.write(tx_buf)
        # Read response
        touch_i2c.read(buf=rx_buf)
        
        # Convert to list for display
        data = list(rx_buf)
        
        # Only print/update if data changed
        if data != last_data:
            last_data = data[:]
            
            num_points = data[1]
            
            if num_points > 0:
                # Parse touch coordinates
                x = ((data[2] & 0x0F) << 8) | data[3]
                y = ((data[4] & 0x0F) << 8) | data[5]
                event = (data[2] >> 6) & 0x03
                
                msg = f"TOUCH DETECTED!\nPoints: {num_points}\nX: {x}, Y: {y}\nEvent: {event}\nRaw: {data}"
                print(f"*** TOUCH: X={x}, Y={y}, Event={event}, Points={num_points}")
                print(f"    Raw data: {data}")
                data_label.set_text(msg)
                data_label.set_style_text_color(lv.color_make(0, 255, 0), 0)
            else:
                # No touch
                count += 1
                if count % 10 == 0:  # Update every second
                    data_label.set_text(f"No touch detected\nPolling... ({count/10:.0f}s)\nRaw: {data}")
                    data_label.set_style_text_color(lv.color_make(255, 255, 0), 0)
                    
    except Exception as e:
        print(f"I2C Error: {e}")
        data_label.set_text(f"I2C Error: {e}")
        data_label.set_style_text_color(lv.color_make(255, 0, 0), 0)
        time.sleep_ms(1000)
