
import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv
import math


gas = ROOT.Garfield.MediumMagboltz("ne", 85.72, "co2", 9.52, "n2", 4.76)
gas.SetTemperature(293.15)
gas.SetPressure(750)
gas.Initialise(True)

gas.LoadGasFile("Ne_90_CO2_10_N2_5_with_mg.gas")
gas.LoadIonMobility('IonMobility_Ne+_Ne.txt')


cmpe = ROOT.Garfield.ComponentAnalyticField()
cmpe.SetMedium(gas)

cmpi = ROOT.Garfield.ComponentAnalyticField()
cmpi.SetMedium(gas)



iroc = True  # or False
gap = 0.2 if iroc else 0.3

period = 0.25
cmpe.SetPeriodicityX(period)
cmpi.SetPeriodicityX(period)

xs = 0
ys = gap
ds = 0.0020
vs = 1460.0 if iroc else 1570.0
cmpe.AddWire(xs,ys,ds,vs,"s",100.0,50.0,19.3,1)
cmpi.AddWire(xs, ys, ds, vs)

xc = 0.5*period
yc = 2*gap
dc = 0.0075
cmpe.AddWire(xc,yc,dc,0.0,"c",100.0, 50.0, 19.3, 1)
cmpi.AddWire(xc, yc, dc, 0.)

xg1 = 0.25*period
xg2 = 0.75 * period
yg = 2.0*gap+0.3
dg = 0.0075
vg = -70.0
deltav = 90.
cmpe.AddWire(xg1,yg,dg,vg,"g",100.0, 50.0, 19.3, 1)
cmpe.AddWire(xg2,yg,dg,vg,"g",100.0, 50.0, 19.3 ,1)
cmpi.AddWire(xg1, yg, dg, vg + deltav, "g+")
cmpi.AddWire(xg2, yg, dg, vg - deltav, "g-")

cmpe.AddPlaneY(0.0,0.0,"pad_plane")
cmpi.AddPlaneY(0., 0., "pad_plane")
yHV = 249.7
vHV = -100000
cmpe.AddPlaneY(yHV,vHV)
cmpi.AddPlaneY(yHV, vHV)



cmpe.SetMagneticField(0,0.5,0)
cmpi.SetMagneticField(0, 0.5, 0)

xmin = -3 * period
xmax = 3 * period

sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(cmpe)
sensor.AddComponent(cmpi)
sensor.SetArea(xmin, 0., -1., xmax, yHV, 1.)
sensor.AddElectrode(cmpi, "pad_plane")

drift = ROOT.Garfield.DriftLineRKF()
drift.SetSensor(sensor)
'''
xt = xmin
yt = 0.5 * yHV
track = ROOT.Garfield.TrackHeed()
track.SetSensor(sensor)
track.SetParticle('pi')
track.SetMomentum(1.e9)
track.NewTrack(xt,yt,0.0,0.0,1.0,0.0,0.0)

total_electrons = 0
clusters = track.GetClusters()
print(f"Number of clusters: {len(clusters)}")

for i, cluster in enumerate(clusters):
    n_electrons = len(cluster.electrons)
    total_electrons += n_electrons
    print(f"Cluster {i}: {n_electrons} electrons")

print(f"Total number of electrons: {total_electrons}")
'''
'''
gain = 10.0
for cluster in track.GetClusters():
    for electron in cluster.electrons:
        y0 = electron.y

        dT = 0.0198
        sigma = dT * math.sqrt(max(y0,1.2)-1.2)
        x0 = electron.x + ROOT.Garfield.RndmGaussian() * sigma
        z0 = electron.z + ROOT.Garfield.RndmGaussian() * sigma

        sensor.EnableComponent(0,True)
        sensor.EnableComponent(1, False)
        drift.DriftElectron(x0,1.2,z0,0)
        
        x1 = 0
        y1 = gap
        z1 = 0
        t1 = 0
        status = 0
        theta = 0.4

        drift.GetEndpoint(x1,y1,z1,t1,status)
        sensor.EnableComponent(1,True)
        sensor.EnableComponent(0,False)

        low_thresh = 0.5 * gap
        high_thresh = 1.5 * gap

        if low_thresh < y1 < high_thresh:
            nIons = int(round(ROOT.Garfield.RndmPolya(theta) * gain))
            print(nIons)
            r = 0.01
            for i in range(nIons):
                angle = ROOT.Garfield.RndmGaussian(0,1.4)
                x_drift = x1 + r * math.sin(angle)
                y_drift = gap + r * math.cos(angle)
                drift.DriftIon(x_drift,y_drift,0,0)


'''
fieldView = ROOT.Garfield.ViewField()

fieldView.SetComponent(cmpe)
fieldView.SetArea(xmin,-1.0,xmax,5*gap)
fieldView.SetVoltageRange(-1000.0,1000.0)

ROOT.SetOwnership(fieldView, False)
ROOT.SetOwnership(cmpe, False)

fieldView.PlotContour()
canvas = fieldView.GetCanvas()
canvas.SaveAs("alicefield.png")

'''
driftView = ROOT.Garfield.ViewDrift()
drift.EnablePlotting(driftView)

cellView = ROOT.Garfield.ViewCell()
ROOT.SetOwnership(cellView,False)
cellView.SetComponent(cmpi)
cellView.SetArea(xmin,0.0,xmax,5*gap)
cellView.Plot2d()
driftView.SetArea(xmin,0.0,xmax,5*gap)
driftView.SetCanvas(cellView.GetCanvas())
driftView.Plot(True,False)
#canvas = cellView.GetCanvas()
#canvas.SaveAs('alicedrift.png')

signalView = ROOT.Garfield.ViewSignal()

signalView.SetSensor(sensor)
ROOT.SetOwnership(signalView,False)
signalView.PlotSignal("pad_plane")

def transfer(t):
    tau = 160  # peaking time in ns
    fC_to_mV = 12.7  # mV per fC
    return fC_to_mV * math.exp(4) * (t / tau)**4 * math.exp(-4 * t / tau)

sensor.SetTransferFunction(transfer)
fft = True
sensor.ConvoluteSignal("pad_plane",fft)
signalView.PlotSignal("pad_plane")
'''