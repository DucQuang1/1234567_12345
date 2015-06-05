# -*- coding: utf-8 -*-
"""
Created on Sat May 23 18:05:45 2015

@author: Martin Nguyen
"""
numberofPatients = 5
class PlottingSystem(object):
    def __init__(self,plt):
        self.plt = plt
        self.newlist = []
        self.newlist1 = []
        self.newlist2 = []
        self.newlist3 = []
        self.newlist4 = []
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
            self.newlist4.append(obj.medicalRecords['NumberTrabeculectomy'])
            sum1 += obj.CostAttribute['QALY']
            sum3 += obj.Attribute['MD']
        for i in SimulationSystem.monitor.TotalCost:
            sum2 += i
        
        inner_dict = dict(zip(field_names,[sum1/SimulationSystem.size,sum2/SimulationSystem.size]))
        masterList.append(inner_dict)
        
        print ('CURRENT ITERATION: {}'.format(iteration))
        print ('Average QALY: {}'.format(sum1/SimulationSystem.size))
        print('Average Medical Cost: {}'.format(sum2/SimulationSystem.size))
        print ('Average MD: {}'.format(sum3/SimulationSystem.size))
        print (' ')
        
        
        
        
#==============================================================================
        self.plt.figure(order)  
        self.plt.hist(self.newlist1)
        self.plt.title("Iteration {} :Bar Chart for initial MD values".format(iteration))
        self.plt.xlabel("MD")
        self.plt.ylabel("Number (Counts)")
        order = order + 1
        self.plt.figure(order)
        self.plt.hist(self.newlist)
        self.plt.title("Iteration {}: Bar Chart for final MD values".format(iteration))
        self.plt.xlabel("MD")
        self.plt.ylabel("Number (Counts)")
        order = order + 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.IOP_list[i])
        self.plt.title("Iteration {}: IOP Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("IOP level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.MD_list[i])
        self.plt.title("Iteration {}: MD Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("MD level")
        order += 1
        ######plot new stuffs here
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.IOPTarget_list[i])
        self.plt.title("Iteration {}: IOP Target Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("IOP Target level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.CurrentMed_list[i])
            print ("Patient {}: List of Medication Progression is {}".format(i,SimulationSystem.monitor.CurrentMed_list[i]))
            print("Patient {}: List of Final Medication Amount is {}".format(i,SimulationSystem.monitor.Medication_amount[i]))
        self.plt.title("Iteration {}: Current Medication Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Current Medication Number")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.TimeNextVisit_list[i])
        self.plt.title("Iteration {}: Time to Next Visit Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Number of Months")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.SideEffect_list[i])
        self.plt.title("Iteration {}: Side Effect Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("Number of Months")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.MedicationIntake_list[i])
        self.plt.title("Iteration {}: Medication Intake Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Current Medication Amount")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.VFCoutdown_list[i])
        self.plt.title("Iteration {}: VF Countdown Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("Number of Months")
        order = order+1 
        self.plt.figure(order)
        for i in range(numberofPatients+50):
            self.plt.plot(SimulationSystem.monitor.TreatmentStatus_list[i])
        self.plt.title("Iteration {}: Treatment status Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("Status")
        order = order+1 
        self.plt.figure(order)
        self.plt.hist(self.newlist2)
        self.plt.title("Iteration {}: QALY distribution".format(iteration))
        self.plt.xlabel("QALY")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(SimulationSystem.monitor.TotalCost)
        self.plt.title("Iteration {}: Distribution of Medical Cost".format(iteration))
        self.plt.xlabel("Dollars")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(self.newlist3)
        self.plt.title("Iteration {}: Distribution of Final Medication Type".format(iteration))
        self.plt.xlabel("Final Medication Type")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(self.newlist4)
        self.plt.title("Iteration {}: Distribution of Number of Trabeculectomy".format(iteration))
        self.plt.xlabel("Number of Trabeculectomy")
        self.plt.ylabel("Counts")
        del self.newlist[:]
        del self.newlist1[:]
        del self.newlist2[:]
        del self.newlist3[:]
        del self.newlist4[:]
#==============================================================================
