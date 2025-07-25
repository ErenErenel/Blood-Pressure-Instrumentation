import pandas as pd
import numpy as np
from scipy.signal import find_peaks

# Load CH2 to find time of 14th peak
ch2_data = pd.read_csv('pressure_trimmed_ch2.csv')
ch2_time = ch2_data.iloc[:, 0]
ch2_pressure = ch2_data.iloc[:, 1]

# Sampling setup
dt = np.mean(np.diff(ch2_time))
fs = 1 / dt
HR = 74
min_distance = int(fs * (0.7 * 60 / HR))

# Find positive peaks
peaks, _ = find_peaks(ch2_pressure, distance=min_distance)
peaks = peaks[ch2_pressure[peaks] > 0]

# Find troughs (local minima)
troughs, _ = find_peaks(-ch2_pressure, distance=min_distance)
troughs = troughs[ch2_pressure[troughs] < -0.23]

# Match each peak with the most recent trough before it
matched_peaks = []
matched_troughs = []
t_idx = 0

for p in peaks:
    while t_idx < len(troughs) and troughs[t_idx] < p:
        t_idx += 1
    if t_idx == 0:
        continue  # no prior trough
    matched_peaks.append(p)
    matched_troughs.append(troughs[t_idx - 1])

# Convert to numpy arrays
matched_peaks = np.array(matched_peaks)
matched_troughs = np.array(matched_troughs)

# Calculate amplitudes as peak - preceding trough
amplitudes = ch2_pressure[matched_peaks].values - ch2_pressure[matched_troughs].values

# Print results
print("\nOscillation Amplitudes:")
for i, amp in enumerate(amplitudes, start=1):
    print(f"Oscillation {i}: Amplitude = {amp:.2f} mmHg")

# Get 14th peak time
fourteenth_peak_time = ch2_time.iloc[matched_peaks[13]]
print(f"\n14th peak time = {fourteenth_peak_time:.3f} s")

# Load CH1 to get pressure at that time
ch1_data = pd.read_csv('pressure_trimmed_ch1.csv')
ch1_time = ch1_data.iloc[:, 0]
ch1_pressure = ch1_data.iloc[:, 1]

# Find closest index in CH1 to this time
idx = (np.abs(ch1_time - fourteenth_peak_time)).argmin()
map_pressure = ch1_pressure.iloc[idx]

# Output MAP
print(f"\nMAP occurs at index {idx}, time = {ch1_time.iloc[idx]:.3f} s")
print(f"Estimated Mean Arterial Pressure (MAP): {map_pressure:.2f} mmHg")
