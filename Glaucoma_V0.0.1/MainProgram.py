# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:58:54 2015

@author: Martin Nguyen
"""

#error checking measures 
import csv 
import matplotlib.pyplot as plt
def csv_dict_writer(path, fieldnames, data):
    with open(path, "wb") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
masterListforReplications = []
field_names = "QALY,TotalCost".split(",")
from PlottingSystemClass import PlottingSystem
from SimulationSystemClass import SimulationSystem
plottingsystem = PlottingSystem(plt)
order = 1
for i in range(20):
    sysSimulation = SimulationSystem(3000,"PatientList/Patients_list_{}.csv".format(i))
    sysSimulation.SystemSimulation()
    plottingsystem.plot(sysSimulation,order,i,masterListforReplications)
    order += (7*1) 
    del sysSimulation 
print order 
csv_dict_writer("MList.csv",field_names,masterListforReplications)