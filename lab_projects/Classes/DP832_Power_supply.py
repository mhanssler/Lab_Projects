"""docstring: Class to control Rigol DP832 programmable power supply using SCPI commands.
Assume the interface is USB and the instrument is connected to the computer.
Date: 09.27.24"""
import logging
import pyvisa

import logging
import pyvisa

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("dp832.log"),  # Logs will be saved in this file
        logging.StreamHandler()            # Logs will also be displayed on the console
    ]
)

class DP832:
    """Class to control Rigol DP832 programmable power supply using SCPI commands with pyvisa."""

    def __init__(self, resource_address):
        """
        Initialize the DP832 with a VISA resource address.
        The resource address specifies the connection string (e.g., 'USB0::0x1AB1::0x0E11::DP8C12345678::INSTR').
        """
        self.resource_address = resource_address
        self.rm = pyvisa.ResourceManager()  # Initialize VISA resource manager
        try:
            self.connection = self.rm.open_resource(self.resource_address)
            logging.info(f"Connected to {self.resource_address}")
        except Exception as e:
            logging.error(f"Failed to connect to {self.resource_address} - {e}")
            self.connection = None

    def scpi_command(func):
        """Decorator to send a SCPI command to the power supply."""
        def wrapper(self, *args, **kwargs):
            if self.connection is None:
                logging.error("No active connection to the device.")
                return
            try:
                command = func(self, *args, **kwargs)
                self.connection.write(command)
                logging.info(f"Executed command: {command}")
            except Exception as e:
                logging.error(f"Error executing command: {command} - {e}")
        return wrapper

    def scpi_query(func):
        """Decorator to send a SCPI query command and return the response."""
        def wrapper(self, *args, **kwargs):
            if self.connection is None:
                logging.error("No active connection to the device.")
                return None
            try:
                command = func(self, *args, **kwargs)
                response = self.connection.query(command)
                logging.info(f"Executed query: {command} - Response: {response}")
                return response
            except Exception as e:
                logging.error(f"Error executing query: {command} - {e}")
                return None
        return wrapper

    @scpi_command
    def set_output(self, channel, state):
        """Set the output state of the specified channel (ON/OFF)."""
        logging.info(f"Channel {channel} output set to {state}")
        return f":OUTPut{channel}:STATe {state}"

    @scpi_query
    def get_output_state(self, channel):
        """Query the output state of the specified channel."""
        return f":OUTPut{channel}:STATe?"

    @scpi_command
    def set_voltage(self, channel, voltage):
        """Set the output voltage of the specified channel."""
        logging.info(f"Channel {channel} voltage set to {voltage}V")
        return f":SOURce{channel}:VOLTage {voltage}"

    @scpi_query
    def get_voltage(self, channel):
        """Query the output voltage of the specified channel."""
        return f":SOURce{channel}:VOLTage?"

    @scpi_command
    def set_current(self, channel, current):
        """Set the output current of the specified channel."""
        logging.info(f"Channel {channel} current set to {current}A")
        return f":SOURce{channel}:CURRent {current}"

    @scpi_query
    def get_current(self, channel):
        """Query the output current of the specified channel."""
        return f":SOURce{channel}:CURRent?"

    @scpi_command
    def set_overvoltage_protection(self, channel, voltage):
        """Set the overvoltage protection limit for the specified channel."""
        logging.info(f"Channel {channel} overvoltage protection set to {voltage}V")
        return f":SOURce{channel}:VOLTage:PROTection {voltage}"

    @scpi_command
    def set_overcurrent_protection(self, channel, current):
        """Set the overcurrent protection limit for the specified channel."""
        logging.info(f"Channel {channel} overcurrent protection set to {current}A")
        return f":SOURce{channel}:CURRent:PROTection {current}"

    @scpi_command
    def enable_overvoltage_protection(self, channel, state):
        """Enable or disable overvoltage protection for the specified channel."""
        logging.info(f"Channel {channel} overvoltage protection {'enabled' if state == 'ON' else 'disabled'}")
        return f":SOURce{channel}:VOLTage:PROTection:STATe {state}"

    @scpi_command
    def enable_overcurrent_protection(self, channel, state):
        """Enable or disable overcurrent protection for the specified channel."""
        logging.info(f"Channel {channel} overcurrent protection {'enabled' if state == 'ON' else 'disabled'}")
        return f":SOURce{channel}:CURRent:PROTection:STATe {state}"

    @scpi_query
    def get_identification(self):
        """Query the identification information of the power supply."""
        return "*IDN?"

    @scpi_command
    def reset(self):
        """Reset the power supply to its default settings."""
        logging.info("Power supply reset to default settings.")
        return "*RST"

    @scpi_command
    def clear_status(self):
        """Clear the status of the power supply."""
        logging.info("Power supply status cleared.")
        return "*CLS"

    @scpi_query
    def measure_voltage(self, channel):
        """Measure the voltage on the specified channel."""
        return f":MEASure:VOLTage? CH{channel}"

    @scpi_query
    def measure_current(self, channel):
        """Measure the current on the specified channel."""
        return f":MEASure:CURRent? CH{channel}"

    @scpi_query
    def measure_power(self, channel):
        """Measure the power on the specified channel."""
        return f":MEASure:POWEr? CH{channel}"

    @scpi_command
    def set_display_brightness(self, brightness):
        """Set the brightness of the display."""
        logging.info(f"Display brightness set to {brightness}.")
        return f":SYSTem:BRIGhtness {brightness}"

    @scpi_command
    def lock_keyboard(self, state):
        """Lock or unlock the keyboard."""
        logging.info(f"Keyboard {'locked' if state == 'ON' else 'unlocked'}.")
        return f":SYSTem:KLOCk {state}"

    def close(self):
        """Close the connection to the power supply."""
        if self.connection:
            self.connection.close()
            logging.info(f"Disconnected from {self.resource_address}")
