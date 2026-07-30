import ROOT
import Garfield
import ctypes
import matplotlib.pyplot as plt

# -----------------------------
# User settings
# -----------------------------
gas_file = "ar_92_ch4_8_1atm.gas"
ymin = 0.0      # drift velocity min (cm/us)
ymax = 0.1      # drift velocity max (cm/us)

# -----------------------------
# Load gas
# -----------------------------
gas = ROOT.Garfield.MediumMagboltz()
gas.LoadGasFile(gas_file)

# -----------------------------
# ROOT canvas and view
# -----------------------------
canvas = ROOT.TCanvas("c1", "Electron Drift Velocity", 800, 600)
medium_view = ROOT.Garfield.ViewMedium()
medium_view.SetMedium(gas)
medium_view.SetCanvas(canvas)
medium_view.PlotElectronVelocity('e')  # 'e' for electrons
canvas.Update()

# -----------------------------
# Extract the TGraph from the canvas
# -----------------------------
primitives = canvas.GetListOfPrimitives()
graphs = [p for p in primitives if isinstance(p, ROOT.TGraph)]

if not graphs:
    raise RuntimeError("No TGraph found on the canvas!")

# Take the first TGraph with points
graph = next((g for g in graphs if g.GetN() > 0), None)
if graph is None:
    raise RuntimeError("No TGraph with points found!")

# Set y-axis limits
graph.GetYaxis().SetRangeUser(ymin, ymax)
canvas.Modified()
canvas.Update()

# -----------------------------
# Extract data for Matplotlib
# -----------------------------
n_points = graph.GetN()
x_vals, y_vals = [], []

for i in range(n_points):
    x = ctypes.c_double()
    y = ctypes.c_double()
    graph.GetPoint(i, x, y)
    x_vals.append(x.value / 1e3)      # V/cm -> kV/cm
    y_vals.append(y.value)       # cm/us -> μm/ns

# -----------------------------
# Plot with Matplotlib
# -----------------------------
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_vals, lw=2, label="Electron Drift Velocity")

plt.xlabel("Electric Field [kV/cm]")
plt.ylabel("Drift Velocity [μm/ns]")
plt.title(f"Electron Drift Velocity ({gas_file})")
plt.grid(True)
plt.ylim(ymin*10, ymax*10)  # match the ROOT limits
plt.legend()
plt.tight_layout()
plt.savefig("drift_velocity.png", dpi=300)
plt.show()

# -----------------------------
# Clean up
# -----------------------------
del medium_view
del gas
del canvas
