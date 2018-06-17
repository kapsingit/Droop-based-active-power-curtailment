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
global voltage_initial
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
voltage_initial = np.full((12,1),240.0)
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
m = 8.4/((1.058-vcri)*240);
V_cri = np.full((12,1), 240*vcri)
A  = np.full((12,1),0.0)
Pc = 0
Del_Pc = 0
B = m*sensitivity + I
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


f = open(HOUSE_FILE)
mylist = []
for line in f:
    if line:
        mylist.append(line.rstrip('\n')
    else:
        break

print(mylist)

