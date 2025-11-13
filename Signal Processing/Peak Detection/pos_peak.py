import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load the pressure data
file_path = 'pressure_trimmed_ch2.csv'  # Replace with your file path
pressure_data = pd.read_csv(file_path)

# Extract time and pressure columns
time = pressure_data.iloc[:, 0]
pressure = pressure_data.iloc[:, 1]

# Calculate the sampling rate
dt = np.mean(np.diff(time))
fs = 1 / dt

# Approximate heart rate (from periodogram or estimate)
HR = 77.974  # bpm

# Minimum distance between peaks in samples
min_distance = int(fs * (0.6 * 60 / HR))
print(f"Calculated minimum distance between peaks (samples): {min_distance}")

# Find positive peaks
peaks, _ = find_peaks(pressure, distance=min_distance)

# Filter peaks above a certain threshold
filtered_peaks = [p for p in peaks if pressure[p] > -0.05]  # Adjust threshold as needed

# Plot the pressure signal with filtered peaks
plt.figure(figsize=(10, 6))
plt.plot(time, pressure, label='Oscillation Pressure [mmHg]', color='blue')
plt.plot(time[filtered_peaks], pressure[filtered_peaks], 'r*', label='Filtered Peaks', markersize=6)

plt.title('Identified Peaks in Pressure Signal')
plt.xlabel('Time [s]')
plt.ylabel('Oscillation Pressure [mmHg]')
plt.legend()
plt.grid(True)

print(f"Number of filtered peaks found: {len(filtered_peaks)}")
plt.show()
