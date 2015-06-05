# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:58:54 2015

@author: Martin Nguyen
"""

#error checking measures 
import csv 
import matplotlib.pyplot as plt
numberofGraphs = 15
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
for i in range(2):
    sysSimulation = SimulationSystem(3000,"PatientList/Patients_list_{}.csv".format(i))
    sysSimulation.SystemSimulation()
    plottingsystem.plot(sysSimulation,order,i,masterListforReplications)
    order += (numberofGraphs*1) 
    del sysSimulation 
print order 
csv_dict_writer("MList.csv",field_names,masterListforReplications)