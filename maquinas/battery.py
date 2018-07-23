import time
import datetime
import csv
import visa
from supply_E3631A import SupplyE3631A
from load_6063B import Load6063B
from multimeter_SDM3065X import MultimeterSDM3065X


class Battery():
	def __init__(self,charge=1000, v_max=7, v_min=3, eoc_current= 0.2):
		import visa
		rm = visa.ResourceManager()
		print(rm.list_resources())
		sup_ins=rm.open_resource('GPIB0::3::INSTR')
		load_ins=rm.open_resource('GPIB0::4::INSTR')
		multim_ins=rm.open_resource('USB0::0xF4EC::0xEE38::SDM36FAD1R0345::0::INSTR')
		multim_ins.timeout = 20000
		self._load = Load6063B(load_ins)
		self._supply = SupplyE3631A(sup_ins)
		self._charge = charge
		self._v_max = v_max
		self._v_min = v_min
		self._eoc_current = eoc_current
		multim = MultimeterSDM3065X(multim_ins)
		self._multimm = multim


	def load_measure_ocv(self, curr):
		self._load.set_current(0)
		time.sleep(0.5)
		volt = self._load.voltage()
		self._load.set_current( curr)
		return volt

	def discharge_ocv(self, curr, sample_time = 1000, ocv_per_samples = 10 ,log_file = None):
		self._load.input_off()
		self._load.set_current(curr)
		self._load.input_on()
		
		cnt = 0
		if not log_file:
			ts = time.time()
			log_file = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H-%M-%S_') + 'discharge.csv' 
		with open(log_file, 'w', newline='') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
			
			voltage = self._load.voltage()
			current = self._load.current()
			before = int(round(time.time() * 1000))
			while voltage > self._v_min:
				voltage = self._load.voltage()
				current = self._load.current()
			
				if cnt % ocv_per_samples == 0: 
					t1=int(round(time.time() * 1000))
					ocv = self.load_measure_ocv(curr)    
					t2=int(round(time.time() * 1000))

				csvwriter.writerow([voltage, current, before, ocv,self._charge])
				now = int(round(time.time() * 1000))
				while now-before < sample_time:
					now = int(round(time.time() * 1000))
				self._charge = self._charge - current*((now-before-(t2-t1))/(1000*60*60))
				print(f'Current: {current}, Voltage: {voltage},Time: {before}, Charge remainign: {self._charge}, OCV:{ocv}')
				t1 = 0
				t2 = 0
				cnt = cnt+1
				before = now
		self._load.input_off()
		

	def charge_ocv(self, curr, sample_time = 1000, ocv_per_samples = 10, output = "+6V", log_file = None):
		self._supply.output_off()
		self._supply.select_output(output)
		self._supply.limit_current( curr)
		self._supply.set_voltage( self._v_max)
		self._supply.output_on()
		cnt = 0
		voltage = self._supply.voltage()
		current = self._supply.current()
		if not log_file:
			ts = time.time()
			log_file = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H-%M-%S_') + 'charge.csv' 
		with open(log_file, 'w', newline='') as csvfile:            
			csvwriter = csv.writer(csvfile, delimiter=',',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
			before = int(round(time.time() * 1000))
			while current > self._eoc_current:
				voltage = self._supply.voltage()
				current = self._supply.current()
				
				if cnt % ocv_per_samples == 0: 
					t1=int(round(time.time() * 1000))
					ocv = self.load_measure_ocv(curr)    
					t2=int(round(time.time() * 1000))

				csvwriter.writerow([voltage, current, before,ocv,self._charge])
				now = int(round(time.time() * 1000))
				while now-before < sample_time:
					now = int(round(time.time() * 1000))
				self._charge = self._charge + current*(now-before-(t2-t1))/(1000*60*60)
				print(f'Current: {current}, Voltage: {voltage},Time: {before}, Charge: {self._charge}, OCV: {ocv}')
				before = now
				t1=0
				t2=0
		self._supply.output_off()

	def discharge(self, curr, sample_time = 5000 ,log_file = None):
		self._load.input_off()
		self._load.set_current(curr)
		self._load.input_on()
		
		voltage = self._multimm.voltage()
		current = self._multimm.current()
		self._load.set_current(curr)
		self._supply.output_off()

		before = int(round(time.time() * 1000))
		while voltage > self._v_min:
			voltage = self._multimm.voltage()
			current = self._multimm.current()
			now = int(round(time.time() * 1000))
			self._charge = self._charge + current*(now-before)
			print(f'Current: {current}, Voltage: {voltage}, Time: {now-before}, Charge: {self._charge}')
			before=now

		self._multimm.reset()
				

	def charge(self, curr, sample_time = 5300, output = "+25V", log_file = None):
		self._supply.output_off()
		self._supply.select_output(output)
		self._supply.limit_current(curr)
		self._supply.set_voltage( self._v_max)
		self._supply.output_on()
		self._load.input_off()
		voltage = self._supply.voltage()
		current = self._supply.current()
		
		now = int(round(time.time() * 1000))
		before = int(round(time.time() * 1000))
		print(f'Current: {current}, Voltage: {voltage}, Time: {now-before}, Charge: {self._charge}')
		voltage = self._supply.voltage()
		current = self._supply.current()

		while voltage < self._v_max*0.999:
			new_now = 0
			now = int(round(time.time() * 1000))
			new_now = now-before
			while new_now < sample_time:
				before = now
				voltage = self._supply.voltage()
				current = self._supply.current()
				now = int(round(time.time() * 1000))
				new_now = new_now+(now-before)

			self._charge = self._charge + current*(new_now)
			print(f'Current: {current}, Voltage: {voltage}, Time: {new_now}, Charge: {self._charge}')

		self._multimm.reset()
					 
	

	def set_charge(self,val):
		self._charge = val   

	def jkl(self):
		print('lsf')

if __name__ == '__main__': 
	
	bat_name="FT103450P_1_Cd50"
	bat = Battery(charge=1000, v_max = 7, v_min = 3, eoc_current=1.8*0.02)
	bat.charge(0.7)
	print(bat.voltage())
