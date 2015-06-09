# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:16:26 2015

@author: Martin Nguyen
"""
from numpy import random
from TreatmentBlock2Class import TreatmentBlock2
class TreatmentBlock3(TreatmentBlock2):
    def __init__ (self,Attribute,params,medicalRecords):
        self.__init__(self, Attribute,params,medicalRecords)
    def updateImplant(self):
        if self.medicalRecords['OnImplant'] == False:
            self.SurgeryImplant()
        else:
            self.SetNumberofVisits()
            
        self.DeterminetoExitImplantblock()
    def SurgeryImplant(self):
        self.Attribute['IOP'] = random.normal(15,0.37)
        self.medicalRecords['ContinueTreatment'] = False
        self.medicalRecords['OnImplant'] = True
        self.medicalRecords['MedicationIntake'] = 0
        self.medicalRecords['CurrentMedicationType'] = 31
        self.medicalRecords['TreatmentOverallStatus'] = 0
    def DeterminetoExitImplantblock (self):
        if self.medicalRecords['TreatmentOverallStatus'] == 2 :
            
            if  self.medicalRecords['MedicationIntake'] < 9:
                self.medicalRecords['ImplantSuccess'] = False
                self.medicalRecords['OnImplant'] = False
                self.medicalRecords['ExitCode'] = True
            else:
                #self.medicalRecords['TreatmentBlock']  = 3
                self.medicalRecords['OnImplant'] = False
                self.medicalRecords['ExitCode'] = True