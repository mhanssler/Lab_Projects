import pyvisa
import Power_Supply_Control

def list_devices():
    try:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()
    except Exception as e:
        print("Error listing devices:", e)
        return []
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
    try:
        rm = pyvisa.ResourceManager()
        return rm.open_resource(address)    
    except Exception as e:
        print("Error connecting to device:", e)
        return None

def main():
    devices = list_devices()
    if not devices:
        print("No devices found")
        return
    print("Connected devices:", devices)
    voltage = input("Please Enter the Voltage for the Power Supply 0-30 ")
    channel = input("please Enter the Channel for the Power Supply 1, 2 ")

    # Example: connect to a device (replace with actual address)
    power_supply = 'USB0::0x1AB1::0x0E11::DP8C172602885::INSTR'
    #Load = 'USB0::0x1AB1::0x0E11::DL3A222000386::INSTR'
    #O_scope = 'USB0::0x1AB1::0x0588::DS1ET153818956::INSTR'

    instrument = connect_device(power_supply)
    if instrument:
        ps_set_voltage(instrument, voltage, channel)
        try:
            instrument.write('*IDN?')
            print("Device ID",instrument.read())
        except Exception as e:
            print("Error sending command:", e)
    else:
        print("Device not connected")

if __name__ == "__main__":
    main()

