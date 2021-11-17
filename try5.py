# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:31:56 2021

@author: Leon
"""
import numpy as np

N=10
bw=20e6/N
pt= 0.1
n= 10.0 ** (-173 / 10.0)*0.001
I= 10.0 ** (-140 / 10.0)*0.001
ts = 0.1
pmax=0.2

ues = list(range(N))
cap = np.zeros(N)
d = np.zeros([N, N])
Cc = np.zeros([N, N])
Cr = np.zeros(N)
tc = np.zeros([N, N])
pr = np.zeros([N, N])
CB = np.zeros([N, N])
G = np.zeros([N, N])
Gc = np.zeros([N, N])
Gr = np.zeros([N, N])

class User() :
    
    def __init__(self, number):
        self.number = number
        self.x = int(np.random.uniform(-250,250))
        self.y = int(np.random.uniform(-250,250))
        self.g = 1
        
    def gain(self):
        d = np.sqrt(self.x**2+self.y**2)
        self.g = (d)**-3
        print(self.g)
        
def createUser():
    for i in range(N):
        ues[i] = User('i')
        ues[i].gain()

def capacity(ues):
    for i in range(N):
        C=bw*np.log2(1+(pt*ues[i].g)/(bw*(n+I)))
        cap[i]=C
   # print(cap)

def distance(ues):
    for i in range(N):
        for j in range(N):
            d[i,j] = np.sqrt((ues[j].x-ues[i].x)**2+(ues[j].y-ues[i].y))
            

def capCue(ues):
    for i in range(N):
        for j in range(N):
            if i != j:
                Cc[i,j]=2*bw*np.log2(1+(pt*d[i,j]**-3)/(2*bw*(n+I)))
            else :
                Cc[i,j]=0
    
    #print(Cc)

def capRue(ues):
    for i in range(N):
        Cr[i]=2*bw*np.log2(1+(pt*ues[i].g)/(2*bw*(n+I)))
        
def time(ues):
    for i in range(N):
        for j in range(N):
            if i != j:
               tc[i,j]= cap[i]*ts/Cc[i,j]
            else :
                tc[i,j]=0
    #print(tc)
    
def capBoost(ues):
    for i in range(N):
        for j in range(N):
            if i != j:
               pr[i,j]= (pt*ts)/(ts-tc[i,j])
            else :
                tc[i,j]=0
    
    for i in range(N):
        for j in range(N):
            if i != j:
                pb= min(pr[i,j], pmax)
                CB[i,j]=2*bw*np.log2((2*bw*(n+I)+pb*ues[i].g)/(2*bw*(n+I)+pt*ues[i].g))
            else :
                CB[i,j]=0
    
    #print(CB)

def deriveG (ues):
    for i in range(N):
        for j in range(N):
            if i !=j:
                Gc[i,j] = Cc[i,j]*tc[i,j]-cap[i]*ts
                Gr[i,j] = Cr[i]*(ts-tc[i,j])-Cc[i,j]*tc[i,j]-cap[i]*ts
            if i != j and Gc[i,j]>=0 and (Gr[i,j] + CB[i,j]) > 0:
                G[i,j]=  Gc[i,j]+Gr[i,j]+CB[i,j]
            else :
                G[i,j]=0
    print(G)

createUser()
capacity(ues)
distance(ues)
capCue(ues)
capRue(ues)
time(ues)
capBoost(ues)     
deriveG(ues)

        
        
        