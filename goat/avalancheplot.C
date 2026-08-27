#include <iostream>

#include <TCanvas.h>
#include <TH2F.h>

#include "Garfield/MediumMagboltz.hh"
#include "Garfield/ComponentAnalyticField.hh"
#include "Garfield/Sensor.hh"
#include "Garfield/AvalancheMicroscopic.hh"
#include "Garfield/ViewDrift.hh"
#include "Garfield/ViewCell.hh"


int main() {
    
    const double pressure = 760.0;

    const bool iroc = true;

    const double gap = iroc ? 0.2 : 0.3;

    const double period = 0.25;

    const double ds = 0.0020;
    const double dc = 0.0075;
    const double dg = 0.0075;

    const double vs = 1150.0;
    const double vg = -125.0;

    const double deltav = 90.0;

    const double yHV = 249.7;
    const double vHV = -400.0;

    const double xmin = -3.0 * period;
    const double xmax =  3.0 * period;

    Garfield::MediumMagboltz gas(
        "ar", 90.0,
        "co2", 10.0
    );

    gas.SetTemperature(293.15);
    gas.SetPressure(pressure);

    gas.EnablePenningTransfer();

    gas.LoadIonMobility(
        "IonMobility_Ar+_Ar.txt"
    );

    Garfield::ComponentAnalyticField cmpe;

    cmpe.SetMedium(&gas);
    cmpe.SetPeriodicityX(period);

    const double xs = 0.0;
    const double ys = gap;

    cmpe.AddWire(
        xs,
        ys,
        ds,
        vs
    );

    const double xc = 0.5 * period;
    const double yc = 2.0 * gap;

    cmpe.AddWire(
        xc,
        yc,
        dc,
        0.0
    );

    const double xg1 = 0.25 * period;
    const double xg2 = 0.75 * period;
    const double yg = 2.0 * gap + 0.3;

    cmpe.AddWire(
        xg1,
        yg,
        dg,
        vg,
        "g",
        100.0,
        50.0,
        19.3,
        1
    );

    cmpe.AddWire(
        xg2,
        yg,
        dg,
        vg,
        "g",
        100.0,
        50.0,
        19.3,
        1
    );

    cmpe.AddPlaneY(
        0.0,
        0.0,
        "pad_plane"
    );

    cmpe.AddPlaneY(
        yHV,
        vHV
    );

    cmpe.SetMagneticField(
        0.0,
        0.5,
        0.0
    );

    Garfield::Sensor sensor;

    sensor.AddComponent(&cmpe);

    sensor.SetArea(
        xmin,
        0.0,
        -1.0,
        xmax,
        yHV,
        1.0
    );

    Garfield::AvalancheMicroscopic aval;

    aval.SetSensor(&sensor);

    Garfield::ViewDrift driftView;

    driftView.SetArea(
        xmin,
        0.0,
        xmax,
        2.5
    );

   
    aval.EnablePlotting(
        &driftView,
        1
    );

    Garfield::ViewCell cellView;

    cellView.SetComponent(&cmpe);

    cellView.SetArea(
        xmin,
        0.0,
        xmax,
        2.5
    );

    TCanvas canvas(
        "c1",
        "Avalanche with Geometry",
        900,
        700
    );

    canvas.SetLeftMargin(0.12);
    canvas.SetBottomMargin(0.12);
    canvas.SetRightMargin(0.05);
    canvas.SetTopMargin(0.05);

    TH2F hframe(
        "hframe",
        "Avalanche; x [cm]; y [cm]",
        10,
        xmin,
        xmax,
        10,
        0.0,
        2.5
    );

    hframe.SetStats(0);

    hframe.Draw("AXIS");

    const double x0 = -0.4;
    const double y0 =  2.2;
    const double z0 =  0.0;

    const double t0 = 0.0;
    const double e0 = 0.07;

    const double dx0 = 0.0;
    const double dy0 = 0.0;
    const double dz0 = 0.0;


    sensor.EnableComponent(0, true);


    aval.AvalancheElectron(
        x0,
        y0,
        z0,
        t0,
        e0,
        dx0,
        dy0,
        dz0
    );

    int ne = 0;
    int ni = 0;

    aval.GetAvalancheSize(
        ne,
        ni
    );

    std::cout << "Avalanche:" << std::endl;
    std::cout << "  electrons = " << ne << std::endl;
    std::cout << "  ions      = " << ni << std::endl;
    cellView.SetCanvas(&canvas);

    cellView.Plot2d();
    driftView.SetCanvas(&canvas);

    driftView.Plot2d(
        false,
        false
    );

    hframe.Draw("SAME AXIS");

    canvas.Update();

    canvas.SaveAs(
        "avalanche_with_geometry.png"
    );

    std::cout
        << "Saved plot to avalanche_with_geometry.png"
        << std::endl;


    return 0;
}