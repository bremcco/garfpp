

import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys


ROOT.gROOT.SetBatch(True)

def main():
    

    # Setup the gas.
    gas = ROOT.Garfield.MediumMagboltz("ar", 70., "co2", 30.)
    gas.SetTemperature(293.15)
    gas.SetPressure(760.)
    gas.Initialise(True)
    gas.EnablePenningTransfer()
    gas.LoadIonMobility("IonMobility_Ar+_Ar.txt")

    # Load the field map.
    fm = ROOT.Garfield.ComponentAnsys123()
    fm.EnableDeleteBackgroundElements(False)
    fm.Initialise("gemmovie/ELIST.lis", "gemmovie/NLIST.lis", "gemmovie/MPLIST.lis", "gemmovie/PRNSOL.lis", "mm")
    fm.EnableMirrorPeriodicityX()
    fm.EnableMirrorPeriodicityY()
    fm.PrintRange()

    fm.SetGas(gas)
    fm.PrintMaterials()

   # Dimensions of the GEM [cm]
    pitch = 0.07

    # Assemble the sensor.
    sensor = ROOT.Garfield.Sensor()
    sensor.AddComponent(fm)
    sensor.SetArea(-5 * pitch, -5 * pitch, -0.2, 5 * pitch,  5 * pitch, 0.5)

    aval = ROOT.Garfield.AvalancheMicroscopic()
    aval.SetSensor(sensor)
    drift = ROOT.Garfield.AvalancheMC()
    drift.SetSensor(sensor)
    drift.SetTimeSteps(0.05)

    fieldView = ROOT.Garfield.ViewField()
    fieldView.SetComponent(fm)
    fieldView.SetPlane(0, -1, 0, 0, 0, 0)
    fieldView.SetArea(-2 * pitch, -0.02, 2 * pitch, 0.02)
    fieldView.SetVoltageRange(-150., 150.)

    canvas = ROOT.TCanvas("cCanvas", "", 600, 600)
    canvas.SetLeftMargin(0.16)
    fieldView.SetCanvas(canvas)

    plotField = False

    meshView = ROOT.Garfield.ViewFEMesh()
    meshView.SetArea(-2 * pitch, -0.02, 2 * pitch, 0.02)
    meshView.SetComponent(fm)
    meshView.SetPlane(0, -1, 0, 0, 0, 0)
    meshView.SetFillMesh(True)
    meshView.SetColor(2, ROOT.kGray)
    meshView.SetCanvas(canvas)

    driftView = ROOT.Garfield.ViewDrift()
    aval.EnableExcitationMarkers(False)
    aval.EnableIonisationMarkers(False)
    aval.EnableAttachmentMarkers(False)
    aval.EnablePlotting(driftView)
    drift.EnablePlotting(driftView)
    driftView.SetPlane(0, -1, 0, 0, 0, 0)
    driftView.SetArea(-2 * pitch, -0.02, 2 * pitch, 0.02)
    driftView.SetCanvas(canvas)

    label = ROOT.TLatex()

    # Add the initial electron.
    x0, y0, z0, t0, e0 = 0., 0., 0.02, 0., 0.1
    aval.AddElectron(x0, y0, z0, t0, e0)

    prev = [(x0, y0, z0, t0, e0)]
    tmin = 0.0
    dt = 0.1
    nFrames = 207

    os.makedirs("frames", exist_ok=True)

    for i in range(nFrames):
        if i % 10 == 0:
            print(f"Frame {i}")

        driftView.Clear()

        if len(aval.GetElectrons()) > 0:
            aval.SetTimeWindow(tmin, tmin + dt)
            aval.ResumeAvalanche()

            next_prev = []
            for electron in aval.GetElectrons():
                x1 = electron.path.front().x
                y1 = electron.path.front().y
                z1 = electron.path.front().z
                t1 = electron.path.front().t

                existing = False
                tol = 1.e-5
                for p in prev:
                    if (abs(x1 - p[0]) < tol and abs(y1 - p[1]) < tol and
                        abs(z1 - p[2]) < tol and abs(t1 - p[3]) < tol):
                        existing = True
                        break

                if not existing:
                    drift.AddIon(x1, y1, z1, t1)

                x2 = electron.path.back().x
                y2 = electron.path.back().y
                z2 = electron.path.back().z
                t2 = electron.path.back().t
                e2 = electron.path.back().energy
                next_prev.append((x2, y2, z2, t2, e2))

            prev = next_prev

        if len(drift.GetIons()) > 0:
            drift.SetTimeWindow(tmin, tmin + dt)
            drift.ResumeAvalanche()

        if plotField and i < 5:
            fieldView.Plot("v", "CONT1")
            driftView.Plot2d(False, True)
        else:
            driftView.Plot2d(True, True)

        meshView.Plot(True)

        canvas.cd()
        if i < 100:
            text = f"#it{{t}} = {tmin + dt:04.1f} ns"
        else:
            text = f"#it{{t}} = {1.e-3 * (tmin + dt):04.2f} #mus"
        label.DrawLatexNDC(0.3, 0.88, text)

        canvas.Update()
        ROOT.gSystem.ProcessEvents()

        gif = True
        if not gif:
            filename = f"frames/frame_{i:03d}.png"
            canvas.SaveAs(filename)
        else:
            if i == nFrames - 1:
                canvas.Print("gem_movie.gif++")
            else:
                canvas.Print("gem_movie.gif+3")

        tmin += dt
        if i == 99:
            dt = 10.0
            drift.SetTimeSteps(1.0)
        elif i == 108:
            dt = 100.0
            drift.SetTimeSteps(10.0)

 

if __name__ == "__main__":
    main()