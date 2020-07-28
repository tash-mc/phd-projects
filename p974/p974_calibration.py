import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
from PySide2 import QtCore, QtWidgets, QtGui
import matplotlib

path = 'data_1934_DEC'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.hdf' in file:
            files.append(os.path.join(r, file))

# Section which should plot all the scans bandpass calibrated
for file_name in files:

    print(file_name.split("/")[1])

    f = h5py.File(file_name, 'r')

    f.keys()

    freq = np.array(f.get('beam_0/band_SB5/astronomy_data/frequency'))
    intensity = np.array(f.get('beam_0/band_SB5/astronomy_data/data'))

    # Data array shape is given by [spectral dump][][polarisations][channels][]

    chan_len = len(intensity[0][0][0])

    # Create an off source spectra by using the mean of the spectra dumps between 3 and 10.

    temp1 = []
    temp2 = []
    for i in range(2,10):
        temp1.append(np.reshape(intensity[i][0][0], chan_len))
        temp2.append(np.reshape(intensity[i][0][1], chan_len))

    temp1 = np.array(temp1)
    temp2 = np.array(temp2)

    off_source_pol1 = np.mean(temp1, axis=0)
    off_source_pol2 = np.mean(temp2, axis=0)

    i_off = (off_source_pol1 + off_source_pol2) / 2

    p_onoff = []
    median_intensity = []

    # Cycle through all spectral dumps
    for dump in range(0,len(intensity)):

        on_source_pol1 = np.reshape(intensity[dump][0][0], chan_len)
        on_source_pol2 = np.reshape(intensity[dump][0][1], chan_len)

        i_on = (on_source_pol1 + on_source_pol2) / 2

        p_onoff.append((i_on - i_off) / i_off)

    plt.axes(ylabel="Signal Strength [Counts]", xlabel="Spectral Dump Number")
    plt.title("Bandpass Calibrated Scan")
    plt.plot(range(0,len(intensity)), np.mean(p_onoff, axis= 1))

plt.savefig("Bandpass Calibrated Scan.png")
plt.show()

# Section that will run the bandpass cal for the "on source" scan portion of 1934
"""for file_name in files:

    f = h5py.File(file_name, 'r')

    f.keys()

    freq = np.array(f.get('beam_0/band_SB5/astronomy_data/frequency'))
    intensity = np.array(f.get('beam_0/band_SB5/astronomy_data/data'))

    # Data array shape is given by [spectral dump][][polarisations][channels][]

    intensity_median = []
    intensity_max = []
    off_source_pol1 = []
    off_source_pol2 = []
    chan_len = len(intensity[0][0][0])
    p_onoff = []

    # Cycle through all spectral dumps
    for dump in range(0,len(intensity)):

        # Create a temp array to store the data for pol 1
        intensity_temp = np.reshape(intensity[dump][0][0], chan_len)

        # Store the median value for each dump across the scan
        intensity_median.append(np.median(intensity_temp))

        # Using the dumps between this value as the off source spectra
        if 80 < dump < 100:

            off_source_pol1.append(np.reshape(intensity[dump][0][0], chan_len))
            off_source_pol2.append(np.reshape(intensity[dump][0][1], chan_len))

    # Record the spectral dump index where the intensity was at a maximum
    dump_on_source = intensity_median.index(np.max(intensity_median))

    # Create the on source pol spectra using the dump index above

    on_source_pol1 = np.reshape(intensity[dump_on_source][0][0], chan_len)
    on_source_pol2 = np.reshape(intensity[dump_on_source][0][1], chan_len)

    # Create the off source pol spectra by averaging the scan between 80 and 100 dumps.

    off_source_pol1 = np.array(off_source_pol1)
    off_source_pol2 = np.array(off_source_pol2)

    mean_off_pol1 = np.mean(off_source_pol1,axis=0)
    mean_off_pol2 = np.mean(off_source_pol2,axis=0)

    i_on = (on_source_pol1 + on_source_pol2)/2
    i_off = (mean_off_pol1 + mean_off_pol2)/2

    p_onoff.append((i_on - i_off)/i_off)

    median_intensity.append(np.median(p_onoff))

    plt.axes(ylabel="Signal Strength [Counts]", xlabel="Frequency [MHz]")
    plt.plot(freq,(i_on - i_off)/i_off, linewidth = 0.5)
    plt.title(file_name)
    plt.savefig(file_name.split("/")[1]+"_bandpasscal.png")
    plt.show()

    """
