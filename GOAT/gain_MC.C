#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "Garfield/MediumMagboltz.hh"
#include "Garfield/ComponentAnalyticField.hh"
#include "Garfield/Sensor.hh"
#include "Garfield/AvalancheMC.hh"

void write_csv(const std::vector<int>& data, const std::string& file_path) {
    std::ofstream csvfile(file_path, std::ios::app);
    if (!csvfile.is_open()) {
        std::cerr << "Error: could not open " << file_path << std::endl;
        return;
    }
    for (const auto& item : data) csvfile << item << "\n";
}

int main(int argc, char** argv) {

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <job_index> [trials]" << std::endl;
        return 1;
    }

    const std::string jobIdx = argv[1];
    const int trials = (argc > 2) ? std::stoi(argv[2]) : 1;

    // HTCONDOR WRITING DIRECTORY TEST
    const std::string file_name = "result_" + jobIdx + ".csv";

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

    // MUST CHANGE GAS FILE TO CORRECT PRESSURE VALUE
    Garfield::MediumMagboltz gas;
    gas.LoadGasFile("GOAT_ar_90_co2_10_1atm_0p5T.gas");
    gas.EnablePenningTransfer();
    gas.LoadIonMobility("IonMobility_Ar+_Ar.txt");

    Garfield::ComponentAnalyticField cmpe;
    Garfield::ComponentAnalyticField cmpi;

    cmpe.SetMedium(&gas);
    cmpi.SetMedium(&gas);

    cmpe.SetPeriodicityX(period);
    cmpi.SetPeriodicityX(period);

    const double xs = 0.0;
    const double ys = gap;

    cmpe.AddWire(xs, ys, ds, vs);
    cmpi.AddWire(xs, ys, ds, vs);

    const double xc = 0.5 * period;
    const double yc = 2.0 * gap;

    cmpe.AddWire(xc, yc, dc, 0.0);
    cmpi.AddWire(xc, yc, dc, 0.0);

    const double xg1 = 0.25 * period;
    const double xg2 = 0.75 * period;
    const double yg = 2.0 * gap + 0.3;

    cmpe.AddWire(xg1, yg, dg, vg, "g", 100.0, 50.0, 19.3, 1);
    cmpe.AddWire(xg2, yg, dg, vg, "g", 100.0, 50.0, 19.3, 1);

    cmpi.AddWire(xg1, yg, dg, vg + deltav, "g+");
    cmpi.AddWire(xg2, yg, dg, vg - deltav, "g-");

    cmpe.AddPlaneY(0.0, 0.0, "pad_plane");
    cmpi.AddPlaneY(0.0, 0.0, "pad_plane");

    cmpe.AddPlaneY(yHV, vHV);
    cmpi.AddPlaneY(yHV, vHV);

    cmpe.SetMagneticField(0.0, 0.5, 0.0);
    cmpi.SetMagneticField(0.0, 0.5, 0.0);

    Garfield::Sensor sensor;

    sensor.AddComponent(&cmpe);
    sensor.AddComponent(&cmpi);

    sensor.AddElectrode(&cmpi, "pad_plane");

    sensor.SetArea(xmin, 0.0, -1.0, xmax, yHV, 1.0);

    Garfield::AvalancheMC aval;
    aval.SetSensor(&sensor);
    aval.SetCollisionSteps(100);
    aval.EnableAvalancheSizeLimit(200000);

    std::vector<int> ne_list;
    ne_list.reserve(trials);

    for (int i = 0; i < trials; ++i) {

        sensor.EnableComponent(0, true);
        sensor.EnableComponent(1, false);

        const double x0 = -0.4;
        const double y0 =  2.2;
        const double z0 =  0.0;
        const double t0 =  0.0;

        aval.AvalancheElectron(x0, y0, z0, t0);

        unsigned int ne = 0;
        unsigned int ni = 0;
        aval.GetAvalancheSize(ne, ni);
        ne_list.push_back(ne);
    }

    write_csv(ne_list, file_name);

    return 0;
}
