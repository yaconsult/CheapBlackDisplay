# Restoring Original Firmware Backup

## Purpose

Restore the original firmware backup to verify that touch hardware is still functional after all our testing. This will confirm whether the issue is purely firmware-related or if any hardware damage occurred.

## Prerequisites

- Original firmware backup file (created before flashing MicroPython)
- esptool.py installed (`pip install esptool` or `uv pip install esptool`)
- Board connected via USB

## Backup File Location

The backup should have been created before flashing MicroPython. If you followed standard backup procedures, you should have:

**Typical backup command used:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 read_flash 0x0 0x1000000 backup_original.bin
```

**Expected file:**
- `backup_original.bin` (16MB for full flash backup)
- Or separate partition backups if you backed up individually

## Restore Procedure

### Step 1: Identify Your Serial Port

```bash
ls /dev/ttyACM*
# Should show /dev/ttyACM0 or /dev/ttyACM1
```

### Step 2: Erase Flash (Recommended)

```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 erase_flash
```

**Wait for:** "Chip erase completed successfully"

### Step 3: Restore Backup

**If you have a full flash backup:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m \
  0x0 backup_original.bin
```

**If you have partition backups:**
```bash
# Restore bootloader
esptool.py --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  write_flash 0x0 bootloader.bin

# Restore partition table
esptool.py --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  write_flash 0x8000 partition-table.bin

# Restore application
esptool.py --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  write_flash 0x10000 firmware.bin
```

### Step 4: Reset Board

After flashing completes:
1. Unplug USB cable
2. Wait 5 seconds
3. Plug USB cable back in
4. Board should boot with original firmware

## Verification

### What to Check

1. **Display Powers On**
   - Screen should light up
   - Original demo/app should appear

2. **Touch Functionality**
   - Touch the screen
   - UI should respond to touches
   - Buttons should work
   - Swipe gestures should work

3. **Multi-App Demo** (if that was the original firmware)
   - Should show multiple demo applications
   - Touch navigation should work
   - All demos should be accessible

### Expected Results

**If touch works:**
- ✅ Touch hardware is fine
- ✅ Issue is purely MicroPython firmware bug
- ✅ Safe to proceed with Arduino firmware or wait for fix

**If touch doesn't work:**
- ⚠️ Possible hardware issue
- ⚠️ May need to contact manufacturer
- ⚠️ Check connections and cables

## Troubleshooting

### "No serial port found"

```bash
# Check USB connection
lsusb | grep -i esp

# Check permissions
sudo chmod 666 /dev/ttyACM0

# Try other port
ls /dev/ttyACM*
```

### "Failed to connect"

1. Hold BOOT button while connecting USB
2. Try lower baud rate: `-b 115200` instead of `-b 460800`
3. Try different USB cable
4. Try different USB port on computer

### "Flash size mismatch"

Adjust `--flash_size` parameter:
- 4MB: `--flash_size 4MB`
- 8MB: `--flash_size 8MB`
- 16MB: `--flash_size 16MB`

Check your board's actual flash size in original documentation.

### Restore fails partway through

1. Erase flash completely first
2. Try slower baud rate
3. Check USB cable quality
4. Ensure stable power supply

## If You Don't Have a Backup

### Option 1: Use Manufacturer's Firmware

If the manufacturer provides firmware downloads:
1. Download original firmware from manufacturer
2. Flash using their instructions
3. Usually similar to restore procedure above

### Option 2: Use Arduino Firmware

Flash the working Arduino firmware:
```bash
cd JC3248W535EN/1-Demo/Demo_Arduino/DEMO_LVGL/

# Build in Arduino IDE, then flash the .bin file
# Or use pre-built binary if available
```

### Option 3: Keep MicroPython

If you don't have a backup and can't get original firmware:
- Touch won't work in MicroPython (confirmed bug)
- Display works fine
- Can still develop display-only applications
- Wait for firmware developer to fix touch

## After Verification

### If Touch Works in Original Firmware

**Next Steps:**
1. Document that touch hardware is confirmed working
2. Decide between:
   - **Arduino firmware** (touch works, use Arduino IDE)
   - **Wait for MicroPython fix** (timeline unknown)
   - **Keep original firmware** (if it meets your needs)

### If Touch Doesn't Work

**Next Steps:**
1. Check all physical connections
2. Inspect ribbon cables
3. Contact manufacturer about hardware issue
4. Consider RMA/replacement if under warranty

## Re-flashing MicroPython Later

If you want to go back to MicroPython after testing:

```bash
cd ESP32-JC3248W535-Micropython-LVGL-main

python -m esptool --chip esp32s3 --port /dev/ttyACM0 -b 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m \
  --erase-all 0x0 lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-16_NEW_SPI.bin
```

## Safety Notes

- ⚠️ Flashing firmware can brick your device if interrupted
- ⚠️ Ensure stable power during flashing
- ⚠️ Don't disconnect USB during flash process
- ⚠️ Keep backup files safe for future use
- ⚠️ Test on non-critical device first if possible

## Documentation

After restoring and testing, document your findings:

1. **Touch works:** Update `TOUCH_RESEARCH.md` with confirmation
2. **Touch doesn't work:** Document hardware issue
3. **Firmware choice:** Document which firmware you're using going forward

---

*Created: 2026-04-03*
*Purpose: Verify touch hardware functionality*
