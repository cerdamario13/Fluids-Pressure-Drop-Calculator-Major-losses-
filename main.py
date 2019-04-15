#importing tkinter
from tkinter import *
import math
import fluids #fluids package for fluid calculations
import tkinter.messagebox #for the error message box



#creating a tkinter GUI that will detrmine if a fluid in the system is Laminar or turbulent
# it will also determine the pressure drop in the system

#------------------------------------- Setting up tkinter settings
root = Tk()

root.title('Pressure Drop Calculation') #title
root.geometry("550x500")
root.resizable(width=False, height=False)
color = 'gray77'
root.configure(bg=color) #background color

#------------------------------------- Short Description of the program
description_label = Label(text='Pressure drop (Major Loss). Using (fluids) python package.')\
    .grid(row=0, column=0, columnspan=5)


#------------------------------------- Title at the top
title_label = Label(text='Enter variables (Metric)', font='Helvetica 10 bold', width=20, bg=color)\
    .grid(row=1, column=0, columnspan=2)

#------------------------------------- Labels and Entries
entry_width = 11
label_width = 15

#Entries
rho_label = Label(text='Rho(Density)', width=label_width, bg=color).grid(row=3, column=0)
rho_var = DoubleVar()
rho_num = Entry(textvariable=rho_var, width=entry_width)#variable name is rho_var
rho_num.grid(row=3, column=1) #have to call .grid seperate otherwise the 'delete' does not work

q_label = Label(text='Q(vol/rate)', width=label_width, bg=color).grid(row=4, column=0)
q_var = DoubleVar()
q_num = Entry(textvariable=q_var, width=entry_width)
q_num.grid(row=4, column=1) #variable name is q_var

mu_label = Label(text='Absolute visc', width=label_width, bg=color).grid(row=5, column=0)
mu_var = DoubleVar()
mu_num = Entry(textvariable=mu_var, width=entry_width)
mu_num.grid(row=5, column=1)

nps_label = Label(text='Nominal diam', width=label_width, bg=color).grid(row=6, column=0)
nps_var = DoubleVar()
nps_num = Entry(textvariable=nps_var, width=entry_width)
nps_num.grid(row=6, column=1)

len_label = Label(text='Length', width=label_width, bg=color).grid(row=7, column=0)
len_var = DoubleVar()
len_num = Entry(textvariable=len_var, width=entry_width)
len_num.grid(row=7, column=1)

e_label = Label(text='Roughness', width=label_width, bg=color).grid(row=8, column=0)
e_var = DoubleVar()
e_num = Entry(textvariable=e_var, width=entry_width)
e_num.grid(row=8, column=1)


#------------------------------------- Buttons
calc_btn = Button(text='Calculate', width=20, command=lambda: delta_press()).grid(row=9, column=0, columnspan=2)
clear_btn = Button(text='Clear', width=20, command=lambda: clear()).grid(row=7, column=4, columnspan=2)


#---Adding space for the results by adding another 'blank' column
blank_col3 = Label(width=10, bg=color).grid(row=3, column=3)#this adds a blank column
    #allowing us to have some separation between boxes and labels

#Results
result_label_width = 20

#title for results
result_title = Label(text='Results', width=20, bg=color , font='Helvetica 10 bold')\
    .grid(row=1, column=4, columnspan=2)

pressP_label = Label(text='Change Pressure (Pa)', width=result_label_width, bg=color).grid(row=3, column=4)
pressP_var = DoubleVar()
pressP_num = Entry(textvariable=pressP_var, width=entry_width, state='readonly')
pressP_num.grid(row=3, column=5)

presskPa_label = Label(text='Change Pressure (KPa)', width=result_label_width, bg=color).grid(row=4, column=4)
presskPa_var = DoubleVar()
presskPa_num = Entry(textvariable=presskPa_var, width=entry_width, state='readonly')
presskPa_num.grid(row=4, column=5)

pressPSI_label = Label(text='Change Pressure (PSI)', width=result_label_width, bg=color).grid(row=5, column=4)
pressPSI_var = DoubleVar()
pressPSI_num = Entry(textvariable=pressPSI_var, width=entry_width, state='readonly')
pressPSI_num.grid(row=5, column=5)

rey_label = Label(text='Fluid', width=result_label_width + 8, bg=color).grid(row=6, column=4)
rey_var = StringVar()
rey_num = Entry(textvariable=rey_var, width=10, state='readonly')
rey_num.grid(row=6, column=5)


#------------------------------------- Functions

def delta_press():

    if rho_var.get() and q_var.get() and mu_var.get() and nps_var.get() and len_var.get() and e_var != 0:

        npsNums = fluids.nearest_pipe(NPS = nps_var.get()) #returns: NPS, inner diam, outer diam, wall thickness
        #Getting the values form the NPS tuple
        inDiam = npsNums[1] #inner diam
        area = (math.pi * inDiam ** 2) / 4 #surface area for the pipe

        #calculating velocity from volumetric flowrate and area
        vel = q_var.get() / area

        #Calculating Reynols number
        rey_calc = fluids.core.Reynolds(D=inDiam, rho=rho_var.get(), V=vel, mu=mu_var.get())
        #if conditional for Laminar or turbulent flow
        if rey_calc < 2100:
            rey_var.set('Laminar')
        elif rey_calc > 2101:
            rey_var.set('Turbulent')

        #calculating friction factor (MAJOR LOSSES ONLY)
        f = fluids.friction.friction_factor(Re=rey_calc, eD=e_var.get()/(inDiam/100))

        #change in pressure function
        def change_press(ffactor, length, idiam, density, Vel): #Friction f, inner diam, density, velocity
            return ((ffactor*length)/idiam) * ((density*Vel**2)/2)


        #change in pressure
        deltaP = change_press(f, len_var.get(), inDiam, rho_var.get(), vel)


        #printing the values
        pressP_var.set(round(deltaP, 2))
        presskPa_var.set(round(deltaP/1000, 2))
        pressPSI_var.set(round(deltaP * 0.000145038, 2))

    elif rho_var.get() or q_var.get() or mu_var.get() or nps_var.get() or len_var.get() or e_var == 0:
        errorMsg('error')




def clear(): #clearing all of the variables when pressed
    #clearing the entries
    rho_num.delete(0, END)
    q_num.delete(0, END)
    mu_num.delete(0, END)
    nps_num.delete(0, END)
    len_num.delete(0, END)
    e_num.delete(0, END)

    #clearing the results (only works it NOT using 'readonly')
    pressP_num.delete(0, END)
    presskPa_num.delete(0, END)
    pressPSI_num.delete(0, END)
    rey_num.delete(0, END)

#Generating an error message
def errorMsg(ms):
    if ms == 'error':
        tkinter.messagebox.showerror('Error!', 'Check numbers.')


root.mainloop() #closing the file



