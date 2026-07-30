
import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv

def write_csv(rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)

    write_header = not os.path.exists(file_path)

    with open(file_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if write_header:
            writer.writerow([
                "N1_before",
                "N1_after",
                "N2_before",
                "N2_after"
            ])

        for row in rows:
            writer.writerow(row)



# GEM 1 planes
z_gem1_before = -0.206   # bottom of GEM 1
z_gem1_after  = -0.1     # middle of transfer gap

# GEM 2 planes
z_gem2_before = -0.1     # transfer gap above GEM 2
z_gem2_after  =  0.0     # past top copper of GEM 2


'''
def crossed_plane(path, z_plane):
    for i in range(len(path) - 1):
        if path[i].z < z_plane and path[i+1].z >= z_plane:
            return True
    return False
'''

path = os.getenv('GARFIELD_INSTALL')

trials = 1
pressure = 760. * 2.0
file_name = '2_0atm.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/t_field1/1000'


# Load the field map.
fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("1000/ELIST.lis", "1000/NLIST.lis", "1000/MPLIST.lis", "1000/PRNSOL.lis", "micron")
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
#rPenning = 0.51
gas.EnablePenningTransfer()
# Load the ion mobilities.
gas.LoadIonMobility('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt')
 
fm.SetGas(gas)
fm.PrintMaterials()

# Assemble the sensor.
sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(fm)
sensor.SetArea(-2, -1, -2, 2,  1, 0.01)

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


rows = []

for i in range(trials):

    N1_before = 0
    N1_after  = 0
    N2_before = 0
    N2_after  = 0

    x0 = 0
    y0 = 0
    z0 = -0.4
    t0 = 0.
    e0 = 0.07

    aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.)
    aval.GetAvalancheSize(ne, ni)

    electrons = aval.GetElectrons()

    for electron in electrons:
        path = electron.path
        z_birth = path[0].z
        z_end   = path[-1].z

        # ====================
        # GEM 1: extraction into transfer gap
        # ====================
        if z_birth < -0.201:
            N1_before += 1

        # survives into transfer gap
        if z_end >= -0.05025:
            N1_after += 1

        # ====================
        # GEM 2: collection into holes
        # ====================
        if z_birth < -0.1005 and z_end > -0.1005:
            N2_before += 1

            # survives past top copper
        if z_end >= 0.0:
            N2_after += 1

    rows.append([N1_before, N1_after, N2_before, N2_after])




write_csv(rows, directory, file_name)


'''
cD = ROOT.TCanvas('cD', '', 600, 600)
meshView = ROOT.Garfield.ViewFEMesh()
meshView.SetComponent(fm)
plotMesh = True 
if plotDrift:
  if plotMesh:
    meshView.SetArea(-2 * pitch, -1, 2 * pitch, 1)
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
