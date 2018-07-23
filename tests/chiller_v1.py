"""
Problems:
- Para leer temperaturas y demás te incluye las unidades usadas para representarlas, por lo que hay que separarlo de alguna forma
- read_data() y cambiar todas las lecturas que se hacen para devolver el float
- No se si hay que hacer un "casting" a string cuando te devuelve una cadena de caracteres
- Cuando le pasas un valor a una funcion y lo metes en un string da igual si es int o un caracter??
- Hay que hacer un flush despues de cada lectura para limpiar??
"""

class Chiller: #cambiar nombre
	def __init__(self, ser):
		self.ser = ser

	# Data reading
	def read_data(self):
		data = self.ser.read(size=1)
		while data[-1] != ('\r' or '\n'):
			data += self.ser.read(size=1)
		self.ser.flush()
		return data[0:-1]


	# Read Temperature (Internal)
	def read_temperature_int(self):
		self.ser.write('RT')
		return float(read_data())

	# Read Temperature (External)
	def read_temperature_ext(self):
		self.ser.write('RT2')
		return float(read_data())
		
	# Read Dsiplayed Setpoint
	def read_disp_setpoint(self):
		self.ser.write('RS')		
		return float(read_data())

	# Read Internal RTA1-5	
	def read_int_rta(self,number):
		self.ser.write(f'RIRTA{number}')		
		return float(read_data())

	# Read External RTA1-5
	def read_ext_rta(self,number):
		self.ser.write(f'RERTA{number}')		
		return float(read_data())

	# Read Setpoint 1-5
	def read_setpoint(self,number):
		self.ser.write(f'RS{number}')		
		return float(read_data())

	# Read High Temperature Fault
	def read_high_temp_fault(self):
		self.ser.write('RHTF')		
		return float(read_data())

	# Read High Temperature Warn
	def read_high_temp_warn(self):
		self.ser.write('RHTW')		
		return float(read_data())

	# Read Low Temperature Fault
	def read_low_temp_fault(self):
		self.ser.write('RLTF')		
		return float(read_data())

	# Read Low Temperature Warn
	def read_low_temp_warn(self):
		self.ser.write('RLTW')		
		return float(read_data())

	# Read Proportional Heat Band Setting
	def read_prop_heat_band(self):
		self.ser.write('RPH')		
		return float(read_data())

	# Read Proportional Cool Band Setting
	def read_prop_cool_band(self):
		self.ser.write('RPC')		
		return float(read_data())

	# Read Integral Heat Band Setting
	def read_integral_heat_band(self):
		self.ser.write('RIH')		
		return float(read_data())

	# Read Integral Cool Band Setting
	def read_integral_cool_band(self):
		self.ser.write('RIC')		
		return float(read_data())

	# Read Derivate Heat Band Setting
	def read_deriv_heat_band(self):
		self.ser.write('RDH')		
		return float(read_data())

	# Read Derivate Cool Band Setting
	def read_deriv_cool_band(self):
		self.ser.write('RDC')		
		return float(read_data())

	# Read Temperature Precision
	def read_temp_precision(self):
		self.ser.write('RTP')		
		return float(read_data())

	# Read Temperature Units
	def read_temp_units(self):
		self.ser.write('RTU')		
		return str(read_data())

	# Read Unit On
	def read_unit_on(self):
		self.ser.write('RO')
		if (int(self.ser.read(size=8)) == 0):
			return False
		elif (int(self.ser.read(size=8))) == 1:
			return True

	# Read External Probe Enabled
	def read_ext_probe_en(self):
		self.ser.write('RE')
		if int(self.ser.read(size=8)) == 0:
			return False
		elif int(self.ser.read(size=8)) == 1:
			return True

	# Read Auto Restart Enabled
	def read_deriv_heat_band(self):
		self.ser.write('RAR')
		if int(self.ser.read(size=8)) == 0:
			return False
		elif int(self.ser.read(size=8)) == 1:
			return True

	# Read Time
	def read_time(self):
		self.ser.write('RCK')		
		return str(read_data())

	# Read Date
	def read_date(self):
		self.ser.write('RDT')		
		return str(read_data())

	# Read Date Format
	def read_date_format(self):
		self.ser.write('RDF')		
		return str(read_data())

	# Read Ramp Status
	def read_ramp_status(self):
		self.ser.write('RRS')		
		return str(read_data())

	# Read Firmware Version
	def read_firmware_ver(self):
		self.ser.write('RVER')		
		return float(read_data()) 

	# Read Firmware Checksum
	def read_firmware_checksum(self):
		self.ser.write('RSUM')		
		return float(read_data()) #no se si es float o una cadena

	# Read Unit Fault Status
	def read_unit_fault_sta(self):
		return 0
		#hay que poner todas las posibilidades?

	# Set Displayed Setpoint
	def set_disp_setpoint(self, value):
		self.ser.write(f'SS {value}')		
		return str(read_data())

	# Set Internal RTA1-5
	def set_int_rta(self, value, number):
		self.ser.write(f'SIRTA{number} {value}')		
		return str(read_data())

	# Set External RTA1-5
	def set_ext_rta(self, value, number):
		self.ser.write(f'SERTA{number} {value}')		
		return str(read_data())

	# Set Setpoint 1-5
	def set_setpoint(self, value, number):
		self.ser.write(f'SS{number} {value}')		
		return str(read_data())

	# Set High Temperature Fault
	def set_high_temp_fault(self, value):
		self.ser.write(f'SHTF {value}')		
		return str(read_data())

	# Set High Temperature Warning
	def set_high_temp_warning(self, value):
		self.ser.write(f'SHTW {value}')
		return str(read_data())

	# Set Low Temperature Fault
	def set_low_temp_fault(self, value):
		self.ser.write(f'SLTF {value}')		
		return str(read_data())

	# Set Low Temperature Warning
	def set_low_temp_warning(self, value):
		self.ser.write(f'SLTW {value}')		
		return str(read_data())

	# Set Proportional Heat Band Setting
	def set_prop_heat_band(self, value):
		self.ser.write(f'SPH {value}')		
		return str(read_data())

	# Set Proportional Cool Band Setting
	def set_prop_cool_band(self, value):
		self.ser.write(f'SPC {value}')		
		return str(read_data())
		
	# Set Integral Heat Band Setting
	def set_integral_heat_band(self, value):
		self.ser.write(f'SIH {value}')		
		return str(read_data())

	# Set Integral Cool Band Setting
	def set_integral_cool_band(self, value):
		self.ser.write(f'SIC {value}')		
		return str(read_data())

	# Set Derivative Heat Band Setting
	def set_deriv_heat_band(self, value):
		self.ser.write(f'SDH {value}')		
		return str(read_data())

	# Set Derivative Cool Band Setting
	def set_deriv_cool_band(self, value):
		self.ser.write(f'SDC {value}')		
		return str(read_data())

	# Set Temperature Resolution
	def set_temp_resolution(self, value):
		self.ser.write(f'STR {value}')
		
		return str(read_data())

	# Set Temperature Units
	def set_temp_units(self, value):
		self.ser.write(f'STU {value}')		
		return str(read_data())

	# Set Unit On Status
	def set_unit_onstatus(self, value):
		self.ser.write(f'SO {value}')		
		return str(read_data())

	# Set External Probe On Status
	def set_ext_probe_onstatus(self, value):
		self.ser.write(f'SE {value}')
		return str(read_data())

	# Set Auto Restart Enabled
	def set_temp_units(self, value):
		self.ser.write(f'SAR {value}')		
		return str(read_data())

	# Set Energy Saving Mode
	def set_energy_saving(self, value):
		self.ser.write(f'SEN {value}')		
		return str(read_data())

	# Set Pump Speed 
	def set_pump_speed(self, value):
		self.ser.write(f'SPS {value}')		
		return str(read_data())

	# Set Ramp Number
	def set_ramp_number(self, value):
		self.ser.write(f'SRN {value}')		
		return str(read_data())


if __name__ == "__main__":
	import serial
	ser = serial.Serial(
			port='COM3',
			baudrate=9600,
			parity=serial.PARITY_ODD,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.SEVENBITS
			)
	#No se si hay que abrir el puerto o no con open()