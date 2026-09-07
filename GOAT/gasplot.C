#include <TApplication.h>
#include <TCanvas.h>

#include "Garfield/MediumMagboltz.hh"
#include "Garfield/ViewMedium.hh"

using namespace Garfield;

int main(int argc, char* argv[]) {
  TApplication app("app", &argc, argv);

  MediumMagboltz gas;
  gas.LoadGasFile("GOAT_ar_90_co2_10_8atm_0p5T.gas");
  std::vector<double> efields;
  std::vector<double> bfields;
  std::vector<double> angles;
  gas.GetFieldGrid(efields, bfields, angles);

  Garfield::ViewMedium view;
  view.SetMedium(&gas);
  view.SetMagneticField(0.5);


  TCanvas c1("c1", "", 800, 600);
  view.SetCanvas(&c1);
  if (!angles.empty()) view.SetAngle(angles[1]);
  
  view.EnableAutoRangeX(false);
  // Plot only the low-field part
  view.SetRangeE(0., 1000., false);
  view.PlotElectronVelocity('e');

  // Plot the velocity as function of angle between E and B,
  // at E = 400 V / cm.
  TCanvas c2("c2", "", 800, 600);
  view.SetCanvas(&c2);
  view.SetElectricField(400.);
  view.SetRangeA(0., HalfPi, false);
  view.PlotElectronVelocity('a');

  app.Run();
}
