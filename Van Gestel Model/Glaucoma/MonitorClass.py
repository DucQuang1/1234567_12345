# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:32:17 2015

@author: Martin Nguyen
"""
from __future__ import division
import copy 
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
    def Medication1Update(self,name,timevisit):
        self.Medication_amount[name][0] +=1
        self.TotalCost[name] += 6.0*timevisit
    def Medication2Update(self,name,timevisit):
        self.Medication_amount[name][1] += 1
        self.TotalCost[name] += 20.02*timevisit
    def Medication3Update(self,name,timevisit):
        self.Medication_amount[name][2] += 1
        self.TotalCost[name] += 13.9*timevisit
    def Medication4Update(self,name,timevisit):
        self.Medication_amount[name][3] += 1
        self.TotalCost[name] += 14.0*timevisit
    def Medication5Update(self,name,timevisit):
        self.Medication_amount[name][4] += 1
    def CumulativeCostfromMD (self,name,MD,Age,timevisit):
        if MD < -20:
            self.TotalCost[name] += (80.0 +130.0)*timevisit
            self.Below15[name] = 1
            if Age < 65:
                self.ProductiveLoss[name] =1
        elif MD < -15:
            self.TotalCost[name] += (56.0 +103.0)*timevisit
            self.Below15[name] = 1
            if Age < 65:
                self.ProductiveLoss[name] =1
        elif MD < -10:
            self.TotalCost[name] += (37.0+159.0)*timevisit
        elif MD < -5:
            self.TotalCost[name] += (20.0)*timevisit
    def finalCostPatient (self,name,Trabeculectomy,Visits,VF):
        self.TotalCost[name] += (Trabeculectomy*1214 + Visits*(6+2+65) +self.Below15[name]*325 +self.ProductiveLoss[name]*3029)
        self.TotalCost[name] += (VF *150.0)
        