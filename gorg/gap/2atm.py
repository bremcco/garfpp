
import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv

def write_csv(data, directory, filename):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(directory, filename)
    
    # Write the integers to the CSV file
    with open(file_path, mode = 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item])

path = os.getenv('GARFIELD_INSTALL')

trials = 1
pressure = 760. * 2.0
file_name = '2atm.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/gorg/gap/ar_ch4_98_2'


# Load the field map.
fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("ELIST.lis", "NLIST.lis", "MPLIST.lis", "PRNSOL.lis", "micron")
fm.EnableMirrorPeriodicityX()
fm.EnableMirrorPeriodicityY()
fm.PrintRange()

# Dimensions of the GEM [cm]
pitch = 0.014
'''
fieldView = ROOT.Garfield.ViewField()
cF = ROOT.TCanvas('cF', '', 600, 600)
fieldView.SetCanvas(cF)
fieldView.SetComponent(fm)
# Set the viewing plane (xz plane).
fieldView.SetPlaneXZ()
# Set the plot limits in the current viewing plane.
fieldView.SetArea(-1, -1.9, 1, 1)
fieldView.SetVoltageRange(-3600., 0000.)

cF.SetLeftMargin(0.16)
fieldView.Plot("v", "colz")
cF.Update()
cF.Draw()
cF.SaveAs("v.png")

input("press enter")

'''
# Setup the gas.
gas = ROOT.Garfield.MediumMagboltz("ar", 98., "ch4", 2.)
gas.SetTemperature(293.15)
gas.SetPressure(pressure)
gas.Initialise(True)

# Set the Penning transfer efficiency.

gas.EnablePenningTransfer()
# Load the ion mobilities.
gas.LoadIonMobility('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt')
 
fm.SetGas(gas)
fm.PrintMaterials()

# Assemble the sensor.
sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(fm)
sensor.SetArea(-2, -1, -2, 2,  1, 0.5)

aval = ROOT.Garfield.AvalancheMicroscopic()
aval.SetSensor(sensor)

drift = ROOT.Garfield.AvalancheMC()
drift.SetSensor(sensor)
drift.SetDistanceSteps(2.e-4)

driftView = ROOT.Garfield.ViewDrift()
plotDrift = True
if plotDrift:
  aval.EnablePlotting(driftView)
  drift.EnablePlotting(driftView)

# Count the total number of ions and the back-flowing ions.
nTotal = 0
nBF = 0
ne= ctypes.c_int()
ni= ctypes.c_int()

ne_list=[]
for i in range(trials):
  # print i, '/', nEvents
  # Randomize the initial position. 
  x0 = -0.5 * pitch + ROOT.Garfield.RndmUniform() * pitch
  y0 = -0.5 * pitch + ROOT.Garfield.RndmUniform() * pitch
  z0 = -1.7
  t0 = 0.
  e0 = 0.07
  aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.)
  aval.GetAvalancheSize(ne, ni)
  ne_list.append(ne.value)

write_csv(ne_list,directory, file_name)
'''
cD = ROOT.TCanvas('cD', '', 600, 600)
meshView = ROOT.Garfield.ViewFEMesh()
meshView.SetComponent(fm)
plotMesh = True 
if plotDrift:
  if plotMesh:
    meshView.SetArea(-2 * pitch, -1.0, 2 * pitch, 1.0)
    meshView.SetCanvas(cD)
    # x-z projection.
    meshView.SetPlane(0, -1, 0, 0, 0, 0)
    meshView.SetFillMesh(True)
    #  Set the color of the kapton.
    meshView.SetColor(2, ROOT.kYellow + 3)
    meshView.EnableAxes()
    meshView.SetViewDrift(driftView)
    meshView.Plot()
  else:
    driftView.SetCanvas(cD)
    driftView.SetPlane(0, -1, 0, 0, 0, 0)
    driftView.SetArea(-2 * pitch, -1, 2 * pitch, 1)
    driftView.Plot(True)
cD.Update()
cD.SaveAs('avalanche_test.png')
'''

