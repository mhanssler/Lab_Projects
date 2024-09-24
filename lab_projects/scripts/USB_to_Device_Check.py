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

        # Set the active configuration (usually needed for USBTMC devices)
        dev.set_configuration()

        # Find the OUT and IN endpoints (adjust based on your device's configuration)
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]

        # OUT endpoint is usually EP1 OUT (endpoint address 0x01)
        ep_out = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )

        # IN endpoint is usually EP1 IN (endpoint address 0x81)
        ep_in = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )

        # Send the command to identify the device
        ep_out.write(b'*IDN?')

        # Read the response (size depends on expected response length)
        response = ep_in.read(64)# Adjust size as needed
        print(f"Response from {device['name']}: {''.join([chr(x) for x in response])}")

    except Exception as e:
        print(f"Error communicating with {device['name']}: {e}")
