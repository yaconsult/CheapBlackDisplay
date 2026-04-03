import machine
import time

print("Testing backlight control...")

# Backlight pin
backlight = machine.Pin(1, machine.Pin.OUT)

print("Turning backlight ON (high)...")
backlight.value(1)
time.sleep(2)

print("Turning backlight OFF (low)...")
backlight.value(0)
time.sleep(2)

print("Turning backlight ON again...")
backlight.value(1)
time.sleep(2)

# Try PWM control
print("Testing PWM backlight control...")
pwm = machine.PWM(backlight, freq=1000)

for brightness in [0, 25, 50, 75, 100]:
    duty = int((brightness / 100) * 1023)
    print(f"Setting brightness to {brightness}% (duty={duty})")
    pwm.duty(duty)
    time.sleep(1)

print("Backlight test complete - should be at 100% brightness now")
