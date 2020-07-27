import numpy as np
import matplotlib.pyplot as plt
import h5py

file_name = 'uwl_191213_123813.hdf'

f = h5py.File(file_name,'r')

f.keys()

print(f.get('beam_0/band_SB7/calibrator_data/'))

freq = np.array(f.get('beam_0/band_SB7/calibrator_data/cal_frequency'))
cal_on = np.array(f.get('beam_0/band_SB7/calibrator_data/cal_data_on'))
cal_off = np.array(f.get('beam_0/band_SB7/calibrator_data/cal_data_off'))


# Shape of the data array first dimension is the spectral dump number
# Then the polarisations
# Channel number

cal_on_pol1 = []
cal_on_pol2 = []
cal_off_pol1 = []
cal_off_pol2 = []

for i in range(0, 23):

    cal_on_pol1_temp = np.reshape(cal_on[i][0][0], 128)
    cal_on_pol1.append(cal_on_pol1_temp)

    cal_on_pol2_temp = np.reshape(cal_on[i][0][1], 128)
    cal_on_pol2.append(cal_on_pol2_temp)

    cal_off_pol1_temp = np.reshape(cal_off[i][0][0], 128)
    cal_off_pol1.append(cal_off_pol1_temp)

    cal_off_pol2_temp = np.reshape(cal_off[i][0][1], 128)
    cal_off_pol2.append(cal_off_pol2_temp)

cal_on_pol1 = np.array(cal_on_pol1)
cal_on_pol2 = np.array(cal_on_pol2)
cal_off_pol1 = np.array(cal_off_pol1)
cal_off_pol2 = np.array(cal_off_pol2)

cal_on_pol1 = np.mean(cal_on_pol1, axis = 0)
cal_on_pol2 = np.mean(cal_on_pol2, axis = 0)
cal_off_pol1 = np.mean(cal_off_pol1, axis = 0)
cal_off_pol2 = np.mean(cal_off_pol2, axis = 0)

print(cal_on_pol1)

plt.axes(ylabel = "Signal Strength [Jy]", xlabel = "Frequency [MHz]")
plt.plot(freq,cal_on_pol1, label = "cal_on_pol1")
plt.plot(freq,cal_on_pol2, label = "cal_on_pol2")
plt.plot(freq,cal_off_pol1, label = "cal_off_pol1")
plt.plot(freq,cal_off_pol2, label = "cal_off_pol2")
plt.legend()
plt.title("Cal on/off: " +file_name + " - R1")
plt.savefig("Cal_onoff.png")