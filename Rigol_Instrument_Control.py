import pyvisa

def list_devices():
    rm = pyvisa.ResourceManager()
    return rm.list_resources()

def ps_set_voltage(instrument, voltage, channel):
    # Ensure voltage is a string. If it's a numeric type, convert it.
    voltage = str(voltage)

    scpi_command = f":SOURce{channel}:VOLTage:LEVel:IMMediate:AMPLitude {voltage}"
    print("Sending SCPI command:", scpi_command)  # For debugging

    try:
        instrument.write(scpi_command)
    except Exception as e:
        print("Error sending command:", e)

#def scope_capture_autoset()



def connect_device(address):
    rm = pyvisa.ResourceManager()
    return rm.open_resource(address)

def main():
    devices = list_devices()
    print("Connected devices:", devices)
    voltage = input("Please Enter the Voltage for the Power Supply 0-30 ")
    channel = input("please Enter the Channel for the Power Supply 1, 2 ")

    # Example: connect to a device (replace with actual address)
    power_supply = 'USB0::0x1AB1::0x0E11::DP8C172602885::INSTR'
    Load = 'USB0::0x1AB1::0x0E11::DL3A222000386::INSTR'
    O_scope = 'USB0::0x1AB1::0x0588::DS1ET153818956::INSTR'

    instrument = connect_device(power_supply)
    ps_set_voltage(instrument, voltage, channel)
    # Replace with actual SCPI commands for your instruments
    instrument.write('*IDN?')
    print("",instrument.read())

if __name__ == "__main__":
    main()
