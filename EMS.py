# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 10:17:31 2022

@author: rubi
"""

import pandas as pd      
import numpy as np    
from pyomo.environ import *     
from pyomo.core.base.PyomoModel import ConcreteModel  
import matplotlib.pyplot as plt

df = pd.read_csv('sheet.csv' )  # Reading sheet into datafrme
df.columns =['Load', 'Price', 'PV']  # Adding column names in dataframe

load = df["Load"] # Extracting columns of dataframe and its datatype is series
Price=df[ "Price"]   # Extracting columns of dataframe and its datatype is series
PV=18*df["PV"]  # Extracting columns of dataframe and its datatype is series
PV_list=PV.tolist()   # Converting series datatype to list in order to call it in optimization problem
Price_list= Price.tolist()

print(Price_list)

def build_battery_model(model, Drate, Crate,efficiency, initial,Erated):
    
    
    model.pchar =   Var(model.T, domain=NonNegativeReals)
    model.pdis =    Var(model.T, domain=NonNegativeReals)
    model.S =       Var(model.T, bounds=(0, Erated))
    model.alpha=    Var(model.T, domain=Binary)
   
    @model.Constraint(model.T)     
    # def power_constraint1(model,t):      
    #    return model.pdis[23] == 0
    # @model.Constraint(model.T)   
    # def power_constraint2(model,t):      
    #    return model.pchar[23] == 0
  
   
    @model.Constraint(model.T)       
    def storage_state(model, t):
        'Storage changes with flows in/out and efficiency losses'
 
        # Set first hour energy equal to initial
        if t == 0:
           return (model.S[t] ==  (model.S[23] +model.PVbatt[t]*efficiency
                                + (model.pchar[t] * (efficiency)) 
                                - (model.pdis[t] / (efficiency))))
        else:
           return (model.S[t] == (model.S[t-1] +model.PVbatt[t]*efficiency
                                + (model.pchar[t] * (efficiency)) 
                                - (model.pdis[t] / (efficiency))))
    @model.Constraint(model.T)
    def discharge_constraint(model, t):
       
        "Maximum dischage each hour"
        return model.pdis[t] <= Drate*(1-model.alpha[t])
    
    @model.Constraint(model.T)
    def charge_constraint(model, t):
       
        "Maximum charge each hour"
        return model.pchar[t] <=  Crate *(model.alpha[t])   
    
       
    return model

def industry_EMS():
    model = ConcreteModel()
    model.T = RangeSet(0,23)
    model.bin=Var(model.T, domain=Binary)
    model.PVgrid =  Var(model.T, domain=NonNegativeReals)
    model.PVbatt =  Var(model.T, domain=NonNegativeReals)
    'Calling battery function'
    build_battery_model(model,50,50,0.98,30,65)
    @model.Constraint(model.T)
    def PV_constraint(model,t):
       return  model.PVbatt[t]+model.PVgrid[t]==PV_list[t]
    @model.Constraint(model.T)
    def M_constraint1(model,t):
       return  5000*model.bin[t]+model.PVbatt[t]<=5000
   
    def M_constraint2(model,t):
        return 5000*(1-model.bin[t])+model.pchar[t]<=5000
    @model.Objective()
    def obj(model):
        return  sum (model.pchar[t]*Price_list[t] for t in model.T)- sum((model.pdis[t]+model.PVgrid[t])*Price_list[t]  for t in model.T)
    return model 

def resultswrite_industry(model):
    pvgrid= [value(model.PVgrid[t]) for t in model.T]
    pvbatt = [value(model.PVbatt[t]) for t in model.T]
    pchar = [value(model.pchar[t])  for t in model.T]  
    
    pdis = [value(model.pdis[t])  for t in model.T]       
    charge_state = [value(model.S[t]) for t in model.T]
    print(charge_state)
    y=list(range(0,24))
    print(pchar)
    fig, ax1 = plt.subplots(figsize=(9,4))
    iterator1=zip(y,pvgrid)
    iterator2=zip(y,pvbatt)
    iterator3=zip(y,pchar)
    iterator4=zip(y,pdis)
    iterator5 =zip(y,charge_state)
    iterator7 =zip(y,PV_list)
    iterator6=zip(y,Price_list)
    
    df_dict1 = dict(    iterator1)
    df_dict2 = dict(    iterator2)
    df_dict3 = dict(    iterator3)
    df_dict4 = dict(    iterator4)
    df_dict5=dict(iterator5)
    df_dict6=dict(iterator6)
    df_dict7=dict(iterator7)
    ax1.plot(*zip(*sorted(df_dict7.items())),label = "PV")
    ax1.plot(*zip(*sorted(df_dict1.items())),color='cyan',label = "PVtogrid")
    ax1.plot(*zip(*sorted(df_dict2.items())),color='black',label = "PVtobatt")
    ax1.bar(*zip(*sorted(df_dict3.items())),color='blue', width=0.4, label = "Charging")
    ax1.bar(*zip(*sorted(df_dict4.items())),color='green', width=0.4,label = "Disharging")
   
   

    
    
    
    
    ax1.set_ylabel('Power')
   
    plt.legend()
    ax2 = ax1.twinx()
    
    ax2.plot(y,Price_list, color = 'r')
    ax2.set_ylabel('price (Nok/kwh)', color = 'r')
    
    plt.xticks(rotation=90)
    #plt.tight_layout()
    plt.margins(x=0)
    plt.tight_layout()
    
   
    plt.savefig("industry.pdf", bbox_inches = 'tight')
    plt.show()
    
  
    return 

def solve_industry_EMS():
    model=industry_EMS()  
    model.pprint()
    solver = SolverFactory('glpk')
    solver.solve(model)
    resultswrite_industry(model)
    return   

solve_industry_EMS()