import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

E_vals = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]  # V/cm

alpha_vals = [9.357623098352714e-14, 9.357623098352714e-14, 9.357623098352714e-14, 9.357623098352714e-14, 9.357623098352714e-14, 9.357623098352714e-14, 9.357623098352714e-14, 0.021387334324600406, 0.11265710009635757, 0.168261785365819]
#alpha_vals = [9.357623280265388e-14, 9.357623280265388e-14, 9.357623280265388e-14, 0.02673767748021008, 0.11309983816989941, 0.4626395458786055, 1.0947271928521327, 2.556662132599587, 4.537704390343901, 7.251830453034106]
pressure = 760.0  # Torr


E = np.array(E_vals)       # V/cm
alpha = np.array(alpha_vals)  # 1/cm
P = pressure            

def alpha_model(E, A, B):
    return A * np.exp(-B * P / E)

A_guess = max(alpha)     # Roughly correct magnitude
B_guess = 100            # Reasonable typical E/P slope

popt, pcov = curve_fit(alpha_model, E, alpha, p0=[A_guess, B_guess])

A_fit, B_fit = popt

print("A =", A_fit)
print("B =", B_fit)

#plotting

E_plot = np.linspace(min(E_vals)*0.9, max(E_vals)*1.1, 500)
alpha_fit = alpha_model(E_plot, A_fit, B_fit)

plt.figure(figsize=(8,6))
plt.plot(E_vals, alpha_vals, 'o', label='Magboltz data', markersize=6)
plt.plot(E_plot, alpha_fit, '-', label=f'Fit: A={A_fit:.3f}, B={B_fit:.1f}', linewidth=2)
plt.xlabel('Electric field E [V/cm]')
plt.ylabel('Townsend coefficient α [1/cm]')
plt.title(f'Townsend fit at P={P} atm')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('towns_fit2atm.png')
