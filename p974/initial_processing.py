#!/usr/bin/env python3.5

import subprocess as sp
import numpy as np


#############################################
# TIME AVERAGE ALL FILES
#############################################

# sp.call('sdhdf_modify -e T -T uwl_*.hdf', shell = True)


#############################################
# ASSIGNING REFERENCE POSITIONS
#############################################

"""off_source_list = ["uwl_191213_111118.hdf", "uwl_191213_123813.hdf", "uwl_191214_080511.hdf", "uwl_191214_112126.hdf"]
R2 = ["uwl_191213_114420.hdf"]
off_source_list.extend(R2)"""

off_source_list = sp.check_output('sdhdf_identify -src R1 uwl_*.hdf', shell = True).decode('utf-8').split("\n")[:-1]

R2 = sp.check_output('sdhdf_identify -src R2 uwl_*.hdf', shell = True).decode('utf-8').split("\n")[:-1]
off_source_list.extend(R2)

file_name = []

for i in range(0, len(off_source_list)):
    file_name.append(off_source_list[i].split(".hdf")[0])

ref_dets = []
# array with [0] as date and [1] as time

for i in range(0, len(file_name)):
    temp = [file_name[i].split('_')[1], file_name[i].split('_')[2]]
    ref_dets.append(temp)

#############################################
# ASSIGNING SOURCE POSITIONS
#############################################

# given a source, match to closest reference position in time

# Array of all source IDs (eg. S1, S2...)
source_ids = []
for i in range(1, 37):
    source_ids.append("S" + str(i))

on_source_list = []

for i in range(0, len(source_ids)):

    on_source_list.append(sp.check_output('sdhdf_identify -src ' +str(source_ids[i])+ ' uwl_*.hdf', shell = True).decode("utf-8").split("\n")[:-1])

"""on_source_list = [["uwl_191213_111456.hdf", "uwl_191214_080227.hdf"],
                  ["uwl_191213_111721.hdf", "uwl_191214_081050.hdf"],
                  ["uwl_191213_111947.hdf", "uwl_191214_081318.hdf", "uwl_191214_112930.hdf"]]"""

src_file_name = []

for j in range(0, len(on_source_list)):
    temp = []
    for i in range(0, len(on_source_list[j])):
        temp.append(on_source_list[j][i].split(".hdf")[0])
    src_file_name.append(temp)

src_dets = []
# array with [0] as date and [1] as time


for j in range(0, len(src_file_name)):
    temp = []
    for i in range(0, len(src_file_name[j])):
        temp.append([src_file_name[j][i].split("_")[1], src_file_name[j][i].split("_")[2]])
    src_dets.append(temp)


#############################################
# MATCHING EACH SOURCE POSITION WITH A REFERENCE POSITION
#############################################

for source in range(0, len(on_source_list)):
    for file in range(0, len(on_source_list[source])):

        # print("On source file: " + on_source_list[source][file])

        date = src_dets[source][file][0]

        distance_in_time = 99999

        for i in range(0, len(off_source_list)):

            if ref_dets[i][0] == date:

                # print("Ref source file to compare: " + off_source_list[i])

                if distance_in_time > np.abs(int(ref_dets[i][1]) - int(src_dets[source][file][1])):
                    distance_in_time = np.abs(int(ref_dets[i][1]) - int(src_dets[source][file][1]))

                    ref_index = i

        print("Found match! Performing bandpass calibration: "+on_source_list[source][file] + " " + off_source_list[ref_index])

        sp.call("sdhdf_onoff -on "+ on_source_list[source][file] +".T -off "+ off_source_list[ref_index] +".T -o "+ "S"+str(int(source)+1) +"-"+ src_dets[source][file][0]+"_"+src_dets[source][file][1] +"_bpcal", shell = True)
        sp.call("sdhdf_modify -e lsr -lsr "+"S"+str(int(source)+1) +"-"+ src_dets[source][file][0]+"_"+src_dets[source][file][1] +"_bpcal", shell = True)
        sp.call("sdhdf_baseline -f "+ "S"+str(int(source)+1) +"-"+ src_dets[source][file][0]+"_"+src_dets[source][file][1] +"_bpcal.lsr", shell = True)
        sp.call("sdhdf_modify -e total -p1 "+ "S"+str(int(source)+1) +"-"+ src_dets[source][file][0]+"_"+src_dets[source][file][1] +"_bpcal.lsr", shell = True)

#############################################
# SUM ACROSS ALL SOURCE POSITIONS
#############################################

for src_id in range(0, len(source_ids)):
    sp.call("sdhdf_sum -o "+ source_ids[src_id]+".sum " +source_ids[src_id]+"*.total", shell = True)
