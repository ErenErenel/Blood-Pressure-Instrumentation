import matplotlib.pyplot as plt
import numpy as np

# Load converted pressure data for Channel 1
data_ch1 = np.loadtxt("pressure_converted_ch1.csv", delimiter=",", skiprows=1)
t_ch1 = data_ch1[:, 0]
pressure_mmhg_ch1 = data_ch1[:, 1]

# Load converted pressure data for Channel 2
data_ch2 = np.loadtxt("pressure_converted_ch2.csv", delimiter=",", skiprows=1)
t_ch2 = data_ch2[:, 0]
pressure_mmhg_ch2 = data_ch2[:, 1]

# Define trimming time range
start_time = 30
end_time = 60

# Trim data for Channel 1
trim_indices_ch1 = (t_ch1 >= start_time) & (t_ch1 <= end_time)
trimmed_t_ch1 = t_ch1[trim_indices_ch1]
trimmed_pressure_ch1 = pressure_mmhg_ch1[trim_indices_ch1]

# Trim data for Channel 2
trim_indices_ch2 = (t_ch2 >= start_time) & (t_ch2 <= end_time)
trimmed_t_ch2 = t_ch2[trim_indices_ch2]
trimmed_pressure_ch2 = pressure_mmhg_ch2[trim_indices_ch2]

# Save trimmed data for Channel 1
trimmed_signal_ch1 = np.column_stack((trimmed_t_ch1, trimmed_pressure_ch1))
np.savetxt("pressure_trimmed_ch1.csv", trimmed_signal_ch1, delimiter=",", header="time,pressure_mmhg", comments='')

# Save trimmed data for Channel 2
trimmed_signal_ch2 = np.column_stack((trimmed_t_ch2, trimmed_pressure_ch2))
np.savetxt("pressure_trimmed_ch2.csv", trimmed_signal_ch2, delimiter=",", header="time,pressure_mmhg", comments='')

# Plot for Channel 1 (Trimmed Only)
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)  # Separate graph for Channel 1
plt.plot(trimmed_t_ch1, trimmed_pressure_ch1, label="Trimmed Pressure Signal (Ch1) - mmHg", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (mmHg)")
plt.title("Trimmed Pressure Signal - Channel 1")
plt.legend()
plt.grid(True)

# Plot for Channel 2 (Trimmed Only)
plt.subplot(2, 1, 2)  # Separate graph for Channel 2
plt.plot(trimmed_t_ch2, trimmed_pressure_ch2, label="Trimmed Pressure Signal (Ch2) - mmHg", color="red")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (mmHg)")
plt.title("Trimmed Pressure Signal - Channel 2")
plt.legend()
plt.grid(True)

# Show the plots
plt.tight_layout()
plt.show()

print("Trimming and plotting complete. Saved trimmed data to 'pressure_trimmed_ch1.csv' and 'pressure_trimmed_ch2.csv'.")
