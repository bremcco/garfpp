import ROOT
import Garfield
import math

# ----------------------------
# Gas files (manual list)

gas_files = [
("ar_90_co2_10_1atm.gas", ROOT.kRed),
 ("ar_92_ch4_8_1atm.gas", ROOT.kBlue),
 ("ar_96_ch4_4_1atm.gas", ROOT.kGreen),
 ("ar_98_ch4_2_1atm.gas", ROOT.kMagenta)
]
# ----------------------------

# Canvas
c = ROOT.TCanvas("c", "Drift velocity comparison", 900, 700)

# Draw axes first (empty dummy graph)
frame = ROOT.TH2F("frame", "Electron Drift Velocity; Electric Field (V/cm); Velocity (cm/#mus)",
                  100, 0, 1000,    # x-axis: 0–1000 V/cm
                  100, 0, 10)      # y-axis: adjust depending on gas velocities
frame.Draw()

legend = ROOT.TLegend(0.15, 0.68, 0.45, 0.88)

for gasfile, color in gas_files:

    # Load gas
    gas = ROOT.Garfield.MediumMagboltz()
    if not gas.LoadGasFile(gasfile):
        raise RuntimeError(f"Failed to load {gasfile}")

    # ViewMedium for this gas
    medView = ROOT.Garfield.ViewMedium()
    medView.SetMedium(gas)

    # IMPORTANT: do not clear canvas, just draw curves on it
    medView.SetCanvas(c)
    medView.PlotElectronVelocity("e")

    legend.AddEntry(None, gasfile, "l")

legend.Draw()

c.SaveAs("drift_velocity_viewmedium.png")
print("Saved drift_velocity_viewmedium.png")