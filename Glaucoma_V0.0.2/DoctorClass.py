# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:03:03 2015

@author: Martin Nguyen
"""
TimeToVFTest = 11
from TreatmentBlock1Class import TreatmentBlock1
from TreatmentBlock2Class import TreatmentBlock2
class Doctor(object):
    def __init__(self,Attribute,params,medicalRecords):
        self.PatientAttribute = Attribute
        self.params = params
        self.medicalRecords = medicalRecords
#Main Program instructions 
    def ReturnAllDoctorValues (self):
        self.IOPTargetSetting()
        self.IOPandSideEffectEvaluation()
        self.DoctorModule()
        
        
        
#This module is to instruct the treatment block             
    def DoctorModule(self):
        if self.medicalRecords['TreatmentBlock'] == 1: 
            block1 = TreatmentBlock1(self.params,self.medicalRecords)
            block1.update()
            del block1
        if self.medicalRecords['TreatmentBlock'] == 2:
            block2 = TreatmentBlock2(self.PatientAttribute,self.params,self.medicalRecords)
            block2.update()
            del block2
        if self.medicalRecords['TreatmentBlock'] == 3:
            block3 = TreatmentBlock1(self.params,self.medicalRecords)
            block3.update()
            del block3
#        if self.medicalRecords['TreatmentBlock'] > 3:
#            print ('')
        self.medicalRecords['PatientVisits'] = self.medicalRecords['PatientVisits'] +1
    def IOPTargetSetting(self):
        #the doctor module here is only called during VF Tests
        if self.params['VFCountdown'] > TimeToVFTest: 
            self.SetCorrectIOPTarget()
            self.medicalRecords['NumberVF'] +=1
        self.params['VFCountdown'] = self.params['VFCountdown'] + self.params['time_next_visit']
    #Deeper level of meaning     
    def SetCorrectIOPTarget(self):
        if self.params['FirstProgression'] == 1 and self.PatientAttribute['CumulativeMDR'] > 2: 
            self.params['SecondProgression'] =1 
            self.PatientAttribute['CumulativeMDR'] = 0
        elif self.PatientAttribute['CumulativeMDR'] > 2:
            self.params['FirstProgression'] = 1
            self.params['SecondProgression'] =0
            self.PatientAttribute['CumulativeMDR'] = 0
        else:
            self.params['FirstProgression'] = 0
            self.params['SecondProgression'] = 0
        
        if self.params['FirstProgression'] == 1 and self.params['SecondProgression']  == 1:
            self.PatientAttribute['IOPTarget'] = 15.0
        elif self.params['FirstProgression'] == 1:
            self.PatientAttribute['IOPTarget'] = 18.0
        else:
            self.PatientAttribute['IOPTarget'] = 21.0
            
        self.params['VFCountdown'] = 0
    def IOPandSideEffectEvaluation(self):
        if self.medicalRecords['MedicationIntake'] > 10 :
            self.params['SideEffect'] = 0
        if self.PatientAttribute['IOP'] > self.PatientAttribute['IOPTarget']:
            self.medicalRecords['TreatmentOverallStatus'] = 2
            self.medicalRecords['ContinueTreatment'] = True
        else:
            self.medicalRecords['ContinueTreatment'] =False