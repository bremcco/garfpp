#include <ROOT/TApplication.h>
#include <TROOT.h>

#include <Garfield/AvalancheMC.hh>
#include <Garfield/AvalancheMicroscopic.hh>
#include <Garfield/ComponentAnsys123.hh>
#include <Garfield/FundamentalConstants.hh>
#include <Garfield/MediumMagboltz.hh>
#include <Garfield/Random.hh>
#include <Garfield/Sensor.hh>
#include <Garfield/ViewDrift.hh>
#include <Garfield/ViewFEMesh.hh>
#include <Garfield/ViewField.hh>

#include <ctypes.h>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace Garfield;

namespace {

void WriteCsv(const std::vector<int>& data, const std::string& directory,
              const std::string& filename) {
  std::filesystem::create_directories(directory);
  const std::filesystem::path filePath = std::filesystem::path(directory) / filename;

  std::ofstream out(filePath, std::ios::app);
  if (!out.is_open()) {
    throw std::runtime_error("Unable to open output CSV: " + filePath.string());
  }
  for (const int value : data) {
    out << value << '\n';
  }
}

}  // namespace

int main(int argc, char* argv[]) {
  TApplication app("app", &argc, argv);

  const int trials = 1;
  const double pressure = 760.0;
  const std::string fileName = "arch4955.csv";
  const std::string directory =
      "/afs/cern.ch/user/b/bmcconne/private/garfieldpp/gorg/3150_test";

  // Load the field map.
  auto* fm = new ComponentAnsys123();
  fm->Initialise("3150/ELIST.lis", "3150/NLIST.lis", "3150/MPLIST.lis",
                 "3150/PRNSOL.lis", "micron");
  fm->EnableMirrorPeriodicityX();
  fm->EnableMirrorPeriodicityY();
  fm->PrintRange();

  // GEM pitch in cm.
  const double pitch = 0.014;

  // Setup the gas.
  MediumMagboltz gas("ar", 95., "ch4", 5.);
  gas.SetTemperature(293.15);
  gas.SetPressure(pressure);
  gas.Initialise(true);
  gas.EnablePenningTransfer();
  gas.LoadIonMobility(
      "/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt");

  fm->SetGas(&gas);
  fm->PrintMaterials();

  // Assemble the sensor.
  Sensor sensor;
  sensor.AddComponent(fm);
  sensor.SetArea(-2., -1., -2., 2., 1., 0.5);

  AvalancheMicroscopic aval;
  aval.SetSensor(&sensor);

  AvalancheMC drift;
  drift.SetSensor(&sensor);
  drift.SetDistanceSteps(2.e-4);

  ViewDrift driftView;
  const bool plotDrift = false;
  if (plotDrift) {
    aval.EnablePlotting(&driftView);
    drift.EnablePlotting(&driftView);
  }

  std::vector<int> neList;
  neList.reserve(trials);

  for (int i = 0; i < trials; ++i) {
    const double x0 = -0.5 * pitch + RndmUniform() * pitch;
    const double y0 = -0.5 * pitch + RndmUniform() * pitch;
    const double z0 = -0.3;
    const double t0 = 0.0;
    const double e0 = 0.07;

    aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.);

    int ne = 0;
    int ni = 0;
    aval.GetAvalancheSize(ne, ni);
    neList.push_back(ne);

    std::cout << "Trial " << (i + 1) << "/" << trials << ": " << ne
              << " electrons\n";
  }

  WriteCsv(neList, directory, fileName);

  delete fm;
  return 0;
}
