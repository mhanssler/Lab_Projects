import nidaqmx
from nidaqmx.constants import AcquisitionType


class cDAQController:
    def __init__(self, device_name):
        self.device_name = device_name

    def read_analog_input(self, channel, samples_per_channel, sample_rate):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(f"{self.device_name}/{channel}")
            task.timing.cfg_samp_clk_timing(sample_rate, sample_quantity_mode=AcquisitionType.FINITE,
                                            samps_per_chan=samples_per_channel)

            data = task.read(number_of_samples_per_channel=samples_per_channel)
            return data
    def read_digital_input(self, channel, samples_per_channel, sample_rare):
            task.di_channels.add_di_chan(f"{self.device_name}/{channel}")
            task.timing.cfg_samp_clk_timing(sample_rate, sample_quantity_mode=AcquisitionType.FINITE,
                                            samps_per_chan=samples_per_channel)
            

# Example usage
if __name__ == "__main__":
    cdaq = cDAQController("cDAQ1Mod1")  # Replace with your device/module name
    data = cdaq.read_analog_input("ai0", 1000, 1000)  # Read from channel ai0, 1000 samples, at 1000 Hz
    digital_data = cdaq.read_digital_input("port0/line0", 1000, 1000)
    print("Analog Input Data:", data)
