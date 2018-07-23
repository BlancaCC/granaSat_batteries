import serial
import visa
import time
from supply_E3631A import SupplyE3631A
from load_6063B import Load6063B
from multimeter_SDM3065X import MultimeterSDM3065X
from batter_v2_pruebaschiller import Battery
from control_temperatura_v1 import temp_control
from chiller_v1 import CHILLER
import serial


def close_devices(load, sup):
    load.input_off()
    supl.output_off()
    print("Quitting---")

rm = visa.ResourceManager()
sup_ins=rm.open_resource('GPIB0::3::INSTR')
load_ins=rm.open_resource('GPIB0::4::INSTR')
multimeter_ins=rm.open_resource('USB0::0xF4EC::0xEE38::SDM36FAD1R0345::0::INSTR')
load = Load6063B(load_ins)
supl = SupplyE3631A(sup_ins)
multimm = MultimeterSDM3065X(multimeter_ins)
ser = serial.Serial(
			port='COM3',
			baudrate=9600,
			parity=serial.PARITY_ODD,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.SEVENBITS
			)
print(rm.list_resources())

C=1.8
bat_name="FT103450P_1_Cd50"
bat = Battery(charge=0, v_max = 7, v_min = 3, eoc_current=1.8*0.02)
cont = temp_control(ser, inst)
bat.set_charge(0)

bat.charge(C/10,True,0)
bat.discharge(C/10,True,-20)

bat.charge(C/10,True,0)
bat.discharge(C/10,True,-10)

bat.charge(C/10,True,0)
bat.discharge(C/10,True,0)

bat.charge(C/10,True,10)
bat.discharge(C/10,True,10)

bat.charge(C/10,True,20)
bat.discharge(C/10,True,20)

bat.charge(C/10,True,30)
bat.discharge(C/10,True,30)

bat.charge(C/10,True,40)
bat.discharge(C/10,True,40)

print("Quitting---")
