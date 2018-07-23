class SDM3065X:
	def __init__(self, instr):
		if 'SDM3065X' not in instr.query("*IDN?"):
			raise NameError('Device is not SDM3065X')
		else:
			self.instr = instr
			self.plc_current = 10
			self.plc_volt = 10
			self.th_type = 'BITS90'
			self.sensor_type = 'THER'

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

	def set_sensor_type(self, sensor_type):
		"""
		Sets the sensor type used for measuring the temperature. If the sensor name is incorrect, it will show an error message.
		@param sensor_type String that defines the type of sensor used in the multimeter syntax.
		"""
		if not (sensor_type != 'RTD' or sensor_type != 'THER'):
			raise NameError('Sensor type name not available.')
		else:
			self.sensor_type = sensor_type			

	def set_thermo_type(self, thermo_type, sensor_type):
		"""
		Sets the thermocouple type for the measurement. In case a thermoresistor is used for measuring the temperature, the unique option is PT100.
		@param thermo_type Provides the name for the thermoresistor or thermocouple used.
		@param sensor_type The name of the sensor used.
		"""
		if sensor_type == 'THER':
			if not (thermo_type!='BITS90' or thermo_type!='EITS90' or thermo_type!='JITS90' or thermo_type!='KITS90' or
			  		thermo_type!='NITS90' or thermo_type!='RITS90' or thermo_type!='SITS90' or thermo_type!='TITS90'):
				raise NameError('PLC value is not avalaible.')
			else:
				self.th_type = thermo_type
		else:
			self.th_type = 'PT100'


	def temperature(self):
		"""
		Gets the temperature configuration and measurements from the multimeter.
		@param self The pointer for the SDM3065X object.
		@return The temperature configuration and a set of temperature measurements. 
		"""
		return float(self.instr.query(f'MEAS:TEMP? {self.sensor_type},{self.th_type}')) 



if __name__ == '__main__':

	import visa
	rm = visa.ResourceManager()
	inst = rm.open_resource("USB0::0xF4EC::0xEE38::SDM36FAD1R0345::0::INSTR")
	inst.timeout = 20000
	sup = SDM3065X(inst)
	#print(inst.query('*IDN?'))
	
	plc_volt=0.5
	plc_current=0.5	
	thermocouple_type = 'JITS90'
	sensor_type = 'THER'

	sup.set_plc_current(plc_current)
	sup.set_plc_volt(plc_volt)
	sup.set_sensor_type(sensor_type)
	sup.set_thermo_type(thermocouple_type,sensor_type)

	inst.timeout = 10000
	
	print(sup.voltage())
	print(sup.current())
	print(sup.temperature())