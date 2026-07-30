import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# -------------------------------
# 1. INPUT PARAMETERS FOR BOTH FITS
# -------------------------------

# Fit 1
A1, B1 = 505.815, 55.8      # example values
P1 = 760                # Torr
# Fit 2
A2, B2 = 79.944, 80.5      # example values
P2 = 760*2                # Torr

# Define E range for plotting (choose a range covering both fits)
E_plot = np.linspace(1, 1000000, 1000)  # V/cm

# -------------------------------
# 2. DEFINE THE FIT FUNCTIONS
# -------------------------------
def alpha1(E):
    return A1 * np.exp(-B1 * P1 / E)

def alpha2(E):
    return A2 * np.exp(-B2 * P2 / E)



# Generate a dense E array
E_plot = np.linspace(1, 1000000, 100000)  # adjust range if needed
alpha2_vals = alpha2(E_plot)

# Target alpha
alpha_target = 330.990935

# Find index of closest value
idx = np.argmin(np.abs(alpha2_vals - alpha_target))
E_closest = E_plot[idx]
alpha_closest = alpha2_vals[idx]

print(f"Closest match to alpha = {alpha_target}:")
print(f"E = {E_closest:.6f} V/cm, alpha = {alpha_closest:.6f} 1/cm")


# -------------------------------
# 4. PLOT
# -------------------------------
plt.figure(figsize=(8,6))
plt.plot(E_plot, alpha1(E_plot), '-', label='Fit 1', linewidth=2)
plt.plot(E_plot, alpha2(E_plot), '-', label='Fit 2', linewidth=2)


plt.xlabel('Electric field E [V/cm]')
plt.ylabel('Townsend coefficient α [1/cm]')
#plt.xscale('log')
#plt.xlim(1, 1e6)
#plt.yscale('log')
plt.title('Townsend Coefficient Fits for Ar-CH4 92-8')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('towns_fit_overlap.png')