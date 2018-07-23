class SDM3065X:
	def __init__(self, instr):
		if 'SDM3065X' not in instr.query("*IDN?"):
			raise NameError('Device is not SDM3065X')
		else:
			self.instr = instr
			self.plc_current = 10
			self.plc_volt = 10
			self.thermocouple = '';

	def set_plc_current(self, plc):
		if not (plc!=100 or plc!=10 or plc!=1 or plc!=0.5 or plc!=0.05 or plc!=0.005):
			raise NameError('PLC value is not avalaible')
		else:
			self.plc_current = plc

	def set_plc_volt(self, plc):
		if not (plc!=100 or plc!=10 or plc!=1 or plc!=0.5 or plc!=0.05 or plc!=0.005):
			raise NameError('PLC value is not avalaible')
		else:
			self.plc_volt = plc

	def voltage(self):
		self.instr.write('CONF:VOLT:DC')
		self.instr.write(f'VOLT:DC:NPLC {self.plc_volt}')
		return float(self.instr.query('READ?'))

	def current(self):
		self.instr.write('CONF:CURR:DC')
		self.instr.write(f'CURR:DC:NPLC {self.plc_current}')		
		return float(self.instr.query('READ?'))


if __name__ == '__main__':

	import visa
	rm = visa.ResourceManager()
	inst = rm.open_resource("USB0::0xF4EC::0xEE38::SDM36FAD1R0345::0::INSTR")
	inst.timeout = 20000
	sup = SDM3065X(inst)
	print(inst.query('*IDN?'))
	plc_volt=1
	plc_current=100
	sup.set_plc_current(plc_current)
	sup.set_plc_volt(plc_volt)
	inst.timeout = 10000
	print(sup.voltage())
	print(sup.current())