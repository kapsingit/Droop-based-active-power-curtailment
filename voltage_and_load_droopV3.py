## Code generated : 4:32 PM, 6/19/2018
## By: Kapil Duwadi, kapil.duwadi@jacks.sdstate.edu


from buspy.bus import open_bus
from buspy.comm.message import CommonParam
from buspy.comm.message import MessageCommonData
import numpy as np

import pandas as pd


START_TIME = pd.to_datetime('2014-06-22 00:00:00') 
END_TIME = pd.to_datetime('2014-06-22 23:59:00') 


df = pd.read_pickle("datasaved.pkl")

DATA_FRAME=[]
LOAD_current_time=[]

DATA_FRAME.append(df['PV_Power'])

for i in range(1,13):
    DATA_FRAME.append(df['load_%d'% i])

current_time = START_TIME



HOUSE_FILE = 'agg_zips.txt'
BUS_FILE_ITER = 'bus_in_iter.json'
BUS_FILE_MAIN = 'bus_in_main.json'

global Final_power
global voltage
global node
global I
global sensitivity
global PMPPT
global Pcurtail
global m
global V_cri
global A
global Pc
global Del_Pc
global B_inv
global q
global Pnet
global voltage_prev
global flag

Pnet = []

for i in range(0,12):
    Pnet.append(DATA_FRAME[0][:]-DATA_FRAME[i+1][:])


Final_power=[]
voltage=np.full((12, 1), 240.0)
node=["PV_N6A_DH1","PV_N6A_DH2","PV_N6A_DH3","PV_N6A_DH4","PV_N6A_DH5","PV_N6A_DH6","PV_N6A_DH7","PV_N6A_DH8","PV_N6A_DH9","PV_N6A_DH10","PV_N6A_DH11","PV_N6A_DH12"]
I=np.identity(12)
sensitivity=np.matrix([ [0.0509, 0.0509, 0.0486,0.0486, 0.0468,0.0468, 0.0455,0.0455, 0.0447,0.0447, 0.0442, 0.0442],
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
Pcurtail=np.full((12, 1), 0.0)
m = 1093.8
q = 0.5
V_cri=np.full((12, 1), 250)
A=np.full((12, 1), 0.0)
Pc=0
Del_Pc=0
sens = sensitivity/1000
B=m*(sens)+I
B_inv=np.linalg.inv(B)


HOUSES = []
with open(HOUSE_FILE) as f:
    while(True):
        line = f.readline()
        if line:
            HOUSES.append(line.rstrip('\n'))
        else:
            break

def change_power(mat_del_pc, i):

    if abs(voltage[i,0])>250:
        Del_Pc = mat_del_pc
        Pc = round(Pcurtail[i,0]+Del_Pc,4)
        Pinv = round(PMPPT+Pc,4)
    else:
        Pinv=PMPPT
        Pc=0
                
    if Pinv>0:
        Pinv=0
   
    if Pinv<PMPPT:
        Pinv=PMPPT
        Pc=0
        
    Pcurtail[i,0]=Pc
    return Pinv

def get_message_final(LOAD):

    global Final_power

    transfer = MessageCommonData()
    
    for i,n in enumerate(HOUSES):
        transfer.add_param(CommonParam(name=n,param='constant_power_A',value=(Final_power[i]+LOAD[i])))
        
    return transfer

    
def get_message(LOAD,time):
    
    global B_inv
    global A
    global Final_power
    global flag
    
    transfer = MessageCommonData()
    for k in range(0,12):
        if voltage[k,0]>250:
            if voltage[k,0]>(240*1.05) and flag[k] == 0:
                flag[k] = 1
            A[k,0]=m*voltage[k,0]-m*V_cri[k,0]-Pcurtail[k,0]+ flag[k]*q*(Pnet[k][time])
        else:
            A[k,0]=0
   
    X=B_inv*A
    X=X/5
    Final_power=[]
    for i,n in enumerate(HOUSES):
        inverter_power=change_power(X[i,0],i)
        Final_power.append(inverter_power)
        transfer.add_param(CommonParam(name=n,param='constant_power_A',value=(inverter_power+LOAD[i])))          
    return transfer
Display=0

ermax_list12 = []
ermax_list11 = []
ermax_list10 = []
ermax_list9 = []
ermax_list8 = []
ermax_list7 = []

voltage_prev_12 = 240
voltage_prev_11 = 240
voltage_prev_10 = 240
voltage_prev_9 = 240
voltage_prev_8 = 240
voltage_prev_7 = 240

with open_bus(BUS_FILE_MAIN) as bus_MAIN:
    with open_bus(BUS_FILE_ITER) as bus_ITER:
        while not bus_MAIN.finished:
            
            Display=Display+1
            
            print Display
            
            PMPPT=(0- DATA_FRAME[0][current_time])
            
            LOAD_current_time=[]
            
            for i in range(1,13):
                LOAD_current_time.append(( DATA_FRAME[i][current_time]))
            er12 =[]
            er11 = []
            er10 = []
            er9 = []
            er8 = []
            er7 = []
            ermax = []
            flag=np.full((12, 1), 0)
            
            if PMPPT<-2000.0:                
                for ite_loop in range(0,35):
                    
                    result = bus_ITER.transaction(inputs=get_message(LOAD_current_time, current_time))
                    for z,n in enumerate(node):
                        voltage[z,0]=round(abs(result.get_param(n,"measured_voltage_A").value),3)
                        if z == 11:
                            er12.append(voltage[z,0]-voltage_prev_12)
                            voltage_prev_12 = voltage[z,0]
                        if z == 10:
                            er11.append(voltage[z,0]-voltage_prev_11)
                            voltage_prev_11 = voltage[z,0]
                        if z == 9:
                            er10.append(voltage[z,0]-voltage_prev_10)
                            voltage_prev_10 = voltage[z,0]
                        if z == 8:
                            er9.append(voltage[z,0]-voltage_prev_9)
                            voltage_prev_9 = voltage[z,0]
                        if z == 7:
                            er8.append(voltage[z,0]-voltage_prev_8)
                            voltage_prev_8 = voltage[z,0]
                        if z == 6:
                            er7.append(voltage[z,0]-voltage_prev_7)
                            voltage_prev_7 = voltage[z,0]
                        
                ermax_list12.append(er12)
                ermax_list11.append(er11)
                ermax_list10.append(er10)
                ermax_list9.append(er9)
                ermax_list8.append(er8)
                ermax_list7.append(er7)
                
                result = bus_MAIN.transaction(inputs=get_message_final(LOAD_current_time))

                for z,n in enumerate(node):
                    voltage[z,0]=round(abs(result.get_param(n,"measured_voltage_A").value),3)                  

            if PMPPT>=-2000.0:
                Final_power=[]
                for i in range(0,12):
                    Final_power.append(PMPPT)                                
                result = bus_MAIN.transaction(inputs=get_message_final(LOAD_current_time))
                for z,n in enumerate(node):
                    voltage[z,0]=round(abs(result.get_param(n,"measured_voltage_A").value),3)

            current_time += pd.to_timedelta('%s s' % (60.0))

             
ermax_list12 = pd.DataFrame(ermax_list12)
ermax_list11 = pd.DataFrame(ermax_list11)
ermax_list10 = pd.DataFrame(ermax_list10)
ermax_list9 = pd.DataFrame(ermax_list9)
ermax_list8 = pd.DataFrame(ermax_list8)
ermax_list7 = pd.DataFrame(ermax_list7)

ermax_list12.to_csv('Error_list12.csv')
ermax_list11.to_csv('Error_list11.csv')
ermax_list10.to_csv('Error_list10.csv')
ermax_list9.to_csv('Error_list9.csv')
ermax_list8.to_csv('Error_list8.csv')
ermax_list7.to_csv('Error_list7.csv')

                
print 'bus finished'


