import pyvisa #type ignore

class EAPSB9000Controller:
    def __init__(self, resource_name):
        self.rm = pyvisa.ResourceManager()
        self.instr = self.rm.open_resource(resource_name)
    
    # Add a IDN query to check if the instrument is connected
    def check_connection(self):
        return self.query("*IDN?")

    def close(self):
        self.instr.close()

    def send_command(self, command):
        self.instr.write(command)

    def query(self, command):
        return self.instr.query(command)

    # Add specific commands for your power supply here
    def set_voltage(self, voltage):
        command = f"VOLT {voltage}"
        self.send_command(command)

    def set_current(self, current):
        command = f"CURR {current}"
        self.send_command(command)

    def get_voltage(self):
        return self.query("MEAS:VOLT?")

    def get_current(self):
        return self.query("MEAS:CURR?")

    # More specific commands can be added here...

# Example usage
if __name__ == "__main__":
    # Replace with your instrument's address
    psu = EAPSB9000Controller('USB6::5::INSTR')
    psu.list_resources()
    psu.set_voltage(5.0)
    print("Voltage set to 5.0 V")
    print(f"Current Voltage: {psu.get_voltage()} V")
    psu.close()
