import ROOT
import Garfield
import ctypes

# -----------------------------
# Gas setup
# -----------------------------
pressure = 1
gas = ROOT.Garfield.MediumMagboltz("ar", 90., "co2", 10.)
gas.SetPressure(pressure * 760.)  # Torr
gas.SetTemperature(293.15)
gas.SetFieldGrid(0.e3, 80.e3, 90 , False)

# Load pre-generated gas file
gas.LoadGasFile("ar_98_ch4_2_1atm.gas")

# -----------------------------
# ROOT canvas and Garfield view
# -----------------------------
canv = ROOT.TCanvas("c1", "Electron Drift Velocity", 800, 600)
mediumView = ROOT.Garfield.ViewMedium()
mediumView.SetMedium(gas)
mediumView.SetCanvas(canv)

# Plot electron drift velocity
mediumView.PlotElectronVelocity('e')
canv.Update()

# Extract points from TGraph
for prim in canv.GetListOfPrimitives():
    if isinstance(prim, ROOT.TGraph):
        n = prim.GetN()
        print("Points from plot:")
        for i in range(n):
            x = ctypes.c_double(0.0)
            y = ctypes.c_double(0.0)
            prim.GetPoint(i, x, y)
            print(f"x = {x.value:.2f}, y = {y.value:.6e}")

# -----------------------------
# Save the plot
# -----------------------------
canv.SaveAs("arch4982.png")

# -----------------------------
# Clean up
# -----------------------------
del mediumView
del gas
del canv
import gc; gc.collect()
