# Flash Arduino DEMO_LVGL to JC3248W535

## Quick Guide to Flash and Test Arduino Demo with Touch

This guide shows how to flash the Arduino DEMO_LVGL to verify touch works with Arduino firmware.

---

## Prerequisites

You need either:
- **Arduino IDE** (easiest for testing)
- **PlatformIO** (better for development - see PLATFORMIO_SETUP.md)
- **Arduino CLI** (command line)

---

## Option 1: Using Arduino IDE (Recommended for Quick Test)

### Step 1: Install Arduino IDE

```bash
# Download from https://www.arduino.cc/en/software
# Or install via package manager:

# Ubuntu/Debian
sudo apt install arduino

# Or download latest version:
wget https://downloads.arduino.cc/arduino-ide/arduino-ide_2.3.2_Linux_64bit.AppImage
chmod +x arduino-ide_2.3.2_Linux_64bit.AppImage
./arduino-ide_2.3.2_Linux_64bit.AppImage
```

### Step 2: Install ESP32 Board Support

1. Open Arduino IDE
2. Go to **File → Preferences**
3. In "Additional Board Manager URLs" add:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click OK
5. Go to **Tools → Board → Boards Manager**
6. Search for "esp32"
7. Install **"esp32 by Espressif Systems" version 3.0.2** (as specified in Must see for use.txt)
8. Wait for installation to complete

### Step 3: Install Required Libraries

1. Go to **Sketch → Include Library → Manage Libraries**
2. Search and install:
   - **lvgl** (version 8.3.x)
   
**OR** copy libraries from demo folder:

```bash
# Copy to Arduino libraries folder
cp -r ~/PycharmProjects/CheapBlackDisplay/JC3248W535EN/1-Demo/Demo_Arduino/libraries/* ~/Arduino/libraries/
```

### Step 4: Open DEMO_LVGL

1. **File → Open**
2. Navigate to:
   ```
   /home/lpinard/PycharmProjects/CheapBlackDisplay/JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/DEMO_LVGL.ino
   ```
3. Click Open

### Step 5: Configure Board Settings

1. **Tools → Board → esp32 → ESP32S3 Dev Module**

2. Configure settings:
   - **USB CDC On Boot:** Enabled
   - **CPU Frequency:** 240MHz
   - **Flash Mode:** QIO 80MHz
   - **Flash Size:** 16MB
   - **Partition Scheme:** Default 4MB with spiffs
   - **PSRAM:** OPI PSRAM
   - **Upload Speed:** 921600
   - **USB Mode:** Hardware CDC and JTAG

3. **Tools → Port:** Select `/dev/ttyACM0` (or `/dev/ttyACM1`)

### Step 6: Upload

1. Click **Upload** button (→ arrow icon)
2. Wait for compilation
3. If upload fails, hold **BOOT** button and click **Upload** again
4. Wait for "Hard resetting via RTS pin..."

### Step 7: Test Touch

1. **Tools → Serial Monitor** (or Ctrl+Shift+M)
2. Set baud rate to **115200**
3. You should see:
   ```
   LVGL porting example start
   Initialize panel device
   Create UI
   LVGL porting example end
   ```
4. Display should show LVGL widgets demo
5. **Touch the screen** - widgets should respond!

---

## Option 2: Using esptool.py (Pre-compiled Binary)

If you just want to flash without Arduino IDE:

### Step 1: Build in Arduino IDE First

Follow Option 1 steps 1-6, then:

1. **Sketch → Export Compiled Binary**
2. Wait for compilation
3. Binary saved to sketch folder as `DEMO_LVGL.ino.bin`

### Step 2: Flash with esptool

```bash
cd ~/PycharmProjects/CheapBlackDisplay/JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL

# Find the compiled binary (in build folder)
find . -name "*.bin" -type f

# Flash
python -m esptool --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m \
  0x0 DEMO_LVGL.ino.bin
```

---

## Option 3: Using PlatformIO

See **PLATFORMIO_SETUP.md** for complete PlatformIO setup guide.

Quick version:

```bash
# Install PlatformIO
pip install platformio

# Create project
cd ~/PycharmProjects/CheapBlackDisplay
mkdir arduino_demo && cd arduino_demo
pio project init -b esp32-s3-devkitc-1

# Copy files
cp ../JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/DEMO_LVGL.ino src/main.cpp
cp ../JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/*.h include/
cp ../JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/*.c src/

# Configure platformio.ini (see PLATFORMIO_SETUP.md)

# Build and upload
pio run -t upload

# Monitor
pio device monitor
```

---

## Expected Results

### Display Output

You should see the **LVGL Widgets Demo** with:
- Multiple tabs at the top
- Various widgets: buttons, sliders, checkboxes
- Charts and graphs
- Text and labels
- Colorful UI elements

### Touch Functionality

**Touch should work perfectly:**
- ✅ Tap buttons - they respond
- ✅ Drag sliders - they move
- ✅ Switch tabs - they change
- ✅ Scroll lists - they scroll
- ✅ All touch interactions work smoothly

### Serial Output

```
LVGL porting example start
Initialize panel device
Create UI
LVGL porting example end
IDLE loop
IDLE loop
...
```

When you touch elements, you may see debug output if enabled.

---

## Troubleshooting

### Upload Failed

**Error: "Failed to connect"**
```bash
# Hold BOOT button while clicking Upload
# Or try slower baud rate in Tools → Upload Speed → 115200
```

**Error: "Permission denied"**
```bash
sudo chmod 666 /dev/ttyACM0
# Or add to dialout group:
sudo usermod -a -G dialout $USER
```

### Compilation Errors

**Error: "lvgl.h not found"**
- Install lvgl library via Library Manager
- Or copy libraries folder as shown in Step 3

**Error: "esp_bsp.h not found"**
- Make sure all files from DEMO_LVGL folder are in the sketch directory
- Check that .h and .c files are present

### Display Issues

**Black screen:**
- Check USB cable (use good quality cable)
- Verify board is powered (LED should be on)
- Try power cycle (unplug and replug)

**Wrong orientation:**
- Edit DEMO_LVGL.ino
- Change line 16: `#define LVGL_PORT_ROTATION_DEGREE (90)`
- Try values: 0, 90, 180, 270

### Touch Not Working

**If touch doesn't work in Arduino demo:**
- This would be very unusual (Arduino touch is proven working)
- Check serial output for touch initialization messages
- Verify I2C pins in esp_bsp.c (SDA=4, SCL=8)
- Report as hardware issue

**If touch works in Arduino but not MicroPython:**
- This confirms our findings: MicroPython LVGL v9 firmware bug
- Touch hardware is perfect
- Use Arduino for production or wait for MicroPython fix

---

## Comparison: Arduino vs MicroPython

| Feature | Arduino DEMO_LVGL | MicroPython |
|---------|-------------------|-------------|
| **Display** | ✅ Works | ✅ Works |
| **Touch** | ✅ Works | ❌ Broken (firmware bug) |
| **LVGL Version** | v8.3 | v9.2.2 |
| **Language** | C/C++ | Python |
| **Performance** | Faster | Slower |
| **Development** | More code | Less code |
| **Libraries** | Extensive | Limited |

---

## Next Steps After Successful Flash

### If Touch Works (Expected)

1. ✅ **Confirmed:** Touch hardware is perfect
2. ✅ **Confirmed:** Arduino + LVGL works great
3. **Decision:** Use Arduino for your project or wait for MicroPython fix

### Develop Your Application

Choose your path:

**Path 1: Continue with Arduino**
- Modify DEMO_LVGL.ino for your needs
- Add custom UI elements
- Touch will work perfectly
- See PLATFORMIO_SETUP.md for better development workflow

**Path 2: Wait for MicroPython Fix**
- Create GitHub issue (use GITHUB_ISSUE.md template)
- Monitor firmware repository for updates
- Use Arduino temporarily

**Path 3: Hybrid Approach**
- Develop UI in Arduino (working touch)
- Port to MicroPython when fixed
- Keep both versions

---

## Restore MicroPython Later

If you want to go back to MicroPython:

```bash
cd ~/PycharmProjects/CheapBlackDisplay/ESP32-JC3248W535-Micropython-LVGL-main

python -m esptool --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m \
  --erase-all 0x0 lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-16_NEW_SPI.bin
```

---

## Files Needed

All files are in:
```
~/PycharmProjects/CheapBlackDisplay/JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/
```

**Main files:**
- `DEMO_LVGL.ino` - Main sketch
- `display.h` - Display configuration
- `esp_bsp.h` / `esp_bsp.c` - Board support
- `lv_port.h` / `lv_port.c` - LVGL port
- `lv_conf.h` - LVGL configuration

**Libraries folder:**
- `libraries/lvgl/` - LVGL library

---

*Created: 2026-04-03*
*Purpose: Flash Arduino demo to verify touch works*
*Expected Result: Touch works perfectly, confirming hardware is good*
