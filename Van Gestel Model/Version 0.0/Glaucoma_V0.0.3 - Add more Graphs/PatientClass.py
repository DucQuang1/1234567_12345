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
        #'MedicationAmount': [0,0,0,0,0],
        self.medicalRecords = {'PatientVisits': 0, 'MedicationIntake': 0,'MedicationCombination':[0,0,0,0,0],
                               'CurrentMedicationType':0,'TreatmentOverallStatus': 0,
                               'TreatmentBlock': 'A', 'MedicationPath': [0,0,0,0,0],'ContinueTreatment':True,
                               'NumberVF':0, 'ExitCode': False,
                               'NumberTrabeculectomy':0, 'TrabeculectomySuccess': True,
                               'OnTrabeculectomy': False,
                               'ImplantSuccess': True, 
                               'OnImplant':False}
        self.CostAttribute = {'QALY': 0, 'TotalCost': 0, 'Below-15': 0, 'ProductiveLoss':0}
        #initiallist.append(copy.deepcopy(self.Attribute))
        monitor.UpdateInitial(self.Attribute)
        self.action = env.process(self.runSimulation())
    def  runSimulation (self):
        while True:
            self.monitor.UpdateCurrentMedicationType(self.name,self.medicalRecords)
            self.monitor.UpdateMedicationIntake(self.name,self.medicalRecords)
            doctor = Doctor(self.Attribute,self.params,self.medicalRecords)
            doctor.ReturnAllDoctorValues()
            
            self.inCurredSideEffect(doctor)
            self.monitor.CumulativeCostfromMD(self.name,self.Attribute['MD'],self.Attribute['Age'],self.params['time_next_visit'])
            yield self.env.timeout(self.params['time_next_visit'])
            self.params_update()
            #onelist[self.name].append(self.Attribute['IOPTarget'])
            for i in range(int(float(self.params['time_next_visit']))):
                self.monitor.UpdateIOPlist(self.name,self.Attribute)
                self.monitor.UpdateMDlist(self.name,self.Attribute)
                self.monitor.UpdateIOPTargetlist(self.name,self.Attribute)
                self.monitor.UpdateVFCountdown(self.name,self.params)
                self.monitor.UpdateSideEffect(self.name,self.params)
                self.monitor.UpdateOverallStatus(self.name,self.medicalRecords)
            self.monitor.UpdateTimeNextVisit(self.name,self.params)
            del doctor
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
        if self.medicalRecords['ContinueTreatment'] == True :
            self.onMedication()
        if self.medicalRecords['CurrentMedicationType'] == 5 and self.params['IOPReduction'] > 0:
            self.params['IOPReduction'] -= self.params['IOPReduction']*(self.params['time_next_visit']/12)
    
    def onNoMedicationOrTrabeculectomy(self):
        self.params['SideEffect'] = 0
            #IOP is supposed to increase 0.5% annually, without medication
        if  self.medicalRecords['OnTrabeculectomy'] == True or self.medicalRecords['OnImplant'] == True:
            self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (1.5/100)*(self.params['time_next_visit']/12))
            self.medicalRecords['MedicationIntake'] += 1 
        else:
            self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (0.5/100)*(self.params['time_next_visit']/12))
        if self.medicalRecords['MedicationIntake'] == 0:
            self.medicalRecords['MedicationIntake'] += 1
    def onMedication(self):
        self.medicalRecords['MedicationIntake'] += 1 
        self.Attribute['IOP'] = self.Attribute['IOP'] *(1-self.params['IOPReduction']*(self.params['time_next_visit']/12))
        self.UpdateMedicationCombination()
    def inCurredSideEffect(self,doctor):
        SideEffect = 0            
        if random.uniform(0,1) < self.params['SideEffect']:
            self.medicalRecords['TreatmentOverallStatus'] = 1
            self.medicalRecords['ContinueTreatment'] = True
            doctor.DoctorModule() 
            self.monitor.UpdateCurrentMedicationType(self.name,self.medicalRecords)
            self.monitor.UpdateOverallStatus(self.name,self.medicalRecords)
            SideEffect = 1
        self.CostAttribute['QALY'] += (0.94 - 0.097*SideEffect + 0.015*self.Attribute['MD'] - 0.092*0.4)*(self.params['time_next_visit']/12)
    def UpdateMedicationCombination(self):
        if self.medicalRecords['MedicationCombination'][0] == 1:
            self.monitor.Medication1Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][1] == 1:
            self.monitor.Medication2Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][2] == 1:
            self.monitor.Medication3Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][3] == 1:
            self.monitor.Medication4Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][4] == 1:
            self.monitor.Medication5Update(self.name,self.params['time_next_visit'])
