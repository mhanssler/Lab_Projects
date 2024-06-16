"""This script will check the usb connections on the lab pi"""

import usb.core
import usb.util

# Find USB devices
devices = usb.core.find(find_all=True)

# Loop through devices and print information
for device in devices:
    print(f'Device: {device}')
