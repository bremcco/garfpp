import ROOT
import Garfield
import os
import ctypes
import numpy as np  

gas = ROOT.Garfield.MediumMagboltz()
gas.SetTemperature(293.15)
gas.SetPressure(740.)
gas.SetComposition("ar", 80., "co2", 20.)
gas.EnableDrift()

gas.Initialise(True)

rPenning = 0.51
gas.EnablePenningTransfer(rPenning, 0., "ar")

gas.LoadIonMobility('/content/garfield/garfieldpp/Data/IonMobility_Ar+_Ar.txt')

cmp = ROOT.Garfield.ComponentAnalyticField()
cmp.Clear()

cmp.SetMedium(gas)

#Define two planes with a different voltage setting
x_plane0 = 0
x_plane1 = 10 # 10 cm gap

V_plane0 = 0
V_plane1 = 1000 # 1000 Volt


cmp.AddPlaneX(x_plane0, V_plane0 ,"plane0")
cmp.AddPlaneX(x_plane1, V_plane1 ,"plane1")

sensor = ROOT.Garfield.Sensor()

sensor.AddComponent(cmp)

#Define a muon of 170GeV
track = ROOT.Garfield.TrackHeed()
track.SetParticle("muon");
track.SetEnergy(170.e9);
track.SetSensor(sensor);
#Define the impact point and direction
x0 = 0.0
y0 = -4.9
z0 = 0.0
t0 = 0.0
dx0 = 0.0
dy0 = 1.000001
dz0 = 0.0

track.NewTrack(x0, y0, z0, t0, dx0, dy0, dz0)
cluster = track.GetClusters()
print("The number of primary clusters is %i" % cluster.size())

histo_xCl  = ROOT.TH1F("histo_xCl" ,"Cluster position distribution",100,-0.01,0.01)
histo_yCl  = ROOT.TH1F("histo_yCl" ,"Cluster position distribution",100,-10,10)
histo_zCl  = ROOT.TH1F("histo_zCl" ,"Cluster position distribution",100,-0.01,0.01)
histo_dyCl = ROOT.TH1F("histo_dyCl","Spacing",100,0,0.5)

previous_y=0
next_y=0
for cluster in track.GetClusters():
    next_y = cluster.y
    distance = next_y-previous_y
    histo_xCl.Fill(cluster.x)
    histo_yCl.Fill(cluster.y)
    histo_zCl.Fill(cluster.z)
    histo_dyCl.Fill(distance)
    previous_y = cluster.y

histo_nElectron  = ROOT.TH1I("histo_nElectron" ,"Number of electron in the cluster",100,1,101)
track.NewTrack(x0, y0, z0, dx0, dy0, dz0, 0)
track.GetClusters().size()

for cluster in track.GetClusters():
  xc = ctypes.c_double()
  yc = ctypes.c_double()
  zc = ctypes.c_double()
  tc = ctypes.c_double()
  nelectrons = ctypes.c_int()
  nions = ctypes.c_int()
  ec = ctypes.c_double()
  extra = ctypes.c_double()

  track.GetCluster(xc,yc,zc,tc,nelectrons,nions,ec,extra)
  histo_nElectron.Fill(nelectrons.value)

canvas = ROOT.TCanvas("canvas","",800,600)
canvas.cd()
histo_nElectron.Draw()
canvas.Draw()

canvas.SaveAs('test.png')

