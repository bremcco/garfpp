import ROOT
import csv

# -----------------------------
# CSV files and styles
# -----------------------------
csv_files = [
    "driftv_arco29010.csv",
    "driftv_arch4928.csv",
    "driftv_arch4964.csv",
    "driftv_arch4982.csv"
]

labels = [
    "Ar-CO2 90-10",
    "Ar-CH4 92-8",
    "Ar-CH4 96-4",
    "Ar-CH4 98-2"
]

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kMagenta]
markers = [20, 21, 22, 23]

graphs = []

# -----------------------------
# Read CSVs and create TGraphs
# -----------------------------
for i, file in enumerate(csv_files):
    x_vals = []
    y_vals = []
    with open(file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            x = float(row[0].replace("x =", "").strip())
            y = float(row[1].replace("y =", "").strip())
            x_vals.append(x)
            y_vals.append(y)

    n = len(x_vals)
    g = ROOT.TGraph(n)
    for j, (x, y) in enumerate(zip(x_vals, y_vals)):
        g.SetPoint(j, x, y)

    g.SetLineColor(colors[i])
    g.SetMarkerColor(colors[i])
    g.SetMarkerStyle(markers[i])
    g.SetTitle("Electron Drift Velocity;Electric Field [V/cm];v_d [cm/ns]")

    graphs.append(g)

# -----------------------------
# Draw all graphs
# -----------------------------
canv = ROOT.TCanvas("c1", "Electron Drift Velocity", 800, 600)

# Draw first graph with axes
graphs[0].SetMinimum(0.0)
graphs[0].SetMaximum(0.01)
graphs[0].Draw("AL*")



# Draw remaining graphs on same canvas
for g in graphs[1:]:
    g.Draw("L* SAME")

# -----------------------------
# Add legend
# -----------------------------
legend = ROOT.TLegend(0.6, 0.65, 0.88, 0.88)  # x1, y1, x2, y2
for g, label in zip(graphs, labels):
    legend.AddEntry(g, label, "lp")  # "lp" = line + marker
legend.SetBorderSize(0)  # optional: no border
legend.SetFillStyle(0)   # optional: transparent background
legend.Draw()

# -----------------------------
canv.Update()
canv.SaveAs("driftvelocitycomp.png")
