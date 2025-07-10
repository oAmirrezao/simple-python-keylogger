# Python Keylogger

A simple, fully documented Python keylogger using [`pynput`](https://pypi.org/project/pynput/).

---

## ⚠️ Warning & Ethics

**Please use responsibly and legally.**  
Do not run this software on any computer without explicit permission. Unauthorized keylogging is illegal and unethical.

---

## Features

- Logs every key press (with timestamps) to a customizable text file.
- Optionally prints each keystroke live to the console.
- Cleanly stops when `<Esc>` key is pressed.
- Command-line configurable output file and console logging.
- Easy to understand and extend — great for learning.

---

## Requirements

- Python 3.x
- `pynput` library (`pip install pynput`)

---

## Usage

```bash
# Log keys silently to default "keylog.txt"
python keylogger.py

# Log keys to a custom file and print keys live on console
python keylogger.py --file mylog.txt --console
