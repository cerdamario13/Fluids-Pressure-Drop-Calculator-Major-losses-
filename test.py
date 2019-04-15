# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:20:23 2019

@author: Mario cerda
"""
#TEST FILE 

#fluids test
#$ pip install fluids
import fluids
import math


#********Metric******
#calculating the pressure drop across a pipe
#assuming conservation of mass V1A1 = V2A2
#assuming z1 = z2

#change in pressure function
def change_press(ff, l, iD, rhoo, Vel):
    return ((ff*l)/iD) * ((rhoo*Vel**2)/2)


#asking the users for the needed variables (METRIC)
rho1 = float(input('Density(kg/m^3): '))
q = float(input('Volumetric flow(m^3/s): '))
mu1 = float(input('Abs viscosity(N*s/m^2): '))
nps = float(input('Nominal diameter: '))
epsilon = float(input('roughness(cm): '))
length = float(input('Lenght(m): '))
npsNums = fluids.nearest_pipe(NPS = nps)
#getting the values form the tuple
inDiam = npsNums[1] #inner diam
area = (math.pi * inDiam ** 2) / 4

#calculating the velocity
vel = q / area


#calculating Reynols number
re = fluids.core.Reynolds(D=inDiam, rho=rho1, V=vel, mu=mu1)

#Friction factor (MAJOR LOSS)
f = fluids.friction.friction_factor(Re = re, eD=epsilon/(inDiam/100))

deltaP = change_press(f, length, inDiam, rho1, vel)
deltaP_KPa = deltaP/1000
deltaP_psi = deltaP * 0.000145038
print('')
print('***************')
print('Delta Press(Pa)', round(deltaP, 2))
print('Delta Press(KPa)', round(deltaP_KPa, 2))
print('Delta Press(psi)', round(deltaP_psi, 2))
print('Reynols # ', round(re, 2))
print('Vel ', round(vel, 2))
