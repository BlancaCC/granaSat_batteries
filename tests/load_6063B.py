class Load6063B:
    def __init__(self, instr):
        if 'HEWLETT-PACKARD,6063B' not in instr.query("*IDN?"):
            raise NameError('Device is not HEWLETT-PACKARD 6063B')
        else:
            self.instr = instr
            
    def input_on(self):
        self.instr.write('INPUT ON')
    def input_off(self):
        self.instr.write('INPUT OFF')
    def mode(self, mode):
        if mode == 'cc':
            self.instr.write('MODE:CURR')
            self._mode = 'cc'
        elif mode == 'cv':
            self.instr.write('MODE:VOLT')
            self._mode = 'cv'
        elif mode == 'cr':
            self.instr.write('MODE:RES')
            self._mode = 'cr'
        else:
            raise NameError('Not a command')

    def set_current(self, curr):
        try:
            _mode = self._mode
        except AttributeError:
            _mode = 'unknown'
        if _mode is not 'cc':
            self.mode('cc')
        self.instr.write(f'CURR:LEVEL {curr}')
    
    def set_voltage(self, curr):
        try:
            _mode = self._mode
        except AttributeError:
            _mode = 'unknown'
        if _mode is not 'cv':
            self.mode('cv')
        self.instr.write(f'VOL:LEVEL {curr}')

    
    def set_resistence(self, res):
        try:
            _mode = self._mode
        except AttributeError:
            _mode = 'unknown'
        if _mode is not 'cr':
            self.mode('cr')
        self.instr.write(f'RES:{res}')
    
    def current(self) -> 'Amperes': 
        return float(self.instr.query('MEAS:CURR?'))
    
    def voltage(self) -> 'Volts':
        return float(self.instr.query('MEAS:VOLT?'))

if __name__ == '__main__':

    import visa
    rm = visa.ResourceManager()
    print(rm.list_resources())
    load_ins=rm.open_resource('GPIB0::4::INSTR')
    load= Load6063B(load_ins)
    load.set_current(0.5)
        
    
