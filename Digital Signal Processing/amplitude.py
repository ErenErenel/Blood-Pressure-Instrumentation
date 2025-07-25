import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load the pressure data
file_path = 'pressure_trimmed_ch2.csv'  # Replace with your actual file path
pressure_data = pd.read_csv(file_path)

# Extract time and pressure columns
time = pressure_data.iloc[:, 0]
pressure = pressure_data.iloc[:, 1]

# Calculate the sampling rate from time data
dt = np.mean(np.diff(time))
fs = 1 / dt

# Estimated heart rate
HR = 77.974  # bpm

# Compute minimum peak distance in samples
min_distance = int(fs * (0.7 * 60 / HR))
print(f"Calculated minimum distance between peaks/troughs (samples): {min_distance}")

# Find positive peaks
peaks, _ = find_peaks(pressure, distance=min_distance)
peaks = peaks[pressure[peaks] > 0]

# Find negative peaks (troughs)
troughs, _ = find_peaks(-pressure, distance=min_distance)
troughs = troughs[pressure[troughs] < -0.23]

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
amplitudes = pressure[matched_peaks].values - pressure[matched_troughs].values
oscillation_numbers = np.arange(1, len(amplitudes) + 1)

# Plotting
plt.figure(figsize=(12, 8))

# Subplot 1: Raw signal with peaks and troughs
plt.subplot(2, 1, 1)
plt.plot(time, pressure, label='Oscillation Pressure [mmHg]', color='blue')
plt.plot(time[matched_peaks], pressure[matched_peaks], 'r*', label='Peaks', markersize=8)
plt.plot(time[matched_troughs], pressure[matched_troughs], 'g*', label='Troughs (Before Peak)', markersize=8)
plt.title('Peaks and Preceding Troughs in Pressure Signal')
plt.xlabel('Time [s]')
plt.ylabel('Oscillation Pressure [mmHg]')
plt.legend()
plt.grid(True)

# Subplot 2: Amplitudes vs Oscillation Number
plt.subplot(2, 1, 2)
if len(amplitudes) > 0:
    plt.plot(oscillation_numbers, amplitudes, 'mo', label='Amplitude', markersize=6)
    y_pad = (np.max(amplitudes) - np.min(amplitudes)) * 0.2
    plt.ylim(np.min(amplitudes) - y_pad, np.max(amplitudes) + y_pad)
    plt.title('Amplitude (Peak - Preceding Trough)')
    plt.xlabel('Oscillation Number')
    plt.ylabel('Amplitude [mmHg]')
    plt.legend()
    plt.grid(True)
else:
    print("No amplitudes found — check peak/trough detection thresholds.")

plt.tight_layout()
plt.show()

# Time of the 14th positive peak
if len(matched_peaks) >= 14:
    idx_14th_peak = matched_peaks[13]  # 14th peak is at index 13
    time_14th_peak = time[idx_14th_peak]
    print(f"\nThe 14th positive peak occurs at index {idx_14th_peak}, which is at time = {time_14th_peak:.3f} seconds")
else:
    print("\nFewer than 14 peaks were found.")

# Summary
print(f"Number of matched peaks: {len(matched_peaks)}")
print(f"Number of matched troughs: {len(matched_troughs)}")
print(f"Calculated Amplitudes: {amplitudes}")
