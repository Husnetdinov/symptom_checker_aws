# Author: Chirag Jhamb
# To be deployed on AWS Labmda, requires files mentioned below 

import json
import pandas as pd

disease_description_path = "data/disease_description.json"
disease_symptoms_path = "data/symptoms.json"

json1_file = open(disease_symptoms_path)
json1_str = json1_file.read()
json1_data = json.loads(json1_str)

def f3(seq): #https://www.peterbe.com/plog/uniqifiers-benchmark
    keys = {}
    while " " in seq:
        seq.remove(" ")
    for e in seq:
        keys[e] = 1
    return keys.keys()

def give_symptoms(s1,s2,s3,s4):
    s_list=[]
    for i in json1_data.keys():
        if (str(s1) in json1_data[i]) and (str(s2) in json1_data[i]) and (str(s3) in json1_data[i]) and (str(s4) in json1_data[i]):
            s_list.extend(json1_data[i])
    return f3(s_list)

def diagnose(s1,s2,s3,s4):
    details=pd.read_json(disease_description_path)
    d_list=[]
    items=[]
    for i in json1_data.keys():
        if s1 in json1_data[i] and s2 in json1_data[i] and s3 in json1_data[i] and s4 in json1_data[i]:
            d_list.append(i)
    for j in d_list:
        dis_details={}
        n=details[details.disease == j].index
        dis_details["name"]=details.get_value(n[0], "disease")
        dis_details["tests"]=details.get_value(n[0], "test").replace("         ","").replace("\t","")
        dis_details["desc"]=details.get_value(n[0], "desc")
        dis_details["specialities"]=f3(details.get_value(n[0], "specialities"))
        dis_details["symp"]=details.get_value(n[0], "symp")
        dis_details["img_link"]="https://s3.ap-south-1.amazonaws.com/mmdisease/"+str(dis_details["name"].replace(" ","_"))+".jpg"
        #if dis_details not in items:
        items.append(dis_details)
    return items

def lambda_handler(event, context):
    if event["type"]=="d":
        return diagnose(event["s1"],event["s2"],event["s3"],event["s4"])
    elif event["type"]=="s":
        return sorted(give_symptoms(event["s1"],event["s2"],event["s3"],event["s4"]))
    else:
        return "type error"
