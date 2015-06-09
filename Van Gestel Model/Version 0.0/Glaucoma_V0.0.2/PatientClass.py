# -*- coding: utf-8 -*-
"""
Created on Wed May 20 01:19:20 2015

@author: Martin Nguyen
"""

from __future__ import division
from numpy import random
from DoctorClass import Doctor


class Patient(object):
    def __init__(self,env,name,monitor,Attribute):
        random.seed = 123
        self.name = name
        self.age = random.normal(68,5)
        self.env = env
        self.monitor = monitor
        self.Attribute = Attribute
        self.params = {'IOPReduction':0,'time_next_visit': 0,'FirstProgression':0,'SecondProgression':0,'VFCountdown':0,
                       'SideEffect':0 }
        self.medicalRecords = {'PatientVisits': 0, 'MedicationIntake': 0,'MedicationCombination':[0,0,0,0,0],
                               'MedicationAmount': [0,0,0,0,0],'CurrentMedicationType':0,'TreatmentOverallStatus': 0,
                               'TreatmentBlock':1, 'MedicationPath': [0,0,0,0,0],'ContinueTreatment':True,
                               'NumberVF':0,
                               'NumberTrabeculectomy':0, 'TrabeculectomySuccess': True,
                               'OnTrabeculectomy': False}
        self.CostAttribute = {'QALY': 0, 'TotalCost': 0, 'Below-15': 0, 'ProductiveLoss':0}
        #initiallist.append(copy.deepcopy(self.Attribute))
        monitor.UpdateInitial(self.Attribute)
        self.action = env.process(self.runSimulation())
    def params_update(self):
        if self.Attribute['IOP'] > 13:
            difference = self.Attribute['MDR'] *(1.13**(self.Attribute['IOP'] - 15.5))*(self.params['time_next_visit'])
        else:
            difference = 0
        # adjust with the time 
        self.Attribute['CumulativeMDR'] = self.Attribute['CumulativeMDR'] + difference
        self.Attribute['MD'] = self.Attribute['MD'] - difference
        self.Attribute['Age'] = self.Attribute['Age'] + self.params['time_next_visit']/12
        if  self.medicalRecords['ContinueTreatment'] == False or self.params['IOPReduction'] < 0.001:
            self.onNoMedicationOrTrabeculectomy()
        if self.medicalRecords['ContinueTreatment'] == True and self.medicalRecords['TreatmentBlock'] <> 0:
            self.onMedication()
        if self.medicalRecords['CurrentMedicationType'] == 10 or self.medicalRecords['CurrentMedicationType'] == 5 and self.params['IOPReduction'] > 0:
            self.params['IOPReduction'] -= self.params['IOPReduction']*(self.params['time_next_visit']/12)
    def UpdateMedicationCombination(self):
        if self.medicalRecords['MedicationCombination'][0] == 1:
            self.monitor.Medication1Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][1] == 1:
            self.monitor.Medication2Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][2] == 1:
            self.monitor.Medication2Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][3] == 1:
            self.monitor.Medication3Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][4] == 1:
            self.monitor.Medication5Update(self.name,self.params['time_next_visit'])
    def onNoMedicationOrTrabeculectomy(self):
        self.params['SideEffect'] = 0
            #IOP is supposed to increase 0.5% annually, without medication
        if  self.medicalRecords['OnTrabeculectomy'] == True:
            self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (1/100)*(self.params['time_next_visit']/12))
        else:
            self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (0.5/100)*(self.params['time_next_visit']/12))
    def onMedication(self):
        self.medicalRecords['MedicationIntake'] = self.medicalRecords['MedicationIntake'] +1 
        self.Attribute['IOP'] = self.Attribute['IOP'] *(1-self.params['IOPReduction']*(self.params['time_next_visit']/12))
        self.UpdateMedicationCombination()
    def inCurredSideEffect(self,doctor):
        SideEffect = 0            
        if random.uniform(0,1) < self.params['SideEffect']:
            self.medicalRecords['TreatmentOverallStatus'] = 1
            self.medicalRecords['ContinueTreatment'] = True
            doctor.DoctorModule() 
            SideEffect = 1
        self.CostAttribute['QALY'] += (0.94 - 0.097*SideEffect + 0.015*self.Attribute['MD'] - 0.092*0.4)*(self.params['time_next_visit']/12)
    def  runSimulation (self):
        while True:
            doctor = Doctor(self.Attribute,self.params,self.medicalRecords)
            doctor.ReturnAllDoctorValues()
            self.inCurredSideEffect(doctor)
            self.monitor.CumulativeCostfromMD(self.name,self.Attribute['MD'],self.Attribute['Age'],self.params['time_next_visit'])
            yield self.env.timeout(self.params['time_next_visit'])
            self.params_update()
            #onelist[self.name].append(self.Attribute['IOPTarget'])
            self.monitor.UpdateIOPlist(self.name,self.Attribute)
            self.monitor.UpdateMDlist(self.name,self.Attribute)
            del doctor
