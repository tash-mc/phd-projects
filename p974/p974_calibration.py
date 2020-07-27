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


median_intensity = []

for file_name in files:

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
    median_intensity =[]

    # Cycle through all spectral dumps
    for dump in range(0,len(intensity)):

        # Using the dumps between this value as the off source spectra
        if 2 < dump < 10:

            off_source_pol1.append(np.reshape(intensity[dump][0][0], chan_len))
            off_source_pol2.append(np.reshape(intensity[dump][0][1], chan_len))

    off_source_pol1 = np.array(off_source_pol1)
    off_source_pol2 = np.array(off_source_pol2)

    mean_off_pol1 = np.mean(off_source_pol1, axis=0)
    mean_off_pol2 = np.mean(off_source_pol2, axis=0)

    for dump in range(0, len(intensity)):

        on_source_pol1 = np.reshape(intensity[dump][0][0], chan_len)
        on_source_pol2 = np.reshape(intensity[dump][0][1], chan_len)

        i_on = (on_source_pol1 + on_source_pol2)/2
        i_off = (mean_off_pol1 + mean_off_pol2)/2

        p_onoff.append((i_on - i_off)/i_off)

        median_intensity.append(np.median(p_onoff))

    median_intensity = np.array(median_intensity)

    plt.plot(range(0,len(intensity)),median_intensity, linewidth=0.5)
    plt.axes(ylabel="Signal Strength [Counts]", xlabel="Spectral Dump Number")
    plt.title("bandpasscal_1934scans")
    plt.savefig("bandpasscal_1934scans.png")

    #teiujwdlaskld

"""
for file_name in files:

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


plt.axes(ylabel="Signal Strength [Counts]", xlabel="1934 Observation Files")
plt.plot(range(0, len(files)), median_intensity, linewidth=0.5)
plt.title("Plot of Average Signal Strength over Observations of 1934")
plt.savefig("Time Average.png")

    
    src_on_pol2 = np.reshape(intensity[56][0][1], 131072)

    src_off_pol1 = np.reshape(intensity[3][0][0], 131072)
    src_off_pol2 = np.reshape(intensity[3][0][1], 131072)


    plt.plot(freq,src_on_pol2)
    plt.plot(freq,src_on_pol1)
    plt.plot(freq,src_off_pol1)
    plt.plot(freq,src_off_pol2)
    plt.savefig("1934_DEC.png")



    i_on = (src_on_pol1 + src_on_pol2)/2
    i_off = (src_off_pol1 + src_off_pol2)/2

    p_onoff = ((i_on - i_off)/i_off)

    index = np.where(freq == 1380.0002)

    S_sys = 14.69/p_onoff[index]

    print(S_sys)

    p_onoff = S_sys*((i_on - i_off)/i_off)

    fit = np.polyfit(freq,p_onoff,1)

    array_1934 = [[1380,1413],[14.96, 14.87]]

    fit_1934 = np.polyfit(array_1934[0],array_1934[1],1)

    print(p_onoff.shape)

    plt.axes(ylabel = "Signal Strength [Jy]", xlabel = "Frequency [MHz]")
    plt.plot(freq,p_onoff, linewidth = 0.5)
    plt.plot(freq,fit[0]*freq+fit[1], label = "Data Best Fit")
    plt.plot(freq,fit_1934[0]*freq+fit_1934[1], label = "1934")
    plt.title(file_name+ " Ssys value of: " + str(S_sys))
    plt.legend()
    plt.savefig("1934_DEC.png")

"""