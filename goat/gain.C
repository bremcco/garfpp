#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>

#include "Garfield/MediumMagboltz.hh"
#include "Garfield/ComponentAnalyticField.hh"
#include "Garfield/Sensor.hh"
#include "Garfield/AvalancheMicroscopic.hh"
#include "Garfield/DriftLineRKF.hh"
#include "Garfield/ViewDrift.hh"

namespace fs = std::filesystem;

void write_csv(const std::vector<int>& data,
               const std::string& directory,
               const std::string& filename) {

    fs::create_directories(directory);

    const std::string file_path = directory + "/" + filename;
    std::ofstream csvfile(file_path, std::ios::app);

    if (!csvfile.is_open()) {
        std::cerr << "Error: could not open "
                  << file_path << std::endl;
        return;
    }

    for (const auto& item : data) {
        csvfile << item << "\n";
    }

    csvfile.close();
}

int main() {

    const std::string directory =
        "/afs/cern.ch/user/b/bmcconne/private/garfieldpp/alice/goat_data/1";

    const std::string file_name = "1150.csv";

    const double pressure = 760.0 * 1.0;

    const int trials = 1;

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

    const double r_wire = 0.5 * ds;

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
    Garfield::ComponentAnalyticField cmpi;

    cmpe.SetMedium(&gas);
    cmpi.SetMedium(&gas);

    cmpe.SetPeriodicityX(period);
    cmpi.SetPeriodicityX(period);

    const double xs = 0.0;
    const double ys = gap;

    cmpe.AddWire(xs,ys,ds,vs);

    cmpi.AddWire(xs,ys,ds,vs);

    const double xc = 0.5 * period;
    const double yc = 2.0 * gap;

    cmpe.AddWire(xc,yc,dc,0.0);

    cmpi.AddWire(xc,yc,dc,0.0);

    const double xg1 = 0.25 * period;
    const double xg2 = 0.75 * period;
    const double yg = 2.0 * gap + 0.3;

    cmpe.AddWire(xg1,yg,dg,vg,"g",100.0,50.0,19.3,1);

    cmpe.AddWire(xg2,yg,dg,vg,"g",100.0,50.0,19.3,1);

    cmpi.AddWire(xg1,yg,dg,vg + deltav,"g+");

    cmpi.AddWire(xg2,yg,dg,vg - deltav,"g-");

    cmpe.AddPlaneY(0.0,0.0,"pad_plane");

    cmpi.AddPlaneY(0.0,0.0,"pad_plane");

    cmpe.AddPlaneY(yHV,vHV);

    cmpi.AddPlaneY(yHV,vHV);

    cmpe.SetMagneticField(0.0,0.5,0.0);

    cmpi.SetMagneticField(0.0,0.5,0.0);

    Garfield::Sensor sensor;

    sensor.AddComponent(&cmpe);
    sensor.AddComponent(&cmpi);

    sensor.AddElectrode(&cmpi,"pad_plane");

    Garfield::AvalancheMicroscopic aval;

    aval.SetSensor(&sensor);

    Garfield::DriftLineRKF drift;

    drift.SetSensor(&sensor);

    drift.SetIntegrationAccuracy(1.0e-4);

    drift.EnableAvalanche(true);

    Garfield::ViewDrift driftView;

    driftView.SetArea(xmin,0.0,xmax,yHV);

    drift.EnablePlotting(&driftView);

    sensor.SetArea(xmin,0.0,-1.0,xmax,yHV,1.0);

    std::vector<int> ne_list;

    ne_list.reserve(trials);

    for (int i = 0; i < trials; ++i) {

        const double x0 = -0.4;
        const double y0 =  2.2;
        const double z0 =  0.0;

        sensor.EnableComponent(0, true);
        sensor.EnableComponent(1, false);

        const double t0 = 0.0;
        const double e0 = 0.07;

        const double dx0 = 0.0;
        const double dy0 = 0.0;
        const double dz0 = 0.0;

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

        aval.GetAvalancheSize(ne,ni);
        ne_list.push_back(ne);
    }

    write_csv(
        ne_list,
        directory,
        file_name
    );
    
    return 0;
}