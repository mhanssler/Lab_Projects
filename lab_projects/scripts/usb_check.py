"""This script will check the usb connections on the lab pi"""

import usb.core
import usb.util
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Find USB devices
devices = usb.core.find(find_all=True)

# Loop through devices and print information
for device in devices:
    logging.info(f'Device: {device}')
