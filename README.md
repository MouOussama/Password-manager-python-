# Password-manager-python-

A simple Python password manager using PyQt5 and Qt Designer UI.

## Features
- Enter your name
- Select or type a site (editable combo box)
- Generate password: Low (8 chars alphanum), Medium (12 chars + symbols), High (16 chars complex)
- Manually type password
- Save to `passwords.txt`
- Retrieve existing password for name + site

## Requirements
- Python 3.9+
- PyQt5 (already installed)

## Run
```
python3 main.py
```

Passwords stored plainly in `passwords.txt` as `name:site:password` lines. **Not secure for production!**

## File Structure
- `main.py`: Application logic
- `password_manager.ui`: UI designed with Qt Designer (XML)
- `passwords.txt`: Generated on first save

