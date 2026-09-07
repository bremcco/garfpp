#include <iostream>

#include "Garfield/MediumMagboltz.hh"
#include "Garfield/ComponentAnalyticField.hh"
#include "Garfield/ViewField.hh"

#include <TCanvas.h>

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

    const double yHV = 249.7;
    const double vHV = -400.0;

    const double xmin = -3.0 * period;
    const double xmax =  3.0 * period;

    Garfield::MediumMagboltz gas("ar", 90.0, "co2", 10.0);

    gas.SetTemperature(293.15);
    gas.SetPressure(pressure);
    gas.EnablePenningTransfer();
    gas.LoadIonMobility("IonMobility_Ar+_Ar.txt");

    Garfield::ComponentAnalyticField field;

    field.SetMedium(&gas);
    field.SetPeriodicityX(period);

    const double xs = 0.0;
    const double ys = gap;

    field.AddWire(xs, ys, ds, vs);

    const double xc = 0.5 * period;
    const double yc = 2.0 * gap;

    field.AddWire(xc, yc, dc, 0.0);

    const double xg1 = 0.25 * period;
    const double xg2 = 0.75 * period;
    const double yg = 2.0 * gap + 0.3;

    field.AddWire(
        xg1, yg, dg, vg,
        "g", 100.0, 50.0, 19.3, 1
    );

    field.AddWire(
        xg2, yg, dg, vg,
        "g", 100.0, 50.0, 19.3, 1
    );

    field.AddPlaneY(
        0.0, 0.0, "pad_plane"
    );

    field.AddPlaneY(
        yHV, vHV
    );

    field.SetMagneticField(
        0.0, 0.5, 0.0
    );

    TCanvas canvas(
        "c1",
        "Electric Field",
        900,
        700
    );

    Garfield::ViewField view;

    view.SetComponent(&field);
    view.SetCanvas(&canvas);

    view.SetArea(
        xmin,
        0.0,
        xmax,
        2.2
    );

    view.PlotContour("e");

    canvas.Update();

    canvas.SaveAs("electric_field_contours.png");

    std::cout << "Saved electric field plot to "
              << "electric_field_contours.png"
              << std::endl;

    return 0;
}