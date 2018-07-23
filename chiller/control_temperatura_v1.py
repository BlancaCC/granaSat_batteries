import multimeter_SDM3065X_v2
import chiller_v1
import battery

class temp_control:
	def __init__(self, chiller, multi):
		self.chiller = chiller
		self.multi = multi

	def balance_temp(self, temp):
		"""
		Function to get the temperature 'temp' in the chiller, obtained by changing the pump speed at the chiller.
		@param temp Temperatura que queremos obtener en el chiller. 
		"""

		finished = True

		import time
		while (finished):
			if (self.multi.temperature > temp):
					self.chiller.set_pump_speed(set_temp,L) #parece que no hay una opcion de apagar solo de dejar la velocidad de pump en baja
					finished = battery.get_finished()

			elif (self.multi.temperature < temp):
					self.chiller.set_pump_speed(set_temp,H)
					finished = battery.get_finished()
			time.sleep(1)
				


if __name__ == '__main__':
	
	import visa
	import serial

	ser = serial.Serial(
			port='COM3',
			baudrate=9600,
			parity=serial.PARITY_ODD,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.SEVENBITS
			)

	rm = visa.ResourceManager()
	inst = rm.open_resource("USB0::0xF4EC::0xEE38::SDM36FAD1R0345::0::INSTR")
	inst.timeout = 20000

	cont = temp_control(ser, inst)

	temperature = 30

	cont.balance_temp(temperature)