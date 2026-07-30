import ROOT
import Garfield
import math
import ctypes

# Switch between IROC and OROC
iroc = False

# Distance between rows of wires [cm]
gap = 0.2 if iroc else 0.3

# Periodicity (wire spacing) [cm]
period = 0.25

# Wire diameters [cm]
ds = 0.0020  # Sense wires
dc = 0.0075  # Cathode wires
dg = 0.0075  # Gate wires

# Voltage settings [V]
vs = 1460. if iroc else 1570.
vg = -70.
deltav = 90.

# HV plane (drift field)
yHV = 249.7
vHV = -100000

# Setup the gas
gas = ROOT.Garfield.MediumMagboltz()
gas.SetTemperature(293.15)
gas.SetPressure(750.)
gas.SetComposition("ne", 85.72, "co2", 9.52, "n2", 4.76)
gas.LoadGasFile("Ne_90_CO2_10_N2_5_with_mg.gas")
gas.LoadIonMobility("IonMobility_Ne+_Ne.txt")

# Setup the electric field
cmpe = ROOT.Garfield.ComponentAnalyticField()
cmpi = ROOT.Garfield.ComponentAnalyticField()
cmpe.SetMedium(gas)
cmpi.SetMedium(gas)
cmpe.SetPeriodicityX(period)
cmpi.SetPeriodicityX(period)

# Add the sense (anode) wires
xs = 0.
ys = gap
cmpe.AddWire(xs, ys, ds, vs)
cmpi.AddWire(xs, ys, ds, vs)

# Add the cathode wires
xc = 0.5 * period
yc = 2 * gap
cmpe.AddWire(xc, yc, dc, 0.)
cmpi.AddWire(xc, yc, dc, 0.)

# Add the gate wires
xg1 = 0.25 * period
xg2 = 0.75 * period
yg = 2. * gap + 0.3
cmpe.AddWire(xg1, yg, dg, vg, "g", 100., 50., 19.3, 1)
cmpe.AddWire(xg2, yg, dg, vg, "g", 100., 50., 19.3, 1)
cmpi.AddWire(xg1, yg, dg, vg + deltav, "g+")
cmpi.AddWire(xg2, yg, dg, vg - deltav, "g-")

# Add planes
cmpe.AddPlaneY(0., 0., "pad_plane")
cmpi.AddPlaneY(0., 0., "pad_plane")
cmpe.AddPlaneY(yHV, vHV)
cmpi.AddPlaneY(yHV, vHV)

# Set the magnetic field [T]
cmpe.SetMagneticField(0, 0.5, 0)
cmpi.SetMagneticField(0, 0.5, 0)

# Make a sensor
sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(cmpe)
sensor.AddComponent(cmpi)
sensor.AddElectrode(cmpi, "pad_plane")
xmin = -3 * period
xmax = 3 * period
sensor.SetArea(xmin, 0., -1., xmax, yHV, 1.)

fieldView = ROOT.Garfield.ViewField()
fieldView.SetComponent(cmpe)
fieldView.SetArea(xmin, 0., xmax, 5 * gap)
fieldView.SetVoltageRange(-400., 1000.)
fieldView.PlotContour()
ROOT.SetOwnership(fieldView, False)
# Drift setup
drift = ROOT.Garfield.DriftLineRKF()
drift.SetSensor(sensor)

# Gain parameters
theta = 0.4  # Polya parameter
gain = 10

# Setup the charged particle track
track = ROOT.Garfield.TrackHeed()
track.SetSensor(sensor)
track.SetParticle("pi")
track.SetMomentum(1.e9)  # [eV / c]

# Drift view (optional)
driftView = ROOT.Garfield.ViewDrift()
plotDriftLines = True
if plotDriftLines:
    drift.EnablePlotting(driftView)


# Simulate a track
xt = xmin
yt = 0.5 * yHV
track.NewTrack(xt, yt, 0., 0., 1., 0., 0.)

# Retrieve the clusters
#clusters = track.GetClus
for cluster in track.GetClusters():
   
    for electron in cluster.electrons:
        
        y0 = electron.y

        # Smear coordinates
        dT = 0.0198
        sigma = dT * math.sqrt(max(y0, 1.2) - 1.2)
        x0 = electron.x + ROOT.Garfield.RndmGaussian() * sigma
        z0 = electron.z + ROOT.Garfield.RndmGaussian() * sigma

        sensor.EnableComponent(0, False)
        sensor.EnableComponent(1, True)

        if x0 < xmin or x0 > xmax:
            continue

        drift.DriftElectron(x0, 1.2, z0, 0.)
        #x1, y1, z1, t1 = 0., gap, 0., 0.
        x1 = ctypes.c_double(0.0)
        y1 = ctypes.c_double(gap)  
        z1 = ctypes.c_double(0.0)
        t1 = ctypes.c_double(0.0)
        status = ctypes.c_int(0)

        drift.GetEndPoint(x1, y1, z1, t1, status)

        sensor.EnableComponent(1, False)
        sensor.EnableComponent(0, True)

        if 0.5 * gap < y1.value < 1.5 * gap:
            # Electron drifted to a sensing wire

            # Sample the gain from a Polya distribution
            # You may need to define a Polya distribution method
    
            nIons = int(round(ROOT.Garfield.RndmPolya(theta)*gain))
            for _ in range(nIons):
                r = 0.01
                angle = ROOT.Garfield.RndmGaussian(0, 1.4)
                xi = x1.value + r * math.sin(angle)
                yi = gap + r * math.cos(angle)

                if xi < xmin or xi > xmax:
                    continue

                drift.DriftIon(xi, yi, 0., 0.)


cellView = ROOT.Garfield.ViewCell()
ROOT.SetOwnership(cellView, False)  # Prevent Python from deleting C++ object

# Set the component (e.g. cmpe is a Sensor or Component object)
cellView.SetComponent(cmpe)

# Define area: (xmin, ymin, xmax, ymax)
cellView.SetArea(xmin, 0., xmax, 5 * gap)

# Plot the 2D cell layout
cellView.Plot2d()

# If drift lines are to be plotted
if plotDriftLines:
    driftView = ROOT.Garfield.ViewDrift()
    ROOT.SetOwnership(driftView, False)
    
    driftView.SetArea(xmin, 0., xmax, 5 * gap)
    driftView.SetCanvas(cellView.GetCanvas())  # Reuse same canvas
    driftView.Plot(True, False)
    canvas = cellView.GetCanvas()
    canvas.SaveAs("cell_with_drift.png")

