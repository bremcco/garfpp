import ROOT
import Garfield
import math
import ctypes
import os
import csv



def write_csv(data, directory, filename):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(directory, filename)
    
    # Write the integers to the CSV file
    with open(file_path, mode = 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item])

directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/alice/goat_data/1'
file_name = '1150.csv'
pressure = 760.0 * 1



trials = 1
iroc = True
gap = 0.2 if iroc else 0.3
period = 0.25
ds = 0.0020
dc = 0.0075
dg = 0.0075
vs = 1150.0
#vs = 1460. if iroc else 1570.
#vg = -70.0
vg = -125.0
deltav = 90.
yHV = 249.7
vHV = -400.0
r_wire = 0.5 * ds

xmin = -3. * period
constexpr double xmax = 3. * period

GAS_FILE = "GOAT_ar_90_co2_10_1atm.gas"
gas = ROOT.Garfield.MediumMagboltz("ar", 90., "co2", 10.)

gas.SetTemperature(293.15)
gas.SetPressure(pressure)
gas.EnablePenningTransfer()
gas.LoadIonMobility('IonMobility_Ar+_Ar.txt')

cmpe = ROOT.Garfield.ComponentAnalyticField()
cmpi = ROOT.Garfield.ComponentAnalyticField()
cmpe.SetMedium(gas)
cmpi.SetMedium(gas)
cmpe.SetPeriodicityX(period)
cmpi.SetPeriodicityX(period)

xs = 0.
ys = gap
cmpe.AddWire(xs, ys, ds, vs)
cmpi.AddWire(xs, ys, ds, vs)

xc = 0.5 * period
yc = 2 * gap
cmpe.AddWire(xc, yc, dc, 0.)
cmpi.AddWire(xc, yc, dc, 0.)

xg1 = 0.25 * period
xg2 = 0.75 * period
yg = 2. * gap + 0.3
cmpe.AddWire(xg1, yg, dg, vg, "g", 100., 50., 19.3, 1)
cmpe.AddWire(xg2, yg, dg, vg, "g", 100., 50., 19.3, 1)
cmpi.AddWire(xg1, yg, dg, vg + deltav, "g+")
cmpi.AddWire(xg2, yg, dg, vg - deltav, "g-")

cmpe.AddPlaneY(0., 0., "pad_plane")
cmpi.AddPlaneY(0., 0., "pad_plane")
cmpe.AddPlaneY(yHV, vHV)
cmpi.AddPlaneY(yHV, vHV)

cmpe.SetMagneticField(0, 0.5, 0)
cmpi.SetMagneticField(0, 0.5, 0)

sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(cmpe)
sensor.AddComponent(cmpi)
sensor.AddElectrode(cmpi, "pad_plane")

aval = ROOT.Garfield.AvalancheMicroscopic()
aval.SetSensor(sensor)

drift = ROOT.Garfield.DriftLineRKF()
drift.SetSensor(sensor)
drift.SetIntegrationAccuracy(1.0e-4)
drift.EnableAvalanche(True)

driftView = ROOT.Garfield.ViewDrift()
driftView.SetArea(xmin, 0., xmax, yHV)
drift.EnablePlotting(driftView)


xmin = -3 * period
xmax = 3 * period
sensor.SetArea(xmin, 0., -1., xmax, yHV, 1.)

field_canvas = ROOT.TCanvas(
    "field_canvas", "Electric field", 900, 700
)



field_view = ROOT.Garfield.ViewField()
ROOT.SetOwnership(field_view, False)

field_view.SetComponent(cmpe)
field_view.SetCanvas(field_canvas)

# Display one periodic cell and the relevant vertical region.
field_view.SetArea(
    -3 * period, 0.,
     3 * period, 2.2
)
'''
# "e" means electric-field magnitude.
field_view.PlotContour("e")

field_canvas.Update()
field_canvas.SaveAs("electric_field_contours.png")

'''

ne_list = []
for i in range(trials):
   
    x0 = -0.4
    y0 = 2.2
    z0 = 0.0

    
    sensor.EnableComponent(0, True)
    sensor.EnableComponent(1, False)

    x1 = ctypes.c_double(0.0)
    y1 = ctypes.c_double(0.0)
    z1 = ctypes.c_double(0.0)
    t1 = ctypes.c_double(0.0)
    status = ctypes.c_int(0)
    ne= ctypes.c_int()
    ni= ctypes.c_int()

    #drift.GetEndPoint(x1, y1, z1, t1, status)

    #print(f"Electron drift endpoint: x={x1.value:.3f}, y={y1.value:.3f}, z={z1.value:.3f}, time={t1.value:.3f}, status={status.value}")

    sensor.EnableComponent(1, False)
    sensor.EnableComponent(0, True)

    #ok = drift.DriftElectron(x0, y0, z0, 0.0)
    '''
    if ok:
        gain = drift.GetGain()
        ne_list.append(gain)
        print(gain)
    '''
    
    aval.AvalancheElectron(x0, y0, z0, 0.0, 0.07, 0., 0., 0.)
    aval.GetAvalancheSize(ne, ni)

    ne_list.append(ne.value)
    

write_csv(ne_list,directory, file_name)


# Plotting

#cellView plots geometry
cellView = ROOT.Garfield.ViewCell()
ROOT.SetOwnership(cellView, False)
cellView.SetComponent(cmpe)
cellView.SetArea(xmin, 0., xmax, 2.5)

#
canvas = ROOT.TCanvas("c1", "Geometry with Drift", 800, 600)
canvas.SetLeftMargin(0.15)   #
canvas.SetBottomMargin(0.15)  
canvas.SetRightMargin(0.05)  
canvas.SetTopMargin(0.05)    

hframe = ROOT.TH2F("hframe", "Geometry; x [cm]; y [cm]",
                   10, xmin, xmax,
                   10, 0., 2.0)
hframe.SetStats(0)
hframe.Draw("AXIS")


cellView.SetCanvas(canvas)
cellView.SetComponent(cmpe)
cellView.SetArea(xmin, 0., xmax, 2.5)
cellView.Plot2d()


driftView.SetArea(xmin, 0., xmax, 2.5)
driftView.SetCanvas(canvas)
driftView.Plot(True, False)


hframe.Draw("SAME AXIS")

canvas.Update()
canvas.SaveAs("geometry_with_drift.png")
