# TRIKI Library
A Python library for the integrating TRIKI motion controller (made by Caps Apps) into your projects.

> This library is still in development. Some things may change sligthly.

---

## What is TRIKI?
TRIKI is a Bluetooth Low Energy (BLE) motion controller that has the shape and size of a bottle cap. It is produced by Caps Apps (also known as HOPX) and sold by 'Żabka', a convenience store franchise.

It was designed to be used in mini-games which are on the store's loyalty app.

## Why I made this library
I wanted to make this library to give everyone a way to integrate this niche controller into their own games, experiments and other Python projects.

## Features
- Scan for TRIKI controllers
- Connect to TRIKI controller
- Get battery level
- Get FW version
- Get IMU data from the controller
- Get state of the built-in button
- Control built-in LED

## Platforms
| Platform      | Does it work?       |
|---------------|---------------------|
| Windows 10/11 | ✅ Tested            |
| macOS         | ❔ Untested          |
| Linux         | ⚠️ Partially tested |
> Linux support needs further testing. Some Arch-based distributions may have issues with receiving data.
---
## Installation
```bash
pip install triki-library
```

## Usage
```python
# Import the library
import asyncio
from triki import TRIKIScanner, TRIKIController
```

```python
# Scan for TRIKI controllers
scanner = TRIKIScanner()
await scanner.scan()
devices = scanner.scanned_devices # Returned as list[TRIKIDevice]

devices[0].name # Get device name
devices[0].address # Get device BT address
```
```python
# Connect to the controller
controller = TRIKIController("AA:BB:CC:DD:EE:FF")
await controller.connect()
```
```python
controller.is_connected # Check if device is connected
controller.battery_level # Get battery level
device.firmware_version # Get FW version
```
```python
controller.spin_x # Get X Spin
controller.spin_y # Get Y Spin
controller.turn_z # Get Z Turn
controller.tilt_x # Get X Tilt
controller.tilt_y # Get Y Tilt
controller.flip_z # Get Z Flip
```
```python
controller.button_pressed # Check if built-in button is pressed
```
```python
#turn on LED
await controller.toggle_led(True)

#turn off LED
await controller.toggle_led(False)
```
```python
# Loop
try:
    while controller.is_connected:
        # Do stuff
finally:
    await controller.disconnect()
```
```python
# IMPORTANT: disconnect from the controller when you're done with it!
await controller.disconnect()
```
>Examples can be found on the 'examples' directory.
---

## Credits
Library made by [Woofter_Wolf](https://woofterwolf.space)

Special thanks to [Wojciech "Koksny" Górny](https://koksny.com) for doing the hard work of documenting this device (look here for communication documentation): [Link](https://github.com/koksny/TRIKI-Control)

## Copyright
"TRIKI" and "Żabka" are trademarks of Żabka Polska sp. z o.o. "HOPX" is a trademark of Caps Apps sp. z o.o.

This library is an independent, open-source project. It is **NOT** affiliated, endorsed or sponsored by these companies. This library ships with no software, images or any assets belonging to these companies.