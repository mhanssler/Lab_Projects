import pyvisa

def list_devices():
    rm = pyvisa.ResourceManager()
    devices = rm.list_resources()
    print("Connected devices:", devices)  # For debugging
    return devices

def ps_set_voltage(instrument, voltage, channel):
    voltage = str(voltage)  # Convert voltage to string if it's numeric
    scpi_command = f":SOURce{channel}:VOLTage:LEVel:IMMediate:AMPLitude {voltage}"
    print("Sending SCPI command:", scpi_command)  # For debugging

    try:
        instrument.write(scpi_command)
    except Exception as e:
        print("Error sending command:", e)

def connect_device(address):
    rm = pyvisa.ResourceManager()
    try:
        instrument = rm.open_resource(address)
        instrument.timeout = 5000  # Set timeout to 5 seconds (adjust if needed)
        print(f"Connected to {address}")  # Debug confirmation
        return instrument
    except Exception as e:
        print(f"Error connecting to device at {address}: {e}")
        return None

def main():
    devices = list_devices()
    if not devices:
        print("No devices found. Please check connections and try again.")
        return
    
    # Display connected devices for user selection
    for index, device in enumerate(devices):
        print(f"{index + 1}: {device}")

    try:
        device_choice = int(input("Select the device number for the power supply: ")) - 1
        if device_choice < 0 or device_choice >= len(devices):
            print("Invalid selection. Exiting.")
            return
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the device.")
        return

    # Get selected device address
    power_supply = devices[device_choice]

    voltage = input("Please Enter the Voltage for the Power Supply (0-30): ")
    channel = input("Please Enter the Channel for the Power Supply (1, 2): ")

    instrument = connect_device(power_supply)
    if instrument is None:
        print("Failed to connect to the power supply. Exiting.")
        return

    try:
        # Set voltage
        ps_set_voltage(instrument, voltage, channel)

        # Send a simple SCPI command to test communication
        instrument.write('*IDN?')
        response = instrument.read()
        print("Instrument ID:", response)
    except Exception as e:
        print("Error during instrument operation:", e)
    finally:
        # Ensure the instrument is closed properly
        instrument.close()
        print("Instrument connection closed.")

if __name__ == "__main__":
    main()
