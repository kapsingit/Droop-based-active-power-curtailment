## Code generated : 8:42 PM, 6/17/2018
## By: Kapil Duwadi, kapil.duwadi@jacks.sdstate.edu

from buspy.bus import open_bus
from buspy.comm.message import CommonParam
from buspy.comm.message import MessageCommonData
import pandas as pd
import numpy as np

START_TIME = pd.to_datetime('2014-06-22 00:00:00')
END_TIME = pd.to_datetime('2014-06-22 23:59:00')

df = pd.read_pickle("datasaved.pkl")

current_time = START_TIME

#df = pd.read_csv('PV_Load.csv',index_col = 'index', parse_dates = True)

# Reads the load and input data stored in datasaved pickle file same as above but fast

# To save data in pickle format, df.to_pickle("datasaved.pkl"), df is the name of dataframe



input_data = []

input_data.append(df['PV_Power'])

for i in range(1,13):
    input_data.append(df['load_%d'%i])

HOUSE_FILE = 'agg_zips.txt'
BUS_FILE_ITER = 'bus_in_iter.json'
BUS_FILE_MAIN = 'bus_in_main.json'


global Final_Power
global voltage
global node
global I
global sensitivity
global House_name
global vcri
global PV_capacity
global Pcurtail
global m
global V_cri
global A
global Pc
global Del_pc
global multiply_factor
global B_inv
global del_PC_list
global Pc_list
global Pinv_list
global voltage11_12_list


Final_power = []
voltage = np.full((12,1),240.0)
node = node=["PV_N6A_DH1","PV_N6A_DH2","PV_N6A_DH3","PV_N6A_DH4","PV_N6A_DH5","PV_N6A_DH6","PV_N6A_DH7","PV_N6A_DH8","PV_N6A_DH9","PV_N6A_DH10","PV_N6A_DH11","PV_N6A_DH12"]
I = np.identity(12)
sensitivity = np.matrix([ [0.0509, 0.0509, 0.0486,0.0486, 0.0468,0.0468, 0.0455,0.0455, 0.0447,0.0447, 0.0442, 0.0442],
                        [0.0509, 0.0509, 0.0486,0.0486, 0.0468,0.0468, 0.0455,0.0455, 0.0447,0.0447, 0.0442, 0.0442],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1025,0.1025, 0.1002,0.1002, 0.0988,0.0988, 0.0981, 0.0981],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1025,0.1025, 0.1002,0.1002, 0.0988,0.0988, 0.0981, 0.0981],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.1564,0.1564, 0.1543,0.1543, 0.1532, 0.1532],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.1564,0.1564, 0.1543,0.1543, 0.1532, 0.1532],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.2136,0.2136, 0.2109,0.2109, 0.2095, 0.2095],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.2136,0.2136, 0.2109,0.2109, 0.2095, 0.2095],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.2136,0.2136, 0.2682,0.2682, 0.2066, 0.2066],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.2136,0.2136, 0.2682,0.2682, 0.2066, 0.2066],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.2136, 0.2136,0.2682,0.2682, 0.3241, 0.3241],
                        [0.0510, 0.0510, 0.1055,0.1055, 0.1595,0.1595, 0.2136, 0.2136,0.2682,0.2682, 0.3241, 0.3241]])

House_name=["H1","H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12"]
vcri = 1.042;
PV_capacity = round(-75000/12.0, 4)
Pcurtail = np.full((12,1),0.0)
m = 8400/((1.058-vcri)*240);
V_cri = np.full((12,1), 240*vcri)
A  = np.full((12,1),0.0)
Pc = 0
Del_Pc = 0
B = m*sensitivity/1000 + I
B_inv = np.linalg.inv(B)
Del_Pc_list = []
Pc_list = []
Pinv_list = []
voltage11_12_list = []


HOUSES = []
with open(HOUSE_FILE) as f:
    while(True):
        line = f.readline()
        if line:
            HOUSES.append(line.rstrip('\n'))
        else:
            break


def change_power(mat_del_pc,i):

     if abs(voltage[i,0]) > vcri:
                   Del_Pc = mat_del_pc
                   Pc = round(Pcurtail[i,0]+Del_Pc, 4)
                   Pinv = round(PV_capacity+Pc,4)
     else:
                   Pinv = PV_capacity
                   Pc = 0
     if Pinv>0:
         Pinv = 0

     if Pinv<PV_capacity:
         Pinv = PV_capacity
         Pc = 0
     Pcurtail[i,0] = Pc

     return Pinv

def get_message_final(Load):
    
    transfer = MessageCommonData()

    for i,h in enumerate(HOUSES):
        transfer.add_param(CommonParam(name = h, param = 'constant_power_A', value = (Final_power[i]+Load[i])))
    return transfer

def get_message(Load):

    transfer = MessageCommonData()

    for k in range(0,12):
        if voltage[k,0]>vcri:
            A[k,0] = m*voltage[k,0] - m*V_cri[k,0] - Pcurtail[k,0]
        else:
            A[k,0] = 0

    X = B_inv*A

    X = X/5

    Final_power = []

    for id, h in enumerate(HOUSES):

        inverter_power = change_power(X[id,0],id)

        Final_power.append(inverter_power)

        transfer.add_param(CommonParam(name = n,param = 'constant_power_A',value = (inverter_power+Load[id])))
        

    return transfer

display = 0

with open_bus(BUS_FILE_MAIN) as bus_MAIN:
    with open_bus(BUS_FILE_ITER) as bus_ITER:
        while not bus_MAIN.finished:


            display = display + 1
            print(display)

            PMPPT = (0 - input_data[0][current_time])

            current_time_load_data = []

            for i in range(1,13):
                current_time_load_data.append(input_data[i][current_time])

            current_time += pd.to_timedelta('%s s' % (60.0))


            if PMPPT < -2000.00:
                for loop in range(0,20):
                    result = bus_ITER.transaction(inputs=get_message(current_time_load_data))
        
                    for z, n in enumerate(node):

                        voltage[z,0] = round(abs(result.get_param(n,"measured_voltage_A").value),3)

                result = bus_MAIN.transaction(inputs=get_message_final(current_time_load_data))

                for z, n in enumerate(node):

                        voltage[z,0] = round(abs(result.get_param(n,"measured_voltage_A").value),3)
                        
            if PMPPT >= -2000.0:

                Final_power = []

                for i in range(0,12):
                    Final_power.append(PMPPT)

                result = bus_MAIN.transaction(inputs=get_message_final(current_time_load_data))


                for z, n in enumerate(node):

                        voltage[z,0] = round(abs(result.get_param(n,"measured_voltage_A").value),3)

print "Program has ended"

        
    



         
                
                       
