# Troubleshooting Guide

## Current Status

### ✅ What's Working
- Display driver initializes successfully
- Touch controller initializes successfully  
- LVGL graphics system works
- Test patterns display correctly (when display is on)
- Landscape mode (480x320) works
- Portrait mode (320x480) works
- All test scripts load and run without errors

### ⚠️ Known Issues

#### 1. Display Goes Black Intermittently

**Symptom:** Display shows test pattern initially, then goes black after certain operations (resets, running new tests, file uploads).

**What we've tried:**
- Soft resets (Ctrl-D) - sometimes causes black screen
- Power cycling (unplug/replug USB) - sometimes works
- Different test scripts - all have same issue
- Backlight control - set to 100% in all tests

**Possible causes:**
- Display power management issue
- Initialization sequence not complete
- Hardware connection problem
- Display needs specific power-on sequence

**Workarounds:**
1. Unplug and replug USB cable
2. Run `python3 quick_test.py` without doing soft resets
3. Avoid running multiple tests in sequence
4. If display goes black, power cycle the board

#### 2. Touch Not Responding

**Symptom:** Touch controller initializes successfully but doesn't detect touch events.

**Status:** Cannot fully test due to display going black during touch diagnostic tests.

**What we know:**
- Touch controller (AXS15231) initializes without errors
- I2C communication appears to work (no errors during init)
- Touch events not being detected when screen is touched
- Need to verify I2C scan shows device at address 0x3B

**Next steps to test (when display is stable):**
1. Run I2C scan to verify touch controller is detected
2. Check if touch controller needs additional initialization
3. Verify touch coordinates are being read
4. Check if touch calibration is needed

## Recommended Next Steps

### For Display Issue:

1. **Check hardware connections**
   - Verify all display ribbon cables are fully seated
   - Check for loose connections
   - Inspect for physical damage

2. **Try different initialization**
   - May need to add delays after power-on
   - May need specific initialization sequence
   - Check manufacturer's demo code for initialization differences

3. **Power supply**
   - Verify USB power is sufficient
   - Try different USB port or powered USB hub
   - Check if board has external power option

### For Touch Issue:

1. **Verify I2C communication**
   ```python
   from i2c import I2C
   i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
   devices = i2c_bus.scan()
   print(devices)  # Should show [59] or [0x3B]
   ```

2. **Check touch controller datasheet**
   - Verify initialization sequence
   - Check if additional configuration needed
   - Verify I2C address is correct (0x3B)

3. **Test with manufacturer's demo**
   - Compare with factory demo at `/home/lpinard/Downloads/JC3248W535EN`
   - Check if their demo has touch working
   - Compare initialization sequences

## Working Test Commands

When display is stable, use these commands:

```bash
# Simple display test (no touch)
python3 quick_test.py

# Landscape mode test
python3 -c "import serial, time, glob; port=glob.glob('/dev/ttyACM*')[0]; ser=serial.Serial(port,115200,timeout=1); time.sleep(0.5); ser.write(b'\x03'); time.sleep(0.3); ser.read(ser.in_waiting); ser.write(b'import test_landscape_mode\r\n'); time.sleep(3); ser.close()"

# Portrait mode test  
python3 -c "import serial, time, glob; port=glob.glob('/dev/ttyACM*')[0]; ser=serial.Serial(port,115200,timeout=1); time.sleep(0.5); ser.write(b'\x03'); time.sleep(0.3); ser.read(ser.in_waiting); ser.write(b'import test_portrait_mode\r\n'); time.sleep(3); ser.close()"
```

## Hardware Specifications

- **Board**: JC3248W535EN (ESP32-S3)
- **Display**: 320x480, AXS15231B controller, QSPI interface
- **Touch**: AXS15231 capacitive, I2C interface
- **Firmware**: MicroPython 1.25.0 with LVGL 9.2.2

## Pin Configuration

### Display (QSPI):
- SCLK: GPIO 47
- DATA0-3: GPIO 21, 48, 40, 39
- CS: GPIO 45
- DC: GPIO 8
- Backlight: GPIO 1

### Touch (I2C):
- SDA: GPIO 4
- SCL: GPIO 8
- Address: 0x3B
- Bits: 8

## Contact

If you solve the display black screen issue or get touch working, please update this document with the solution!
