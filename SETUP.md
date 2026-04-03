# Setup Instructions

## Virtual Environment Setup

This project uses a Python virtual environment in `.venv` to manage dependencies.

### First Time Setup

1. **Create virtual environment using uv** (recommended):
```bash
uv venv
```

Or using standard Python:
```bash
python3 -m venv .venv
```

2. **Activate virtual environment**:
```bash
source .venv/bin/activate
```

3. **Install dependencies using uv** (faster):
```bash
uv pip install -r requirements.txt
```

Or using standard pip:
```bash
pip install -r requirements.txt
```

### PyCharm Setup

PyCharm should automatically detect the `.venv` virtual environment.

#### Configure PyCharm to Use .venv

1. **File** → **Settings** (or **Ctrl+Alt+S**)
2. **Project: CheapBlackDisplay** → **Python Interpreter**
3. Click the gear icon → **Add**
4. Select **Existing environment**
5. Browse to: `/home/lpinard/PycharmProjects/CheapBlackDisplay/.venv/bin/python`
6. Click **OK**

PyCharm terminal will now automatically activate the virtual environment.

### Running Tests with Virtual Environment

#### In PyCharm Terminal (Recommended)
PyCharm terminal automatically activates `.venv`:
```bash
python quick_test.py
python run_test.py test_landscape_mode
```

#### In System Terminal
Activate the virtual environment first:
```bash
cd /home/lpinard/PycharmProjects/CheapBlackDisplay
source .venv/bin/activate
python quick_test.py
```

#### Without Activating (Direct Path)
```bash
.venv/bin/python quick_test.py
```

### Verify Installation

Test if pyserial is installed:
```bash
python3 -c "import serial; print('pyserial is installed')"
```

Should print: `pyserial is installed`

### Check Python Version

```bash
python3 --version
```

Should show: `Python 3.14.3` (or similar)

## Running Tests After Setup

Once pyserial is installed:

```bash
# In PyCharm terminal or system terminal
python3 quick_test.py
python3 run_test.py test_landscape_mode
python3 run_test.py test_portrait_mode
```

## Troubleshooting

### "No module named 'serial'"

**Cause:** PyCharm is using a virtual environment or different Python interpreter that doesn't have pyserial.

**Solution 1 - Install in current environment:**
```bash
pip3 install --user pyserial
```

**Solution 2 - Use system Python:**
```bash
/usr/bin/python3 quick_test.py
```

**Solution 3 - Configure PyCharm interpreter:**
1. File → Settings → Project → Python Interpreter
2. Select system Python 3.14
3. Install pyserial package

### Permission Denied on /dev/ttyACM*

**Cause:** User not in `dialout` group.

**Solution:**
```bash
sudo usermod -a -G dialout $USER
```

Then log out and log back in.

### Board Not Found

**Check connection:**
```bash
ls -la /dev/ttyACM*
```

Should show `/dev/ttyACM0` or `/dev/ttyACM1`

**If not found:**
- Check USB cable is plugged in
- Try different USB port
- Check board has power (LED on)

## System Requirements

- **OS**: Linux (Fedora or similar)
- **Python**: 3.14+ (or 3.8+)
- **USB**: Board connected via USB
- **Permissions**: User in `dialout` group

## Quick Verification

Run all checks:
```bash
# Check Python version
python3 --version

# Check pyserial
python3 -c "import serial; print('OK')"

# Check board connection
ls -la /dev/ttyACM*

# Check permissions
groups | grep dialout
```

All should succeed before running tests.
