# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:41:37 2015

@author: Martin Nguyen
"""


from __future__ import division
import simpy
import csv
from MonitorClass import Monitor
from PatientClass import Patient
initiallist = []
list_IOP = []
list_MD = []
list_MDR = []
list_Age = []

def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        list_IOP.append(float(line["IOP"]))
        list_MD.append(float(line["MD"]))
        list_MDR.append(float(line["MDR"]))
        list_Age.append(float(line["Age"]))

def final_cost_calculate(patientlist):
    i = 0
    for obj in patientlist:
        obj.CostAttribute['TotalCost'] += (obj.medicalRecords['NumberTrabeculectomy'] * 1214 + obj.medicalRecords['PatientVisits'] * (6+2+65))
        obj.CostAttribute['TotalCost'] += (obj.CostAttribute['Below-15']*325 + obj.CostAttribute['ProductiveLoss']*3029)  
        obj.CostAttribute['TotalCost'] += (obj.medicalRecords['NumberVF'] *150)
        monitor.finalCostPatient(i,obj.medicalRecords['NumberTrabeculectomy'],obj.medicalRecords['PatientVisits'],obj.medicalRecords['NumberVF'])
        i += 1
if __name__ == "__main__":
    monitor = Monitor (3000)
    patientlist = []
    field_names = "IOP,MD,MDR,Age".split(",")
    path = "Patients_list.csv"
    with open("Patients_list.csv") as f_obj:
        csv_dict_reader(f_obj)
    env = simpy.Environment()   
    
    for i in range(3000):
        patientlist.append( Patient(env,i,monitor,{'IOP':list_IOP[i],'MD': list_MD[i],'MDR':list_MDR[i],'CumulativeMDR': 0,'IOPTarget': 24,'Age':list_Age[i], 'TrabeculectomyIOP': 0}))
    env.run(until = 200)
    final_cost_calculate (patientlist)



#error checking measures 

newlist = []
newlist1 = []
sum4 = 0
for obj in monitor.initiallist:
    newlist1.append(obj['MD'])
sum1 = 0
sum2 = 0
sum3 = 0
for obj in patientlist:
    #print obj.medicalRecords['TreatmentBlock']
    #print obj.medicalRecords['ContinueTreatment']
    #print obj.params['IOPReduction']
    newlist.append(obj.Attribute['MD'])
    #newlist.append( obj.medicalRecords['TrabeculectomySuccess'])
    #if obj.medicalRecords['TrabeculectomySuccess'] == True:
    #    sum1 += 1
    #newlist.append( obj.medicalRecords['MedicationIntake'])
    sum1 += obj.CostAttribute['QALY']
    #sum2 += obj.CostAttribute['TotalCost']
    sum3 += obj.Attribute['MD']
    #newlist.append(obj.medicalRecords['TreatmentBlock'])
    #newlist.append(obj.Attribute['MD'])
    #newlist.append(obj.medicalRecords['CurrentMedicationType'])
    #print obj.medicalRecords['CurrentMedicationType']
    #print obj.params
    #print obj.medicalRecord

import matplotlib.pyplot as plt
plt.figure(1)
print ('Average QALY: {}'.format(sum1/3000))
print ('Average MD: {}'.format(sum3/3000))
# print ('Average Medical Cost: {}'.format(sum4/3000))
#==============================================================================
#plt.figure(2)
plt.hist(newlist1)
plt.title("Bar Chart for initial MD values")
plt.xlabel("MD")
plt.ylabel("Number (Counts)")
#print(sum1)
#plt.title("Final Values")
#plt.xlabel("Types")
#plt.ylabel("Count")
#plt.show()
#plt.hist(newlist1)     