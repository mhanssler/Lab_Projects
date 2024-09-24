import usb.core
import usb.util

# Define Vendor and Product IDs based on lsusb output
devices = [
    {'vid': 0x1AB1, 'pid': 0x0588, 'name': 'DS1000 SERIES'},
    {'vid': 0x1AB1, 'pid': 0x0E11, 'name': 'DL3000 Serials'},
    {'vid': 0x1AB1, 'pid': 0x0E11, 'name': 'DP800 Serials'}
]

# Attempt to find each device and communicate
for device in devices:
    try:
        dev = usb.core.find(idVendor=device['vid'], idProduct=device['pid'])
        if dev is None:
            print(f"Device {device['name']} not found.")
            continue

        print(f"Connected to {device['name']}.")

        # Set the active configuration
        dev.set_configuration()

        # Access the first configuration and first interface
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]

        # Find OUT (to send commands) and IN (to receive responses) endpoints
        ep_out = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )

        ep_in = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )

        # Check that endpoints are correctly identified
        if not ep_out or not ep_in:
            print(f"Could not identify endpoints for {device['name']}.")
            continue

        # Send the command to identify the device
        ep_out.write(b'*IDN?')

        # Read the response (size depends on expected response length)
        response = ep_in.read(64, timeout=5000)  # Adjust size and timeout as needed
        print(f"Response from {device['name']}: {''.join([chr(x) for x in response])}")

    except usb.core.USBError as e:
        if e.errno == 110:  # Timeout error
            print(f"Error communicating with {device['name']}: Operation timed out.")
        elif e.errno == 16:  # Resource busy error
            print(f"Error communicating with {device['name']}: Resource busy.")
        else:
            print(f"Unexpected USB error with {device['name']}: {e}")
    except Exception as e:
        print(f"General error with {device['name']}: {e}")
