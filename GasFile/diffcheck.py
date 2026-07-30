import ROOT
import ctypes
import Garfield

ROOT.gSystem.Load("libGarfield")

gas = ROOT.Garfield.MediumMagboltz("ar", 90., "co2", 10.)
gas.SetTemperature(293.15)
gas.SetPressure(760.)
gas.Initialise(True)

E = 105.263  # V/cm

dl = ctypes.c_double(0.0)
dt = ctypes.c_double(0.0)

ok = gas.GetDiffusion(E, dl, dt)
if not ok:
    raise RuntimeError("Diffusion not available")

print("DL =", dl.value, "cm^2/s")
print("DT =", dt.value, "cm^2/s")
