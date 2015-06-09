# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:51:48 2015

@author: Martin Nguyen
"""
from NodeClass import node
from numpy import random
#list of TreatmentTree 
# [[IOPreduction],CurrentMedicationType,SideEffect,MedicationCombination]
TreatmentTree = node ([ [511,1381] ,1, [10,109] , [1,0,0,0,0] ],
                      node([ [589,1407] ,2, [22,258] , [0,1,0,0,0] ],    
                           node([ [294,1231] ,3, [2,12] ,[0,0,1,0,0] ],
                               node([ [148,559] ,4, [5,17] , [0,0,0,1,0]],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,23,[5,17],[0,0,0,1,1] ])),
                               node([ [148,559] ,21,[5,17] ,  [0,0,1,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,22,[5,17],[0,0,1,1,1] ]))),
                               
                           node([ [294,1231] , 16 , [2,12] , [0,1,0,1,0] ],
                               node([ [148,559] ,17,[5,17] , [0,1,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),  
                                   node([ [763,1480] ,20,[5,17],[0,1,0,1,1] ])),
                               node([ [148,559] ,18,[5,17] , [0,1,1,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,19,[5,17],[0,1,1,1,1] ])))
                           ),
                      node([ [589,1407] , 6 , [22,258] , [1,1,0,0,0] ],
                           node([ [294,1231] , 7 , [2,12] , [1,0,1,0,0] ],
                               node([ [148,559] ,12,[5,17] , [1,0,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,15,[5,17],[1,0,0,1,1] ])),
                               node([ [148,559] ,13,[5,17] , [0,1,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,14,[5,17],[1,0,1,1,1] ]))),
                           node([ [294,1231] , 8 , [2,12] , [1,1,1,0,0] ],
                               node([ [148,559] ,9,[5,17] , [1,1,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,11,[5,17],[1,1,0,1,1] ])),
                               node([ [148,559] ,10,[5,17] , [1,1,1,0,1] ]))
                           )
                    )

class TreatmentBlock1(object):
    def __init__(self, params,medicalRecords):
        self.params = params
        self.medicalRecords = medicalRecords
    def update (self):
        #either no treatment or with treatment and side Effect (the TreatmentOverallStatus == 1) outside here only means that
        #side effect is incurred
        if self.medicalRecords['CurrentMedicationType'] == 0 or self.medicalRecords['TreatmentOverallStatus'] == 1:
            self.medicalRecords['ContinueTreatment'] = True
            self.DoctorPrescription()
        
        if self.params['IOPReduction'] < 0.1 and self.medicalRecords['MedicationIntake'] > 1 and self.medicalRecords['ContinueTreatment'] == True:
            self.medicalRecords['TreatmentOverallStatus'] =1
            self.DoctorPrescription()
            
        if self.medicalRecords['TreatmentOverallStatus'] == 2 and self.medicalRecords['MedicationIntake'] > 1:
            self.medicalRecords['ContinueTreatment'] = True
            self.DoctorPrescription()
            
        self.SetTimeNextVisit()
    def DoctorPrescription(self):
        #self.params['IOPReduction'] = 0.12
        tracenode  = node(0)
        tracenode = TreatmentTree
        if self.medicalRecords['MedicationPath'][0] == 0:
            self.medicalRecords['MedicationPath'][0] = 1
            self.operations(TreatmentTree)
            self.medicalRecords['TreatmentOverallStatus'] = 0
            self.medicalRecords['MedicationIntake'] = 0
        else:
            
            i = 1
            #this would shortcut CurrentMedicationType ==10, so when if-else evaluate below, we sure this is not because
            #the new treatment is
            if  self.medicalRecords['CurrentMedicationType'] == 10 and self.params['FirstProgression'] == 1:
                self.medicalRecords['ExitCode'] = True
                self.ResetMedicationPath()
            while i < 5 and self.medicalRecords['MedicationPath'][i] <> 0 and self.medicalRecords['CurrentMedicationType'] <> 10:  
                #add condition of i in here
                if self.medicalRecords['MedicationPath'][i] == 1:
                    tracenode = tracenode.left
                    i = i +1
                elif self.medicalRecords['MedicationPath'][i] == 2:
                    tracenode = tracenode.right
                    i = i+1
            
            if i < 5 and self.medicalRecords['CurrentMedicationType'] <> 10 :
                self.medicalRecords['MedicationPath'][i] = self.medicalRecords['TreatmentOverallStatus']
                if self.medicalRecords['TreatmentOverallStatus'] == 1:
                    tracenode = tracenode.left
                    self.operations(tracenode)
                if self.medicalRecords['TreatmentOverallStatus'] == 2:
                    #print('shit')
                    tracenode = tracenode.right
                    self.operations(tracenode)
            #This is the only way to get out of the treatment block
            
            # Here after every medication indication, patients need to     
            self.medicalRecords['TreatmentOverallStatus'] = 0
            self.medicalRecords['MedicationIntake'] = 0
            
            
            #exit the block if i == 5
            if i == 5 and self.params['FirstProgression'] == 1:
                self.medicalRecords['ExitCode'] = True
                self.ResetMedicationPath()
            
    def operations(self,tracenode):
        self.params['IOPReduction'] = random.beta(tracenode.value[0][0],tracenode.value[0][1])
        self.medicalRecords['CurrentMedicationType'] = tracenode.value[1] 
        if self.medicalRecords['CurrentMedicationType'] <> 5:
            self.params['SideEffect'] = random.beta(tracenode.value[2][0],tracenode.value[2][1])
        else:
            self.params['SideEffect'] = 0
        self.medicalRecords['MedicationCombination'] = tracenode.value[3]
    def SetTimeNextVisit(self):
        if self.medicalRecords['MedicationIntake'] == 0:
            self.params['time_next_visit'] = 3
        else:
            self.params['time_next_visit'] = 6
    def ResetMedicationPath(self):
        self.medicalRecords['MedicationPath'][2] = 0
        self.medicalRecords['MedicationPath'][3] = 0
        self.medicalRecords['MedicationPath'][4] = 0
        self.medicalRecords['OnTrabeculectomy'] = False
        
        if self.medicalRecords['MedicationPath'][1] ==1 :
            self.medicalRecords['MedicationPath'][1] = 2
            self.medicalRecords['CurrentMedicationType'] = 6
        else:
            self.medicalRecords['MedicationPath'][1] = 0
#        elif self.medicalRecords['MedicationPath'][1] ==2 :
#            self.medicalRecords['MedicationPath'][1] == 1
#            self.medicalRecords['CurrentMedicationType'] = 2
#        else:
#            print('This is very wrong')