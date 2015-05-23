# -*- coding: utf-8 -*-
"""
Created on Wed May 20 00:50:02 2015

@author: Martin Nguyen
"""

#Generate CSV files in this file
import csv
from numpy import random
def csv_dict_writer(path, fieldnames, data):
    with open(path, "wb") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    mylist = []
    for line in reader:
        mylist.append(line["IOP"])
        #print(line["last_name"])
    #print mylist
if __name__ == "__main__":
    field_names = "IOP,MD,MDR,Age".split(",")
    print field_names
    
    #print my_list
    path = "Patients_list.csv"
    for j in range(20):    
        
        my_list = []
        for i in range(3000):
            IOP = random.normal(28,3)
            while IOP < 22:
                IOP = random.normal(28,3)
            MD = -random.gamma(2,2.5)
            while MD > -3:
                MD = - random.gamma(2,2.5)
            MDR = random.gamma(2,0.014)
            Age = random.normal(68,5)    
            inner_dict = dict(zip(field_names, [IOP,MD,MDR,Age]))
            my_list.append(inner_dict)
        csv_dict_writer("Patients_list_{}.csv".format(j), field_names, my_list)
    