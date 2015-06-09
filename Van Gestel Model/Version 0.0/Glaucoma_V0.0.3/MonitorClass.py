# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:32:17 2015

@author: Martin Nguyen
"""
from __future__ import division
import copy 
BBlockerPrice = 6.0
ProstaPrice = 20.20
CarboPrice = 13.90
AdrePrice = 14.0
Retirementhome = 80.0
Nursinghome = 130.0
Familyhelp = 56.0
Homecaregroom = 103.0
Householdhelp = 37.0
Homecarenurse = 159.0
Informalcare = 20.0
CostTrabeculectomy =1214.0
LowVisionAid = 325.0
ProductiveLoss = 3029.0
VisualFieldTest = 150.0
class Monitor(object):
    def __init__(self, size):
        self.size = size
        #self.medicalRecords = [{} for i in range(self.size)]
        self.IOP_list = [[0 for j in range(0)] for i in range(self.size)]
        self.MD_list  = [[0 for j in range(0)] for i in range(self.size)]
        self.Medication_amount = [[0,0,0,0,0] for i in range(self.size)]
        self.TotalCost = [0 for i in range(self.size)]
        self.Below15 = [0 for i in range(self.size)]
        self.ProductiveLoss = [0 for i in range(self.size)]
        #self.CostAttribute = {'QALY': 0, 'TotalCost': 0, 'Below-15': 0, 'ProductiveLoss':0,'MedicationAmount':[0,0,0,0,0]}
        self.initiallist = []
    def UpdateInitial(self,Attribute = None):
        self.initiallist.append(copy.deepcopy(Attribute))
    def UpdateIOPlist (self,name,Attribute = None):
        self.IOP_list[name].append(Attribute['IOP'])
    def UpdateMDlist (self,name,Attribute = None):
        self.MD_list[name].append(Attribute['MD'])
    def Medication1Update(self,name,timevisit):
        self.Medication_amount[name][0] +=1
        self.TotalCost[name] += BBlockerPrice*timevisit
    def Medication2Update(self,name,timevisit):
        self.Medication_amount[name][1] += 1
        self.TotalCost[name] += ProstaPrice*timevisit
    def Medication3Update(self,name,timevisit):
        self.Medication_amount[name][2] += 1
        self.TotalCost[name] += CarboPrice*timevisit
    def Medication4Update(self,name,timevisit):
        self.Medication_amount[name][3] += 1
        self.TotalCost[name] += AdrePrice*timevisit
    def Medication5Update(self,name,timevisit):
        self.Medication_amount[name][4] += 1
    def CumulativeCostfromMD (self,name,MD,Age,timevisit):
        if MD < -20:
            self.TotalCost[name] += (Retirementhome +Nursinghome)*timevisit
            self.Below15[name] = 1
            if Age < 65:
                self.ProductiveLoss[name] =1
        elif MD < -15:
            self.TotalCost[name] += (Familyhelp +Homecaregroom)*timevisit
            self.Below15[name] = 1
            if Age < 65:
                self.ProductiveLoss[name] =1
        elif MD < -10:
            self.TotalCost[name] += (Householdhelp+Homecarenurse)*timevisit
        elif MD < -5:
            self.TotalCost[name] += (Informalcare)*timevisit
    def finalCostPatient (self,name,Trabeculectomy,Visits,VF):
        self.TotalCost[name] += (Trabeculectomy*CostTrabeculectomy + Visits*(6+2+65) +self.Below15[name]*LowVisionAid +self.ProductiveLoss[name]*ProductiveLoss)
        self.TotalCost[name] += (VF *VisualFieldTest)
        