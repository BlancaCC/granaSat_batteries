class SupplyE3631A:
    def __init__(self, instr):
        if 'HEWLETT-PACKARD,E3631A' not in instr.query("*IDN?"):
           raise NameError('Device is not HEWLETT-PACKARD E3631A')
        else:
            self.instr = instr
            
    def output_on(self):
        self.instr.write('OUTP ON')

    def output_off(self):
        self.instr.write('OUTP OFF')

    def select_output(self, gpib):
        if gpib == '+6V':
            self.instr.write('INST P6V')
        elif gpib == '+25V':
            self.instr.write('INST P25V')
        elif gpib == '-25V':
            self.instr.write('INST N25V')
        else:
            raise NameError('Not an argument')

    def limit_current(self, curr):
        self.instr.write(f'CURR {curr}')

    def set_voltage(self, volt):
        self.instr.write(f'VOLT {volt}')

    def current(self) -> 'Amperes': 
        return float(self.instr.query('MEAS:CURR?'))    

    def voltage(self) -> 'Volts':
        return float(self.instr.query('MEAS:VOLT?'))

    def write_screen(self, txt):
        self.instr.write(f'DISP:TEXT "{txt}"')
    

if __name__ == '__main__':
	
    import visa
    rm = visa.ResourceManager()
    instr = rm.open_resource('GPIB0::3::INSTR')
    sup = SupplyE3631A(instr)
    sup.output_off()
    sup.limit_current(2.2)
    sup.set_voltage(5.4)
    sup.output_on()
    while True:
        print(f'Voltage: {sup.voltage()}, Current: {sup.current()}')
