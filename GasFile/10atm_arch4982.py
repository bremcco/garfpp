import ROOT
import Garfield
import math
import ctypes
import os
import csv

pressure = 10
gas = ROOT.Garfield.MediumMagboltz("ar", 98., "ch4", 2.)
gas.SetPressure(pressure * 760.)
gas.SetTemperature(293.15)
gas.SetFieldGrid(1.e3, 200.e3, 500, False)
ncoll = 100
gas.GenerateGasTable(ncoll)
gas.WriteGasFile("ar_98_ch4_2_10atm.gas")