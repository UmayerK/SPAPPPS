import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Set directories
cat_directory = './data/lunar/training/catalogs/'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
cat = pd.read_csv(cat_file)

print("Contents of the catalog:")
print(cat)
print("\n")

# Select a detection
row = cat.iloc[1]

# Get arrival time in absolute and relative formats
arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')
arrival_time_rel = row['time_rel(sec)']

print(f"Arrival time (absolute): {arrival_time}")
print(f"Arrival time (relative): {arrival_time_rel}")

# Get the filename
test_filename = row.filename
print(f"Selected filename: {test_filename}")

# Read the CSV file
data_directory = './data/lunar/training/data/S12_GradeA/'
csv_file = f'{data_directory}{test_filename}.csv'
print(f"Full data file path being used: {csv_file}")
data_cat = pd.read_csv(csv_file)

print("Contents of the data file:")
print(data_cat)

# Read in time steps and velocities
csv_times = np.array(data_cat['time_rel(sec)'].tolist())
csv_data = np.array(data_cat['velocity(m/s)'].tolist())

# Plot the trace
fig, ax = plt.subplots(1, 1, figsize=(10, 3))
ax.plot(csv_times, csv_data)

# Make the plot pretty
ax.set_xlim([min(csv_times), max(csv_times)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')
ax.set_title(f'{test_filename}', fontweight='bold')

# Plot where the arrival time is
arrival_line = ax.axvline(x=arrival_time_rel, c='red', label='Rel. Arrival')
ax.legend(handles=[arrival_line])

# Adjust layout to prevent cutting off labels
plt.tight_layout()

# Get the current working directory (assumed to be the project root)
project_root = os.getcwd()

# Create 'stuff' directory in the project root if it doesn't exist
stuff_dir = os.path.join(project_root, 'stuff')
if not os.path.exists(stuff_dir):
    os.makedirs(stuff_dir)

# Save the plot as PNG in the 'stuff' folder
plot_path = os.path.join(stuff_dir, 'lunar_seismic_event_plot.png')
plt.savefig(plot_path)

print(f"Plot saved as '{plot_path}'")

# Display the plot (optional, comment out if running in a non-interactive environment)
plt.show()