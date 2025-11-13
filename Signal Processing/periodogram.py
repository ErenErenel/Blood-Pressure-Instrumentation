import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram

# Load the data
data = pd.read_csv("pressure_converted_ch1.csv")  # Change if your filename differs
time = data['time'].values
raw_signal = data['pressure_mmhg'].values  # Assuming 'pressure' is the column name

# Sampling parameters
dt = np.mean(np.diff(time))  # Time difference between samples
fs = 1 / dt  # Sampling frequency

# Calculate periodogram
frequencies, psd = periodogram(raw_signal, fs=fs)

# Find the peak frequency within the 0-3 Hz range
valid_range = (frequencies >= 0) & (frequencies <= 3)
peak_index = np.argmax(psd[valid_range])
peak_frequency = frequencies[valid_range][peak_index]

# Calculate the Heart Rate (HR) in BPM
HR = peak_frequency * 60

# Plot the periodogram
plt.figure(figsize=(12, 5))

# Plot 1: Full frequency range
plt.subplot(1, 2, 1)
plt.semilogy(frequencies, psd, color='orange')
plt.title("Periodogram (Full Range)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density")
plt.grid(True)

# Plot 2: Zoomed in to 0 – 3 Hz
plt.subplot(1, 2, 2)
plt.semilogy(frequencies, psd, color='green')
plt.title("Periodogram (Zoomed: 0–3 Hz)")
plt.xlabel("Frequency (Hz)")
plt.xlim(0, 3)
plt.axvline(x=peak_frequency, color='red', linestyle='--', label=f'Peak: {peak_frequency:.3f} Hz')

# Annotate the graph with the calculated HR
plt.legend()
plt.grid(True)

plt.suptitle("Untrimmed Unfiltered Data", fontsize=16)
plt.tight_layout()
plt.show()

print(f"Estimated Heart Rate (HR): {HR:.3f} BPM")
