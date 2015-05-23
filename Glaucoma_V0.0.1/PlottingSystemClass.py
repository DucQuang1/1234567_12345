# -*- coding: utf-8 -*-
"""
Created on Sat May 23 18:05:45 2015

@author: Martin Nguyen
"""

class PlottingSystem(object):
    def __init__(self,plt):
        self.plt = plt
        self.newlist = []
        self.newlist1 = []
        self.newlist2 = []
        self.newlist3 = []
    def plot(self,SimulationSystem,order,iteration,masterList):
        for obj in SimulationSystem.monitor.initiallist:
            self.newlist1.append(obj['MD'])
            
        sum1 = 0
        sum2 = 0
        sum3 = 0
        field_names = "QALY,TotalCost".split(",")
        for obj in SimulationSystem.patientlist:
            self.newlist.append(obj.Attribute['MD'])
            self.newlist2.append(obj.CostAttribute['QALY'])
            self.newlist3.append(obj.medicalRecords['CurrentMedicationType'])
            sum1 += obj.CostAttribute['QALY']
            sum3 += obj.Attribute['MD']
        for i in SimulationSystem.monitor.TotalCost:
            sum2 += i
        inner_dict = dict(zip(field_names,[sum1/3000,sum2/3000]))
        masterList.append(inner_dict)
        
        print ('CURRENT ITERATION: {}'.format(iteration))
        print ('Average QALY: {}'.format(sum1/3000))
        print('Average Medical Cost: {}'.format(sum2/3000))
        print ('Average MD: {}'.format(sum3/3000))
        print (' ')
        
        
        
        
#==============================================================================
#         self.plt.figure(order)  
#         self.plt.hist(self.newlist1)
#         self.plt.title("Iteration {} :Bar Chart for initial MD values".format(iteration))
#         self.plt.xlabel("MD")
#         self.plt.ylabel("Number (Counts)")
#         order = order + 1
#         self.plt.figure(order)
#         self.plt.hist(self.newlist)
#         self.plt.title("Iteration {}: Bar Chart for final MD values".format(iteration))
#         self.plt.xlabel("MD")
#         self.plt.ylabel("Number (Counts)")
#         order = order + 1
#         self.plt.figure(order)
#         for i in range(5):
#             self.plt.plot(SimulationSystem.monitor.IOP_list[i])
#         self.plt.title("Iteration {}: IOP Progression".format(iteration))
#         order += 1
#         self.plt.figure(order)
#         for i in range(5):
#             self.plt.plot(SimulationSystem.monitor.MD_list[i])
#         self.plt.title("Iteration {}: MD Progression".format(iteration))
#         order += 1
#         self.plt.figure(order)
#         self.plt.hist(self.newlist2)
#         self.plt.title("Iteration {}: QALY distribution".format(iteration))
#         order += 1
#         self.plt.figure(order)
#         self.plt.hist(SimulationSystem.monitor.TotalCost)
#         self.plt.title("Iteration {}: Distribution of Medical Cost".format(iteration))
#         order += 1
#         self.plt.figure(order)
#         self.plt.hist(self.newlist3)
#         self.plt.title("Iteration {}: Distribution of Final Medication Type".format(iteration))
#==============================================================================
