"""
Simple LVGL Configuration for JC3248W535EN Display (Landscape Mode)
No touch support - display only
"""

import machine
import lcd_bus
import lvgl as lv
import axs15231b

# Display dimensions (landscape mode with 90° rotation)
WIDTH = 480
HEIGHT = 320

# QSPI Display Pins
SCLK_PIN = 47
DATA0_PIN = 21
DATA1_PIN = 48
DATA2_PIN = 40
DATA3_PIN = 39
CS_PIN = 45
DC_PIN = 8
BACKLIGHT_PIN = 1
FREQ = 40000000

# Initialize QSPI bus
spi_bus = machine.SPI.Bus(
    host=1,
    sck=47,
    quad_pins=(21, 48, 40, 39)
)

# Create display bus
display_bus = lcd_bus.SPIBusFast(
    spi_bus=spi_bus,
    dc=DC_PIN,
    cs=CS_PIN,
    freq=FREQ,
    spi_mode=3,
    quad=True
)

# Allocate frame buffer
buf = bytearray(320 * 40 * 2)

# Create display driver
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

# Initialize display
print(f"Initializing {WIDTH}x{HEIGHT} QSPI display...")
display.set_power(True)
display.set_backlight(80)
display.init()
display.set_rotation(lv.DISPLAY_ROTATION._90)
print("Display initialized successfully with 90° rotation!")

# Export for use by other modules
disp = display
