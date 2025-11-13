import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load the pressure data
file_path = 'pressure_trimmed_ch2.csv'  # Replace with your file path
pressure_data = pd.read_csv(file_path)

# Extract time and pressure columns (assuming first column is time, second is pressure)
time = pressure_data.iloc[:, 0]
pressure = pressure_data.iloc[:, 1]

# Calculate the sampling rate from the time data
dt = np.mean(np.diff(time))  # Time difference between samples
fs = 1 / dt  # Sampling frequency

# Define approximate heart rate (bpm) - update based on your periodogram analysis
HR = 77.974  # Example: estimated from periodogram

# Calculate minimum distance between peaks in samples
min_distance = int(fs * (0.6 * 60 / HR))
print(f"Calculated minimum distance between troughs (samples): {min_distance}")

# Find troughs (negative peaks) by inverting the signal
troughs, _ = find_peaks(-pressure, distance=min_distance)

# Filter troughs with values below -0.023
filtered_troughs = [t for t in troughs if pressure[t] < -0.24]

# Plot the data with identified troughs
plt.figure(figsize=(10, 6))
plt.plot(time, pressure, label='Oscillation Pressure [mmHg]', color='blue')
plt.plot(time[filtered_troughs], pressure[filtered_troughs], 'g*', label='Filtered Troughs', markersize=6)  # Green stars for troughs

plt.title('Identified Troughs in Pressure Signal')
plt.xlabel('Time [s]')
plt.ylabel('Oscillation Pressure [mmHg]')
plt.legend()
plt.grid(True)

print(f"Number of filtered troughs found: {len(filtered_troughs)}")
plt.show()
