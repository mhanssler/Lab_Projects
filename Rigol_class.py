import pyvisa

class RigolPowerSupply:
    def __init__(self, address):
        self.rm = pyvisa.ResourceManager
        self.instrument = self.rm.open_resource(address)

