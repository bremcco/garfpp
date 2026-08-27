import ROOT
import Garfield
import ctypes

pressure = 1
gas = ROOT.Garfield.MediumMagboltz("ar", 90., "co2", 10.)
gas.SetPressure(pressure * 760.)  # Torr
gas.SetTemperature(293.15)
gas.SetFieldGrid(0.e3, 80.e3, 90 , False)

gas.LoadGasFile("ar_98_ch4_2_1atm.gas")


canv = ROOT.TCanvas("c1", "Electron Drift Velocity", 800, 600)
mediumView = ROOT.Garfield.ViewMedium()
mediumView.SetMedium(gas)
mediumView.SetCanvas(canv)

mediumView.PlotElectronVelocity('e')
canv.Update()

for prim in canv.GetListOfPrimitives():
    if isinstance(prim, ROOT.TGraph):
        n = prim.GetN()
        print("Points from plot:")
        for i in range(n):
            x = ctypes.c_double(0.0)
            y = ctypes.c_double(0.0)
            prim.GetPoint(i, x, y)
            print(f"x = {x.value:.2f}, y = {y.value:.6e}")

canv.SaveAs("arch4982.png")

del mediumView
del gas
del canv
import gc; gc.collect()
