# -*- coding: utf-8 -*-
"""
Created on Tue May 19 23:44:20 2015

@author: Martin Nguyen
"""

import csv

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
        mylist.append(line["first_name"])
        #print(line["last_name"])
    print float(mylist[3]) +0.8
#----------------------------------------------------------------------


if __name__ == "__main__":
    data = ["first_name,last_name,city".split(","), "Tyrese,Hirthe,Strackeport".split(","),
    "Jules,Dicki,Lake Nickolasville".split(","),
     "Dedric,Medhurst,Stiedemannberg".split(","),[9.2,2.3,3.4]]

    my_list = []

    fieldnames = data[0]

    for values in data[1:]:
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)

    path = "dict_output.csv"
    csv_dict_writer(path, fieldnames, my_list)
    #print(data[0])
if __name__ == "__main__":
    with open("dict_output.csv") as f_obj:
        csv_dict_reader(f_obj)
        
        

