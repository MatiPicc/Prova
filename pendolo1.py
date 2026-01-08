import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

def fit_function(x, a, b):
  return a * x + b
data_x = [1.1449, 1.2769, 1.44, 1.5625, 1.69]
sigma_x = [0.0016, 0.0009, 0.0025, 0.0009, 0.0004]
data_y = [25.4, 31.1, 34.5, 37.8, 41.3]
sigma_y = [0.1, 0.1, 0.1, 0.1, 0.1]
plt.grid()
sigma_x = np.array(sigma_x)
sigma_y = np.array(sigma_y)
popt, pcov = curve_fit(fit_function, data_x, data_y, sigma=sigma_y, p0 = [0, 1])
print(f'a = {popt[0]:.2f} +\- {np.sqrt(pcov[0,0]):.2f}')
print(f'b = {popt[1]:.2f} +\- {np.sqrt(pcov[1,1]):.2f}')
x = np.linspace(0, 100)
plt.errorbar(data_x, data_y, sigma_y, fmt = '.', label = 'data', color= 'black')
plt.plot(x, fit_function(x, *popt), color = 'blue', label = 'fit')
plt.xlabel('T^2 (s^2)')
plt.ylabel('L (cm)')
#plt.title('Periodo del pendolo al variare della lunghezza', fontsize = 14)
plt.xlim(1, 2) # Imposta i limiti dell’asse x
plt.ylim(25, 42) # Imposta i limiti dell’asse y
plt.minorticks_on()
plt.legend()
plt.show()