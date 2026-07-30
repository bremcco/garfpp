import ROOT
import Garfield
import math
import ctypes
import os
import csv

pressure = 3
gas = ROOT.Garfield.MediumMagboltz("ar", 90., "co2", 10.)
gas.SetPressure(pressure * 760.)
gas.SetTemperature(293.15)
gas.SetFieldGrid(0.e3, 80.e3, 1, False)
ncoll = 100
gas.GenerateGasTable(ncoll)
gas.WriteGasFile("natalie_gas_files/ar_90_co2_10_3atm.gas")