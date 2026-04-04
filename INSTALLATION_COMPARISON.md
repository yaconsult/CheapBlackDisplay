# Installation Options Comparison for JC3248W535

## Complete Disk Space and Installation Guide

This document compares all installation options for flashing code to the JC3248W535 board, including disk space requirements, installation time, and use cases.

---

## Quick Comparison Table

| Method | Disk Space | Install Time | Difficulty | Best For |
|--------|-----------|--------------|------------|----------|
| **esptool.py only** | 10 MB | 1 min | Easy | Flashing pre-compiled binaries |
| **Arduino CLI** | 1.5-2 GB | 10-15 min | Medium | Command-line development |
| **Arduino IDE** | 2-3 GB | 15-20 min | Easy | GUI-based development, testing |
| **PlatformIO CLI** | 3-4 GB | 15-20 min | Medium | Professional development |
| **PlatformIO IDE** | 4-5 GB | 20-30 min | Easy | Full IDE experience |

---

## Option 1: esptool.py Only (Minimal)

### Use Case
- Only need to flash pre-compiled `.bin` files
- Don't need to compile code
- Minimal disk space available

### Disk Space Requirements
```
esptool.py:           ~10 MB
Python dependencies:  ~5 MB
Total:                ~15 MB
```

### Installation

```bash
# In your virtual environment
source .venv/bin/activate
pip install esptool
# or
uv pip install esptool
```

### What You Can Do
- ✅ Flash factory firmware
- ✅ Flash pre-compiled Arduino binaries
- ✅ Backup/restore firmware
- ✅ Erase flash
- ❌ Cannot compile code
- ❌ Cannot modify source

### Pros
- Minimal disk space
- Fast installation
- Simple to use

### Cons
- Cannot compile your own code
- Need pre-built binaries

---

## Option 2: Arduino CLI (Command Line)

### Use Case
- Command-line development
- Scripting and automation
- No GUI needed
- Moderate disk space

### Disk Space Requirements
```
Arduino CLI:          ~50 MB
ESP32 platform:       ~1.2 GB
  - Toolchain:        ~800 MB
  - Framework:        ~300 MB
  - Tools:            ~100 MB
Libraries (LVGL):     ~200 MB
Build cache:          ~500 MB
Total:                ~1.5-2 GB
```

### Installation

```bash
# Download Arduino CLI
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Add to PATH
export PATH=$PATH:$HOME/bin

# Install ESP32 platform
arduino-cli config init
arduino-cli config add board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
arduino-cli core update-index
arduino-cli core install esp32:esp32@3.0.2

# Install libraries
arduino-cli lib install "lvgl@8.3.11"
```

### What You Can Do
- ✅ Compile Arduino sketches
- ✅ Upload to board
- ✅ Manage libraries
- ✅ Script builds
- ❌ No GUI
- ❌ Manual code editing

### Pros
- Smaller than Arduino IDE
- Good for automation
- Fast compilation

### Cons
- Command-line only
- Need separate text editor
- Less beginner-friendly

---

## Option 3: Arduino IDE (GUI)

### Use Case
- Beginner-friendly
- Visual development
- Quick testing
- Learning Arduino

### Disk Space Requirements
```
Arduino IDE 2.x:      ~600 MB
  - Application:      ~400 MB
  - Runtime:          ~200 MB
ESP32 platform:       ~1.2 GB
  - Toolchain:        ~800 MB
  - Framework:        ~300 MB
  - Tools:            ~100 MB
Libraries (LVGL):     ~200 MB
Build cache:          ~500 MB
Total:                ~2.5-3 GB
```

**Location of files:**
```
~/Arduino/                    (sketches and libraries)
~/.arduino15/                 (IDE settings and platforms)
~/.arduino15/packages/esp32/  (ESP32 platform - largest)
```

### Installation

**Method A: Download AppImage (Recommended)**
```bash
# Check space
df -h ~

# Download (400 MB)
wget https://downloads.arduino.cc/arduino-ide/arduino-ide_2.3.2_Linux_64bit.AppImage
chmod +x arduino-ide_2.3.2_Linux_64bit.AppImage

# Run
./arduino-ide_2.3.2_Linux_64bit.AppImage
```

**Method B: Package Manager**
```bash
sudo apt install arduino
# Older version (1.8.x), smaller size (~200 MB)
```

### What You Can Do
- ✅ Visual code editor
- ✅ Compile and upload
- ✅ Serial monitor
- ✅ Library manager
- ✅ Board manager
- ✅ Beginner-friendly

### Pros
- Easy to use
- Visual interface
- Built-in examples
- Good for learning

### Cons
- Larger disk space
- Slower than CLI
- Less automation

---

## Option 4: PlatformIO CLI

### Use Case
- Professional development
- Multiple projects
- Advanced features
- CI/CD integration

### Disk Space Requirements
```
PlatformIO Core:      ~500 MB
ESP32 platform:       ~1.5 GB
  - Toolchain:        ~900 MB
  - Framework:        ~400 MB
  - Tools:            ~200 MB
Libraries:            ~100 MB
Build cache:          ~500 MB per project
Total:                ~3-4 GB
```

**Location of files:**
```
~/.platformio/        (all PlatformIO data)
~/project/.pio/       (per-project build cache)
```

### Installation

```bash
# In virtual environment
source .venv/bin/activate

# Install PlatformIO
pip install platformio
# or
uv pip install platformio

# Verify
pio --version

# First project setup downloads platform (~1.5 GB)
pio project init -b esp32-s3-devkitc-1
```

### What You Can Do
- ✅ Advanced project management
- ✅ Multiple frameworks
- ✅ Unit testing
- ✅ Library dependency management
- ✅ CI/CD integration
- ✅ Custom build scripts

### Pros
- Professional features
- Better dependency management
- Faster builds
- Multi-platform support

### Cons
- Larger disk space
- Steeper learning curve
- Command-line focused

---

## Option 5: PlatformIO IDE (VS Code Extension)

### Use Case
- Full IDE experience
- Visual debugging
- Integrated terminal
- Professional development

### Disk Space Requirements
```
VS Code:              ~300 MB
PlatformIO Extension: ~200 MB
PlatformIO Core:      ~500 MB
ESP32 platform:       ~1.5 GB
Libraries:            ~100 MB
Build cache:          ~500 MB per project
Total:                ~4-5 GB
```

### Installation

```bash
# Install VS Code
wget https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64
sudo dpkg -i code_*.deb

# Or use snap
sudo snap install code --classic

# Open VS Code
code

# Install PlatformIO extension:
# 1. Click Extensions (Ctrl+Shift+X)
# 2. Search "PlatformIO IDE"
# 3. Click Install
# 4. Restart VS Code
```

### What You Can Do
- ✅ Full IDE features
- ✅ Visual debugging
- ✅ IntelliSense
- ✅ Git integration
- ✅ Terminal integration
- ✅ Project management

### Pros
- Best development experience
- Visual debugging
- Integrated tools
- Professional features

### Cons
- Largest disk space
- Most complex setup
- Resource intensive

---

## Detailed Disk Space Breakdown

### ESP32 Platform Components

**What takes up space in ESP32 support:**

```
Xtensa GCC Toolchain:     ~800-900 MB
  - Compiler (gcc):       ~400 MB
  - Linker (ld):          ~200 MB
  - Libraries (libc):     ~200 MB
  - Tools (objcopy, etc): ~100 MB

ESP32 Arduino Framework:  ~300-400 MB
  - Core libraries:       ~150 MB
  - WiFi/BT libraries:    ~100 MB
  - Peripheral drivers:   ~50 MB
  - Examples:             ~50 MB

Platform Tools:           ~100-200 MB
  - esptool.py:           ~10 MB
  - mkspiffs:             ~20 MB
  - Other utilities:      ~70 MB
```

### Build Cache

**Per-project build artifacts:**

```
Compiled objects (.o):    ~200 MB
Linked binaries (.elf):   ~50 MB
Flash images (.bin):      ~2-5 MB
Dependency cache:         ~100 MB
Temporary files:          ~50 MB

Total per project:        ~400-500 MB
```

**Tip:** Clean build cache regularly:
```bash
# Arduino IDE: Sketch → Clean Build Folder
# Arduino CLI: rm -rf build/
# PlatformIO: pio run -t clean
```

---

## Recommendations by Use Case

### Just Testing (Flash Demo)
**Recommended:** Arduino IDE
- **Space:** 2-3 GB
- **Time:** 15-20 min
- **Difficulty:** Easy
- See: `FLASH_ARDUINO_DEMO.md`

### Learning Arduino
**Recommended:** Arduino IDE
- **Space:** 2-3 GB
- **Time:** 15-20 min
- **Difficulty:** Easy
- Best for beginners

### Professional Development
**Recommended:** PlatformIO CLI or IDE
- **Space:** 3-5 GB
- **Time:** 20-30 min
- **Difficulty:** Medium
- See: `PLATFORMIO_SETUP.md`

### Automation/CI/CD
**Recommended:** Arduino CLI or PlatformIO CLI
- **Space:** 1.5-4 GB
- **Time:** 10-20 min
- **Difficulty:** Medium
- Good for scripts

### Minimal Setup (Flash Only)
**Recommended:** esptool.py
- **Space:** 10 MB
- **Time:** 1 min
- **Difficulty:** Easy
- Cannot compile code

---

## Space-Saving Tips

### Clean Build Cache Regularly

```bash
# Arduino IDE
# Sketch → Clean Build Folder

# Arduino CLI
rm -rf ~/Arduino/build/

# PlatformIO
pio run -t clean
# Or remove entire build folder
rm -rf .pio/
```

### Remove Unused Platforms

```bash
# Arduino CLI
arduino-cli core uninstall <platform>

# PlatformIO
pio platform uninstall <platform>
```

### Use Shared Libraries

```bash
# PlatformIO: Use global lib_dir instead of per-project
# In platformio.ini:
lib_extra_dirs = ~/.platformio/lib
```

### Compress Old Projects

```bash
# Archive completed projects
tar -czf project_backup.tar.gz project_folder/
rm -rf project_folder/
```

---

## Installation Time Estimates

| Step | Arduino IDE | Arduino CLI | PlatformIO |
|------|-------------|-------------|------------|
| Download tool | 5 min | 1 min | 1 min |
| Install tool | 2 min | 1 min | 5 min |
| Download ESP32 | 10 min | 10 min | 10 min |
| Install ESP32 | 3 min | 3 min | 3 min |
| Install libraries | 2 min | 2 min | 2 min |
| **Total** | **~20 min** | **~15 min** | **~20 min** |

*Times based on 10 Mbps connection*

---

## Checking Available Disk Space

### Before Installation

```bash
# Check free space
df -h ~

# Check specific directory
du -sh ~/.arduino15/
du -sh ~/.platformio/

# Find large files
du -h ~ | sort -rh | head -20
```

### After Installation

```bash
# Arduino IDE
du -sh ~/.arduino15/
du -sh ~/Arduino/

# PlatformIO
du -sh ~/.platformio/
du -sh ~/project/.pio/

# Total for all Arduino/PlatformIO
du -sh ~/.arduino15/ ~/.platformio/ ~/Arduino/
```

---

## Minimum Requirements Summary

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Free Disk Space** | 2 GB | 5 GB |
| **RAM** | 2 GB | 4 GB |
| **Internet Speed** | 1 Mbps | 10 Mbps |
| **USB Ports** | 1 | 2 |

---

## What to Install for Your Situation

### Situation 1: "I just want to test if touch works"
→ **Arduino IDE** (2-3 GB, easy)
- Follow `FLASH_ARDUINO_DEMO.md`
- Quick test, no development needed

### Situation 2: "I want to develop my own application"
→ **PlatformIO** (3-4 GB, best features)
- Follow `PLATFORMIO_SETUP.md`
- Professional development environment

### Situation 3: "I have limited disk space"
→ **Arduino CLI** (1.5-2 GB, minimal)
- Command-line only
- Can still compile and upload

### Situation 4: "I only need to flash firmware"
→ **esptool.py** (10 MB, minimal)
- Just for flashing binaries
- Cannot compile code

---

*Created: 2026-04-03*
*Purpose: Help choose installation method based on disk space and needs*
