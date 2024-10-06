 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from obspy import read
from obspy.signal.invsim import cosine_taper
from obspy.signal.filter import highpass
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
from scipy import signal
from matplotlib import cm

# Set directories
cat_directory = 'backend\\data\\lunar\\training\\catalogs\\'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
cat = pd.read_csv(cat_file)


print("Contents of the catalog:")
print(cat)
print("\n")

# Ask for user input
while True:
    try:
        row_index = int(input("Enter the row number you want to select (0 to {}): ".format(len(cat) - 1)))
        if 0 <= row_index < len(cat):
            break
        else:
            print("Please enter a valid row number.")
    except ValueError:
        print("Please enter a valid integer.")

# Select a detection
row = cat.iloc[row_index]

# Get arrival time in absolute and relative formats
arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')
arrival_time_rel = row['time_rel(sec)']

print(f"Arrival time (absolute): {arrival_time}")
print(f"Arrival time (relative): {arrival_time_rel}")

# Get the filename
test_filename = row.filename
print(f"Selected filename: {test_filename}")

# Read the CSV file
data_directory = 'backend\\data\\lunar\\training\\data\\S12_GradeA\\'
csv_file = f'{data_directory}{test_filename}.csv'
print(f"Full data file path being used: {csv_file}")
data_cat = pd.read_csv(csv_file)

print("Contents of the data file:")
print(data_cat)

# Read in time steps and velocities
csv_times = np.array(data_cat['time_rel(sec)'].tolist())
csv_data = np.array(data_cat['velocity(m/s)'].tolist())

# Implement flattening algorithm
def flatten_data(times, data, window_size=1000):
    flattened_data = np.zeros_like(data)
    for i in range(len(data)):
        start = max(0, i - window_size // 2)
        end = min(len(data), i + window_size // 2)
        window_mean = np.mean(data[start:end])
        flattened_data[i] = data[i] - window_mean
    return flattened_data

flattened_csv_data = flatten_data(csv_times, csv_data)

# Set the minimum frequency
minfreq = 0.5
maxfreq = 1.0
# Going to create a separate trace for the filter data
data_directory = 'backend\\data\\lunar\\training\\data\\S12_GradeA\\'
mseed_file = f'{data_directory}{test_filename}.mseed'
st = read(mseed_file)

st_filt = st.copy()
st_filt.filter('bandpass',freqmin=minfreq,freqmax=maxfreq)
tr_filt = st_filt.traces[0].copy()
tr_times_filt = tr_filt.times()
tr_data_filt = tr_filt.data

f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)
tr = st.traces[0].copy()
tr_times = tr.times()
tr_data = tr.data
df = tr.stats.sampling_rate
# How long should the short-term and long-term window be, in seconds?
sta_len = 120
lta_len = 600
# Run Obspy's STA/LTA to obtain a characteristic function
# This function basically calculates the ratio of amplitude between the␣
# and long-term windows, moving consecutively in time across the data
cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))
# Play around with the on and off triggers, based on values in the␣
thr_on = 4
thr_off = 1.5
on_off = np.array(trigger_onset(cft, thr_on, thr_off))
# The first column contains the indices where the trigger is turned "on"

# Plot characteristic function
fig, ax = plt.subplots(1, 1, figsize=(10, 3))

# File name and start time of trace
fname = row.filename
starttime = tr.stats.starttime.datetime
# Iterate through detection times and compile them
detection_times = []
fnames = []
for i in np.arange(0,len(on_off)):
    triggers = on_off[i]
    on_time = starttime + timedelta(seconds = tr_times[triggers[0]])
    on_time_str = datetime.strftime(on_time,'%Y-%m-%dT%H:%M:%S.%f')
    detection_times.append(on_time_str)
    fnames.append(fname)
# Compile dataframe of detections
detect_df = pd.DataFrame(data = {'filename':fnames, 'time_abs(%Y-%m-%dT%H:%M:%S.%f)':detection_times, 'time_rel(sec)':tr_times[triggers[0]]})
detect_df.head()

# First subplot: filtered seismogram
ax1 = plt.subplot(2, 1, 1)
ax1.plot(tr_times_filt, tr_data_filt)
ax1.set_xlim([min(tr_times_filt), max(tr_times_filt)])
ax1.set_ylabel('Velocity (m/s)')
ax1.set_xlabel('Time (s)')
ax1.legend(loc='upper left')

# Plot where the arrival time is
arrival_line = ax1.axvline(x=arrival_time_rel, c='red', label='Rel. Arrival')
ax1.legend(handles=[arrival_line])

# Second subplot: spectrogram
ax2 = plt.subplot(2, 1, 2)
vals = ax2.pcolormesh(t, f, sxx, cmap=cm.jet, vmax=5e-17)
ax2.set_xlim([min(tr_times_filt), max(tr_times_filt)])
ax2.set_xlabel(f'Time (Day Hour:Minute)', fontweight='bold')
ax2.set_ylabel('Frequency (Hz)', fontweight='bold')
cbar = plt.colorbar(vals, orientation='horizontal')
cbar.set_label('Power ((m/s)^2/sqrt(Hz))', fontweight='bold')

# Display the plot
plt.tight_layout()

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