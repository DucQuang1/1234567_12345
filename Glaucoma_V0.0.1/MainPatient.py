# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:05:11 2015

@author: Martin Nguyen
"""
from __future__ import division
import simpy
import copy
from numpy import random
from DoctorClass import Doctor
initiallist = []
onelist = [[0 for j in range(0)] for i in range(5000)]
class Patient(object):
    def __init__(self,env,name):
        random.seed = 123
        self.name = name
        self.age = random.normal(68,5)
        self.env = env
        self.Attribute = {'IOP':0,'MD':0,'MDR':0,'CumulativeMDR':0,'IOPTarget': 24,'Age':0 , 'TrabeculectomyIOP': 0}
        self.initializationAttributes()
        self.params = {'IOPReduction':0,'time_next_visit': 0,'FirstProgression':0,'SecondProgression':0,'VFCountdown':0,
                       'SideEffect':0}
        self.medicalRecords = {'PatientVisits': 0, 'MedicationIntake': 0,'MedicationCombination':[0,0,0,0,0],
                               'MedicationAmount': [0,0,0,0,0],'CurrentMedicationType':0,'TreatmentOverallStatus': 0,
                               'TreatmentBlock':1, 'MedicationPath': [0,0,0,0,0],'ContinueTreatment':True,
                               'NumberTrabeculectomy':0, 'TrabeculectomySuccess': True,
                               'OnTrabeculectomy': False}
        initiallist.append(copy.deepcopy(self.Attribute))
        self.action = env.process(self.runSimulation())
    
    def initializationAttributes(self):
        self.Attribute['IOP'] = random.normal(28,3) # need to do truncation later
        while self.Attribute['IOP'] < 22:
            self.Attribute['IOP'] = random.normal(28,3)
        self.Attribute['MD'] = -random.gamma(2,2.5) # need to do truncation later
        while self.Attribute['MD'] > -3:
            self.Attribute['MD'] = -random.gamma(2,2.5)
        self.Attribute['MDR'] = random.gamma(2,0.014)
        self.Attribute['Age'] = random.normal(68,5)
    def params_update(self):
        difference = self.Attribute['MDR'] *(1.13**(self.Attribute['IOP'] - 15.5))*(self.params['time_next_visit']/12)
        # adjust with the time 
        self.Attribute['CumulativeMDR'] = self.Attribute['CumulativeMDR'] + difference
        self.Attribute['MD'] = self.Attribute['MD'] - difference
        self.Attribute['Age'] = self.Attribute['Age'] + self.params['time_next_visit']/12
        if  self.medicalRecords['ContinueTreatment'] == False:
            self.params['SideEffect'] = 0
            #IOP is supposed to increase 0.5% annually, without medication
            if  self.medicalRecords['OnTrabeculectomy'] == True:
                self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (1/100)*(self.params['time_next_visit']/12))
            else:
                self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (0.5/100)*(self.params['time_next_visit']/12))
        
        if self.medicalRecords['ContinueTreatment'] == True and self.medicalRecords['TreatmentBlock'] <> 0:
            self.medicalRecords['MedicationIntake'] = self.medicalRecords['MedicationIntake'] +1 
            self.Attribute['IOP'] = self.Attribute['IOP'] *(1-self.params['IOPReduction']*(self.params['time_next_visit']/12))
            self.UpdateMedicationCombination()
        
    def UpdateMedicationCombination(self):
        if self.medicalRecords['MedicationCombination'][0] == 1:
            self.medicalRecords['MedicationAmount'][0] += 1 
        if self.medicalRecords['MedicationCombination'][1] == 1:
            self.medicalRecords['MedicationAmount'][1] +=1 
        if self.medicalRecords['MedicationCombination'][2] == 1:
            self.medicalRecords['MedicationAmount'][2] +=1 
        if self.medicalRecords['MedicationCombination'][3] == 1:
            self.medicalRecords['MedicationAmount'][3] +=1  
        if self.medicalRecords['MedicationCombination'][4] == 1:
            self.medicalRecords['MedicationAmount'][4] +=1 
    def  runSimulation (self):
        while True:
            doctor = Doctor(self.Attribute,self.params,self.medicalRecords)
            doctor.ReturnAllDoctorValues()
            #this is the side effect block, patients have to revisit 
            #the doctors again to change medication, there is side effect            
            if random.uniform(0,1) < self.params['SideEffect']:

                #if no effect, medication will not change
                self.medicalRecords['TreatmentOverallStatus'] = 1
                self.medicalRecords['ContinueTreatment'] = True
                doctor.DoctorModule() 
            #for the wait to kick in
            yield self.env.timeout(self.params['time_next_visit'])
            self.params_update()
            onelist[self.name].append(self.Attribute['IOP'])
            del doctor
if __name__ == "__main__":
    patientlist = []
    alllist = [] 
    env = simpy.Environment()   
    
    for i in range(5):
        patientlist.append( Patient(env,i))
        #alllist.append(onelist)
    env.run(until = 400)




#error checking measures 

newlist = []
newlist1 = []
for obj in initiallist:
    newlist1.append(obj['IOP'])
sum1 = 0
for obj in patientlist:
    #print obj.medicalRecords['TreatmentBlock']
    #print obj.medicalRecords['ContinueTreatment']
    #print obj.params['IOPReduction']
    #newlist.append( obj.medicalRecords['TrabeculectomySuccess'])
    #if obj.medicalRecords['TrabeculectomySuccess'] == True:
    #    sum1 += 1
    #newlist.append( obj.medicalRecords['MedicationIntake'])
    
    newlist.append(obj.medicalRecords['TreatmentBlock'])
    #newlist.append(obj.medicalRecords['CurrentMedicationType'])
    #print obj.medicalRecords['CurrentMedicationType']
    #print obj.params
    print obj.medicalRecords
#gaussian = random.normal(size =100)
#print gaussian
import matplotlib.pyplot as plt
#plot the time series
for i in range(30):
    plt.plot(onelist[i])
#plt.hist(newlist)
#print(sum1)
#plt.title("Final Values")
#plt.xlabel("Types")
#plt.ylabel("Count")
#plt.show()
#plt.hist(newlist1)