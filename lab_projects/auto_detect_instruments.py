import subprocess
import re
import pyvisa

def detect_rigol_devices():
    result = subprocess.run(['lsusb'], capture_output=True, text=True)
    devices = result.stdout
    rigol_devices = re.findall(r'Bus \d+ Device \d+: ID (\w+:\w+) Rigol Technologies', devices)
    return rigol_devices

def connect_to_device(device_id):
    rm = pyvisa.ResourceManager()
    try:
        instrument = rm.open_resource('USB::' + device_id)
        return instrument
    except pyvisa.VisaIOError:
        print(f"Could not connect to device with ID {device_id}")
        return None

def query_device_state(device):
    try:
        # Replace with actual query commands for your devices
        identity = device.query('*IDN?')
        print(f"Device ID: {identity}")
    except Exception as e:
        print(f"Error querying device: {e}")

def main():
    rigol_device_ids = detect_rigol_devices()
    if not rigol_device_ids:
        print("No Rigol devices found")
        return

    for device_id in rigol_device_ids:
        device = connect_to_device(device_id)
        if device:
            query_device_state(device)
            device.close()

if __name__ == "__main__":
    main()
