#include "Garfield/FundamentalConstants.hh"
#include "Garfield/MediumMagboltz.hh"

using namespace Garfield;

int main(int argc, char* argv[]) {
  const double pressure = AtmosphericPressure;
  const double temperature = 293.15;

  
  MediumMagboltz gas("Ar", 90., "CO2", 10.);
  gas.SetTemperature(temperature);
  gas.SetPressure(pressure);

  
  const size_t nE = 50;
  const double emin = 0.;
  const double emax = 200000.;

  const size_t nB = 1;
  const double bmin = 0.5;
  const double bmax = 0.5;

  const size_t nA = 10;
  const double amin = 0.;
  const double amax = HalfPi;
  
  constexpr bool useLog = true;
  gas.SetFieldGrid(
      emin, emax, nE, useLog,
      bmin, bmax, nB,
      amin, amax, nA);

  const int ncoll = 10;
  
  gas.GenerateGasTable(ncoll);
  
  gas.WriteGasFile("GOAT_ar_90_co2_10_1atm_0p5T.gas");
}
