
import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import defaultdict

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

trials = 10
pressure = 760.
file_name = 'GEM2_output_arco29010.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/misalignment/0_misalignment'
file_path = os.path.join(directory, file_name)

# Load the field map.
fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("0_misalignment/GEM2/ELIST.lis", "0_misalignment/GEM2/NLIST.lis", "0_misalignment/GEM2/MPLIST.lis", "0_misalignment/GEM2/PRNSOL.lis", "mm")
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
fieldView.SetArea(-0.5, -0.3, 0.5, 1.8)
fieldView.SetVoltageRange(-315., 1000.)

cF.SetLeftMargin(0.16)
fieldView.Plot("v", "colz")
cF.Update()
cF.Draw()
cF.SaveAs("v.png")

input("press enter")
'''

# Setup the gas.
gas = ROOT.Garfield.MediumMagboltz("ar", 90., "co2", 10.)
gas.SetTemperature(293.15)
gas.SetPressure(pressure)
gas.Initialise(True)

# Set the Penning transfer efficiency.
#rPenning = 0.51
gas.EnablePenningTransfer()
# Load the ion mobilities.
gas.LoadIonMobility('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt')
 
fm.SetGas(gas)
fm.PrintMaterials()

# Assemble the sensor.
sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(fm)
sensor.SetArea(-2, -1, -0.1, 2,  1, 0.3)

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

#Get the initial electron parameters
electrons_by_trial = defaultdict(list)

with open('0_misalignment/GEM1_output_arco29010.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        trial = int(row["trial"])
        electrons_by_trial[trial].append({
            "x": float(row["x"]),
            "y": float(row["y"]),
            "z": float(row["z"]),
            "dx": float(row["dx"]),
            "dy": float(row["dy"]),
            "dz": float(row["dz"]),
            "energy": float(row["energy"])
        })
with open(file_path, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["trial", "ne"])

    data = []
    for i in range(trials):
      # print i, '/', nEvents
      # Randomize the initial position. 
      electrons = electrons_by_trial[i]

      
      for e in electrons:
            aval.AvalancheElectron(
                e["x"], e["y"], 0.1,
                0., e["energy"],
                e["dx"], e["dy"], e["dz"]
            )
      
    
      aval.GetAvalancheSize(ne, ni)
      print(ne.value)
      writer.writerow([i, ne.value])

  
#write_csv(data, directory, file_name)   

'''
cD = ROOT.TCanvas('cD', '', 600, 600)
meshView = ROOT.Garfield.ViewFEMesh()
meshView.SetComponent(fm)
plotMesh = True 
if plotDrift:
  if plotMesh:
    meshView.SetArea(-2 * pitch, -0.3, 2 * pitch, 0.3)
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


