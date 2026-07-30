# --- Scan electric field along central hole axis ---

import numpy as np
import matplotlib.pyplot as plt
import ROOT 
import Garfield
import ctypes



pressure = 760. * 1.0

# Load the field map.
fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("2000/ELIST.lis", "2000/NLIST.lis", "2000/MPLIST.lis", "2000/PRNSOL.lis", "mm")
fm.EnableMirrorPeriodicityX()
fm.EnableMirrorPeriodicityY()


ROOT.gInterpreter.Declare(r"""
#include <cmath>
double field_mag(Garfield::ComponentAnsys123* fm, double x, double y, double z)
{
    double ex = 0., ey = 0., ez = 0., v = 0.;
    Garfield::Medium* m = nullptr;
    int status = 0;
    fm->ElectricField(x, y, z, ex, ey, ez, v, m, status);
    return std::sqrt(ex*ex + ey*ey + ez*ez);
}
""")

x0 = 0.0
y0 = 0.0

z_mm = np.linspace(-2.0, 5.0, 800)
z_cm = z_mm / 10.0
#zvals = np.linspace(-2.0, 5.0, 800)
Eabs = []

for z in z_cm:
    Eabs.append(ROOT.field_mag(fm, x0, y0, z))

plt.figure(figsize=(7, 4))
plt.plot(z_cm, Eabs, label='|E|')
plt.axvline(-0.2, linestyle=':', color='gray')
plt.axvline(0.2, linestyle=':', color='gray')
plt.xlabel('z [cm]')
plt.xlim(-0.1, 0.1)
plt.ylim(0,40000)
plt.ylabel('Electric field [V/cm]')
plt.title('Electric field along THGEM z-axis')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('axisfield.png', dpi=200)