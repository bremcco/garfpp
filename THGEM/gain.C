
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include <TCanvas.h>

#include "Garfield/AvalancheMC.hh"
#include "Garfield/AvalancheMicroscopic.hh"
#include "Garfield/ComponentAnsys123.hh"
#include "Garfield/MediumMagboltz.hh"
#include "Garfield/Random.hh"
#include "Garfield/Sensor.hh"
#include "Garfield/ViewDrift.hh"
#include "Garfield/ViewFEMesh.hh"
#include "Garfield/ViewField.hh"

using namespace Garfield;

void WriteCSV(const std::vector<int>& data,
              const std::string& directory,
              const std::string& filename) {

 
  const std::string command = "mkdir -p " + directory;
  std::system(command.c_str());

  const std::string filePath = directory + "/" + filename;

 
  std::ofstream csvFile(filePath, std::ios::app);

  if (!csvFile.is_open()) {
    std::cerr << "Error: Could not open output file: "
              << filePath << std::endl;
    return;
  }

  for (const int value : data) {
    csvFile << value << "\n";
  }

  csvFile.close();
}

int main() {

  const int trials = 1;

  const double pressure = 760. * 3.25685;

  const std::string fileName = "2110.csv";

  const std::string directory = "/afs/cern.ch/user/b/bmcconne/private/garfieldpp/thgem/2110";

  ComponentAnsys123 fm;

  fm.Initialise("thgem/2110/ELIST.lis","thgem/2110/NLIST.lis","thgem/2110/MPLIST.lis","thgem/2110/PRNSOL.lis","mm");

  fm.EnableMirrorPeriodicityX();
  fm.EnableMirrorPeriodicityY();

  fm.PrintRange();

  const double pitch = 0.8;

  MediumMagboltz gas("ar", 100.);

  gas.SetTemperature(293.15);
  gas.SetPressure(pressure);

  gas.Initialise(true);


  gas.EnablePenningTransfer();

  fm.SetGas(&gas);

  fm.PrintMaterials();

  Sensor sensor;

  sensor.AddComponent(&fm);

  sensor.SetArea(
      -2, -1, -0.2,
       2,  1,  2
  );

  AvalancheMicroscopic aval;

  aval.SetSensor(&sensor);


  AvalancheMC drift;

  drift.SetSensor(&sensor);
  drift.SetDistanceSteps(2.e-4);

  ViewDrift driftView;

  const bool plotDrift = true;

  if (plotDrift) {
    aval.EnablePlotting(&driftView);
    drift.EnablePlotting(&driftView);
  }

  std::vector<int> neList;
  neList.reserve(trials);

  for (int i = 0; i < trials; ++i) {

    const double x0 = -0.5 * pitch + RndmUniform() * pitch;

    const double y0 = -0.5 * pitch + RndmUniform() * pitch;

    const double z0 = 1.0;
    const double t0 = 0.0;
    const double e0 = 0.07;
    const double dx0 = 0.0;
    const double dy0 = 0.0;
    const double dz0 = 0.0;


    aval.AvalancheElectron(
        x0, y0, z0,
        t0, e0,
        dx0, dy0, dz0
    );

    int ne = 0;
    int ni = 0;

    aval.GetAvalancheSize(ne, ni);

    neList.push_back(ne);
  }

  WriteCSV(neList, directory, fileName);

  std::cout << std::endl
            << "Results written to: "
            << directory << "/" << fileName
            << std::endl;


  /*
  TCanvas* cD = new TCanvas("cD", "", 600, 600);

  ViewFEMesh meshView;

  meshView.SetComponent(&fm);

  const bool plotMesh = true;

  if (plotDrift) {

    if (plotMesh) {

      meshView.SetArea(
          -5 * pitch, -0.3,
           5 * pitch,  0.4
      );

      meshView.SetCanvas(cD);

      // x-z projection.
      meshView.SetPlane(
          0, -1, 0,
          0,  0, 0
      );

      meshView.SetFillMesh(true);

      // Set the colour of the Kapton.
      meshView.SetColor(2, kYellow + 3);

      meshView.EnableAxes();

      meshView.SetViewDrift(&driftView);

      meshView.Plot();

    } else {

      driftView.SetCanvas(cD);

      driftView.SetPlane(
          0, -1, 0,
          0,  0, 0
      );

      driftView.SetArea(
          -2 * pitch, -0.3,
           2 * pitch,  0.4
      );

      driftView.Plot(true);
    }
  }

  cD->Update();
  cD->SaveAs("avalanche_test.png");
  */

  return 0;
}

