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

gas.LoadIonMobility('IonMobility_Ar+_Ar.txt')

diameter = 7.8
length = 10
tube = ROOT.Garfield.SolidTube(0,0,0,0.5*diameter,length)

geo = ROOT.Garfield.GeometrySimple()
geo.AddSolid(tube,gas)

field = ROOT.Garfield.ComponentConstant()
field.SetGeometry(geo)
field.SetElectricField(0.0,0.0,500.0)


sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(field)

track = ROOT.Garfield.TrackHeed()
track.SetSensor(sensor)
track.EnableElectricField()

nBins = 500

hElectrons= ROOT.TH1F("hElectrons" ," # electrons",nBins,-0.5,nBins-0.5)
nEvents = 100000

for i in range(nEvents):
    x0 = 0
    y0 = 0
    z0 = 0
    t0 = 0

    ne = ctypes.c_int(0)
    ni = ctypes.c_int(0)
    np = ctypes.c_int(1)
  

    r = 167.0 * ROOT.Garfield.RndmUniform()
    egamma = 0
    if r < 100.0:
        egamma = 5898.8
    elif r < 150.0:
        egamma = 5887.6
    else:
        egamma = 6490.4
    
    cluster = track.TransportPhoton(x0,y0,z0,t0,egamma,0.0,0.0,1.0,ne,ni,np)
    if ne.value > 0:
        hElectrons.Fill(ne.value)

canvas = ROOT.TCanvas("canvas","",800,600)
canvas.cd()
hElectrons.SetTitle("Fe55 Spectrum")  # Main plot title
hElectrons.GetXaxis().SetTitle("Number of Electrons")  # X-axis label
hElectrons.GetYaxis().SetTitle("Counts") 
hElectrons.Draw()
canvas.Update()

canvas.SaveAs('test.png')




