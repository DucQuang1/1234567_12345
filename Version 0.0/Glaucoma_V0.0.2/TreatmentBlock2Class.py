# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:16:36 2015

@author: Martin Nguyen
"""
from numpy import random
class TreatmentBlock2 (object):
    def __init__ (self,Attribute,params,medicalRecords):
        self.Attribute = Attribute
        self.params = params
        self.medicalRecords = medicalRecords
    def update(self):
        if self.medicalRecords['NumberTrabeculectomy'] == 0:
            self.SurgeryTE()
        else:
            self.SetNumberofVisits()
            
        if self.medicalRecords['TreatmentOverallStatus'] == 2 :
            self.medicalRecords['ContinueTreatment'] = False
            
            if  self.medicalRecords['MedicationIntake'] < 9:
                self.medicalRecords['TrabeculectomySuccess'] = False
                self.medicalRecords['TreatmentBlock'] = 3
            else:
                self.medicalRecords['TreatmentBlock']  = 3
    def SurgeryTE(self):
        #self.Attribute['TrabeculectomyIOP'] = self.Attribute['IOP']
        self.Attribute['IOP'] = random.normal(12.5,0.3)
        self.medicalRecords['ContinueTreatment'] = False
        self.medicalRecords['OnTrabeculectomy'] = True
        self.medicalRecords['MedicationIntake'] = 0
        self.medicalRecords['NumberTrabeculectomy'] +=1
        self.medicalRecords['CurrentMedicationType'] = 30
    def SetNumberofVisits(self):
        self.medicalRecords['MedicationIntake'] = self.medicalRecords['MedicationIntake'] +1 
        if self.medicalRecords['MedicationIntake'] == 0 or self.medicalRecords['MedicationIntake'] == 1 or self.medicalRecords['MedicationIntake'] == 2 or self.medicalRecords['MedicationIntake'] == 3:
            self.params['time_next_visit'] = 0.1
        elif self.medicalRecords['MedicationIntake'] == 4 or self.medicalRecords['MedicationIntake'] == 5 or self.medicalRecords['MedicationIntake'] == 6:
            self.params['time_next_visit'] = 0.25
        elif self.medicalRecords['MedicationIntake'] == 7 or self.medicalRecords['MedicationIntake'] == 8:
            self.params['time_next_visit'] = 0.5
        elif self.medicalRecords['MedicationIntake'] == 9:
            self.params['time_next_visit'] = 1
        else:
            self.params['time_next_visit'] = 6