import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def calculate_statistics(file_path):
    # Read the CSV file
    try:
        df = pd.read_csv(file_path, header=None)
    except Exception as e:
        return f"Error reading the file: {e}"
    
    # Check for numeric columns
    numeric_cols = df.select_dtypes(include='number')
    
    if numeric_cols.empty:
        return "No numeric columns found in the file."

    data = df[0].to_numpy()
    mean = np.mean(data)
    trials = len(data)
    uncertainty = np.std(data)/np.sqrt(trials)



    return mean, uncertainty, trials


######################
### TGAP1 PLOTTING ###
######################
'''
#STANDARD
mean1, unc1, tr1 = calculate_statistics("standard/arch4982/2atm.csv")
mean2, unc2, tr2 = calculate_statistics("standard/arch4982/2_5atm.csv")
mean3, unc3, tr3 = calculate_statistics("standard/arch4982/3atm.csv")
mean4, unc4, tr4 = calculate_statistics("standard/arch4982/3_5atm.csv")
mean5, unc5, tr5 = calculate_statistics("standard/arch4982/4atm.csv")
mean6, unc6, tr6 = calculate_statistics("standard/arch4982/4_5atm.csv")
mean7, unc7, tr7 = calculate_statistics("standard/arch4982/5atm.csv")


#REDUCED GAP
mean8, unc8, tr8 = calculate_statistics("new_tgap/2atm.csv")
mean9, unc9, tr9 = calculate_statistics("new_tgap/2_5atm.csv")
mean10, unc10, tr10 = calculate_statistics("new_tgap/3atm.csv")
mean11, unc11, tr11 = calculate_statistics("new_tgap/3_5atm.csv")
mean12, unc12, tr12 = calculate_statistics("new_tgap/4atm.csv")
mean13, unc13, tr13 = calculate_statistics("new_tgap/4_5atm.csv")
#mean14, unc14, tr14 = calculate_statistics("new_tgap/5atm.csv")

pressure = np.array([2.0,2.5,3.0,3.5,4.0,4.5])

# GEM thickness in cm
t = 50e-4  # 50 microns = 5e-3 cm

# GEM voltages (V)
Vsum = 500 + 432.4 + 377.2


x_scaled = (Vsum / t) / pressure

gain_standard = np.array([mean1,mean2,mean3,mean4,mean5,mean6])
unc_standard = np.array([unc1, unc2, unc3, unc4, unc5,unc6])

gain_reduced = np.array([mean8,mean9,mean10,mean11,mean12,mean13])
unc_reduced = np.array([unc8,unc9,unc10,unc11,unc12,unc13])

plt.errorbar(x_scaled,gain_standard,yerr=unc_standard,label='TGAP1 = 2.1 mm')
plt.errorbar(x_scaled,gain_reduced,yerr=unc_reduced,label='TGAP1 = 0.5 mm')

plt.yscale('log')
plt.xlabel(r'$E/P\ \mathrm{[V/(atm\cdot cm)]}$')
plt.ylabel('Gain')
plt.legend()
plt.savefig('gap_test.png')
'''


######################
#### GAS PLOTTING ####
######################     
'''
#AR-CH4 98-2

mean1, unc1, tr1 = calculate_statistics("standard/arch4982/2atm.csv")
mean2, unc2, tr2 = calculate_statistics("standard/arch4982/2_5atm.csv")
mean3, unc3, tr3 = calculate_statistics("standard/arch4982/3atm.csv")
mean4, unc4, tr4 = calculate_statistics("standard/arch4982/3_5atm.csv")
mean5, unc5, tr5 = calculate_statistics("standard/arch4982/4atm.csv")
mean6, unc6, tr6 = calculate_statistics("standard/arch4982/4_5atm.csv")
mean7, unc7, tr7 = calculate_statistics("standard/arch4982/5atm.csv")


#AR-CH4 96-4

mean8, unc8, tr8 = calculate_statistics("standard/arch4964/2atm.csv")
mean9, unc9, tr9 = calculate_statistics("standard/arch4964/2_5atm.csv")
mean10, unc10, tr10 = calculate_statistics("standard/arch4964/3atm.csv")
mean11, unc11, tr11 = calculate_statistics("standard/arch4964/3_5atm.csv")
mean12, unc12, tr12 = calculate_statistics("standard/arch4964/4atm.csv")
mean13, unc13, tr13 = calculate_statistics("standard/arch4964/4_5atm.csv")
mean14, unc14, tr14 = calculate_statistics("standard/arch4964/5atm.csv")

#AR-CH4 92-8

mean15, unc15, tr15 = calculate_statistics("standard/arch4928/2atm.csv")
mean16, unc16, tr16 = calculate_statistics("standard/arch4928/2_5atm.csv")
mean17, unc17, tr17 = calculate_statistics("standard/arch4928/3atm.csv")
mean18, unc18, tr18 = calculate_statistics("standard/arch4928/3_5atm.csv")
mean19, unc19, tr19 = calculate_statistics("standard/arch4928/4atm.csv")
mean20, unc20, tr20 = calculate_statistics("standard/arch4928/4_5atm.csv")
mean21, unc21, tr21 = calculate_statistics("standard/arch4928/5atm.csv")

#AR-CO2 90-10

mean22, unc22, tr22 = calculate_statistics("standard/arco29010/2atm.csv")
mean23, unc23, tr23 = calculate_statistics("standard/arco29010/2_5atm.csv")
mean24, unc24, tr24 = calculate_statistics("standard/arco29010/3atm.csv")
mean25, unc25, tr25 = calculate_statistics("standard/arco29010/3_5atm.csv")
mean26, unc26, tr26 = calculate_statistics("standard/arco29010/4atm.csv")
mean27, unc27, tr27 = calculate_statistics("standard/arco29010/4_5atm.csv")
mean28, unc28, tr28 = calculate_statistics("standard/arco29010/5atm.csv")

# GEM thickness in cm
t = 50e-4  # 50 microns = 5e-3 cm

# GEM voltages (V)
Vsum = 500 + 432.4 + 377.2
pressure = np.array([2.0,2.5,3.0,3.5,4.0,4.5,5.0])

x_scaled = (Vsum / t) / pressure

gain_arch4982 = np.array([mean1,mean2,mean3,mean4,mean5,mean6,mean7])
unc_arch4982 = np.array([unc1, unc2, unc3, unc4, unc5,unc6,unc7])

gain_arch4964 = np.array([mean8,mean9,mean10,mean11,mean12,mean13,mean14])
unc_arch4964 = np.array([unc8,unc9,unc10,unc11,unc12,unc13,unc14])

gain_arch4928 = np.array([mean15,mean16,mean17,mean18,mean19,mean20,mean21])
unc_arch4928 = np.array([unc15,unc16,unc17,unc18,unc19,unc20,unc21])

gain_arco29010 = np.array([mean22,mean23,mean24,mean25,mean26,mean27,mean28])
unc_arco29010 = np.array([unc22,unc23,unc24,unc25,unc26,unc27,unc28])


plt.figure()

plt.errorbar(x_scaled, gain_arch4982,  yerr=unc_arch4982,  label='Ar-CH4 98-2')
plt.errorbar(x_scaled, gain_arch4964,  yerr=unc_arch4964,  label='Ar-CH4 96-4')
plt.errorbar(x_scaled, gain_arch4928,  yerr=unc_arch4928,  label='Ar-CH4 92-8')
plt.errorbar(x_scaled, gain_arco29010, yerr=unc_arco29010, label='Ar-CO2 90-10')

plt.yscale('log')
plt.xlabel(r'$E/P\ \mathrm{[V/(atm\cdot cm)]}$')
plt.ylabel('Gain')
plt.legend()

ax = plt.gca()
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((4, 4))
ax.xaxis.set_major_formatter(formatter)

plt.tight_layout()
plt.savefig('test.png', dpi=300)
plt.show()
'''

######################
#### EXT PLOTTING ####
######################  
'''
mean1, unc1, tr1 = calculate_statistics("sing_tfield/1kVcm/2atm.csv")
mean2, unc2, tr2 = calculate_statistics("sing_tfield/3kVcm/2atm.csv")
mean3, unc3, tr3 = calculate_statistics("sing_tfield/5kVcm/2atm.csv")
mean4, unc4, tr4 = calculate_statistics("sing_tfield/7kVcm/2atm.csv")
mean5, unc5, tr5 = calculate_statistics("sing_tfield/9kVcm/2atm.csv")

mean6, unc6, tr6 = calculate_statistics("sing_tfield/1kVcm/4atm.csv")
mean7, unc7, tr7 = calculate_statistics("sing_tfield/3kVcm/4atm.csv")
mean8, unc8, tr8 = calculate_statistics("sing_tfield/5kVcm/4atm.csv")
mean9, unc9, tr9 = calculate_statistics("sing_tfield/7kVcm/4atm.csv")
mean10, unc10, tr10 = calculate_statistics("sing_tfield/9kVcm/4atm.csv")

mean11, unc11, tr11 = calculate_statistics("sing_tfield/1kVcm/6atm.csv")
mean12, unc12, tr12 = calculate_statistics("sing_tfield/3kVcm/6atm.csv")
mean13, unc13, tr13 = calculate_statistics("sing_tfield/5kVcm/6atm.csv")
mean14, unc14, tr14 = calculate_statistics("sing_tfield/7kVcm/6atm.csv")
mean15, unc15, tr15 = calculate_statistics("sing_tfield/9kVcm/6atm.csv")


field = np.array([1.0,3.0,5.0,7.0,9.0])
mean_1 = np.array([mean1,mean2,mean3,mean4,mean5])
unc_1 = np.array([unc1, unc2,unc3,unc4,unc5])

mean_2 = np.array([mean6,mean7,mean8,mean9,mean10])
unc_2 = np.array([unc6, unc7,unc8,unc9,unc10])

mean_3 = np.array([mean11,mean12,mean13,mean14,mean15])
unc_3 = np.array([unc11, unc12,unc13,unc14,unc15])

plt.errorbar(field, mean_1,  yerr=unc_1, label = '2 atm')
plt.errorbar(field, mean_2,  yerr=unc_2, label = '4 atm')
plt.errorbar(field, mean_3,  yerr=unc_3, label = '6 atm')
plt.ylabel('Extraction Efficiency from GEM 1')
plt.xlabel('Transfer Field [kV/cm]')
plt.legend()
plt.ylim(0,1.0)
plt.savefig('test2.png')
'''
######################
#### COL PLOTTING ####
######################  
'''
mean1, unc1, tr1 = calculate_statistics("sing_tfield/ext_tfield/1kVcm/2atm.csv")
mean2, unc2, tr2 = calculate_statistics("sing_tfield/ext_tfield/3kVcm/2atm.csv")
mean3, unc3, tr3 = calculate_statistics("sing_tfield/ext_tfield/5kVcm/2atm.csv")
mean4, unc4, tr4 = calculate_statistics("sing_tfield/ext_tfield/7kVcm/2atm.csv")
mean5, unc5, tr5 = calculate_statistics("sing_tfield/ext_tfield/9kVcm/2atm.csv")

mean6, unc6, tr1 = calculate_statistics("sing_tfield/ext_tfield/1kVcm/4atm.csv")
mean7, unc7, tr2 = calculate_statistics("sing_tfield/ext_tfield/3kVcm/4atm.csv")
mean8, unc8, tr3 = calculate_statistics("sing_tfield/ext_tfield/5kVcm/4atm.csv")
mean9, unc9, tr4 = calculate_statistics("sing_tfield/ext_tfield/7kVcm/4atm.csv")
mean10, unc10, tr5 = calculate_statistics("sing_tfield/ext_tfield/9kVcm/4atm.csv")

mean11, unc11, tr1 = calculate_statistics("sing_tfield/ext_tfield/1kVcm/6atm.csv")
mean12, unc12, tr2 = calculate_statistics("sing_tfield/ext_tfield/3kVcm/6atm.csv")
mean13, unc13, tr3 = calculate_statistics("sing_tfield/ext_tfield/5kVcm/6atm.csv")
mean14, unc14, tr4 = calculate_statistics("sing_tfield/ext_tfield/7kVcm/6atm.csv")
mean15, unc15, tr5 = calculate_statistics("sing_tfield/ext_tfield/9kVcm/6atm.csv")

mean_1 = np.array([mean1,mean2,mean3,mean4,mean5])
unc_1 = np.array([unc1, unc2,unc3,unc4,unc5])

mean_2 = np.array([mean6,mean7,mean8,mean9,mean10])
unc_2 = np.array([unc6, unc7,unc8,unc9,unc10])

mean_3 = np.array([mean11,mean12,mean13,mean14,mean15])
unc_3 = np.array([unc11, unc12,unc13,unc14,unc15])

field = np.array([1.0,3.0,5.0,7.0,9.0])
plt.errorbar(field, mean_1,  yerr=unc_1, label = '2 atm')
plt.errorbar(field, mean_2,  yerr=unc_2, label = '4 atm')
plt.errorbar(field, mean_3,  yerr=unc_3, label = '6 atm')
plt.ylabel('Collection Efficiency into GEM 2')
plt.xlabel('Transfer Field [kV/cm]')
plt.legend()
plt.ylim(0,1.0)
plt.savefig('test3.png')
'''

######################
### THGEM PLOTTING ###
######################  

'''
mean2, unc2, tr2 = calculate_statistics("THGEM/benchmark/test.csv")

simulation = np.array([5.1, 14.124, 83.4, 2613.4, 50000])
experiment = np.array([2.2539339047347906,5.560297632845825 , 25.808615404180742, 323.44759148768213, 6660.846290809154])

voltage = np.array([1000,1200,1400,1600,1800])

plt.plot(voltage, simulation, label='Simulation')
plt.plot(voltage, experiment, label='Experiment')
plt.yscale('log')
plt.xlabel('Voltage [V]')
plt.ylabel('Gain')
plt.legend()
plt.savefig('thgem_benchmark.png')
'''
######################
### GOAT PLOTTING ###
###################### 



mean1, unc1, tr1 = calculate_statistics("alice/goat_data/1050.csv")
mean2, unc2, tr2 = calculate_statistics("alice/goat_data/1150.csv")
mean3, unc3, tr3 = calculate_statistics("alice/goat_data/1250.csv")
mean4, unc4, tr4 = calculate_statistics("alice/goat_data/1350.csv")
mean5, unc5, tr5 = calculate_statistics("alice/goat_data/1450.csv")

simulation = np.array([mean1,mean2,mean3,mean4,mean5])
print(simulation)
simulation_unc = np.array([unc1,unc2,unc3,unc4,unc5])

experiment = np.array([175.25,467.79,1308.43,3790.36,11505.70])
voltage = np.array([1050,1150,1250,1350,1450])

plt.errorbar(voltage,simulation,yerr=simulation_unc,label="Garfield++ Simulation")
plt.plot(voltage,experiment,label="GOAT Data")
plt.xlabel('Voltage [V]')
plt.ylabel('Gain')
plt.yscale('log')
plt.legend()
plt.savefig("goatcomp.png")


