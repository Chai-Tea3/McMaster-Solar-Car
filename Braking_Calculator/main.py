from tkinter import *
from tkinter import ttk
from equations import calculate
import re

def intiate_calc():
    retrieved_values=[""]*17
    for i in range(len(values)):
        try:
            retrieved_values[i] = float(values[i][1].get())
        except:
            print("Invalid character in the input")
    print(retrieved_values)
    calculated_values = calculate(retrieved_values,outputFrame)
    for i in range(len(calculated_values)):
        Label(outputFrame,text=calculated_values[i][0]).grid(column=0,row=i,padx=6,sticky=W)
        Entry(outputFrame,textvariable=calculated_values[i][1]).grid(column=1,row=i,padx=6,sticky=(W,E))


#Use regex to only allow float values to be input into the text fields
def check_num(newval):
    return re.match('^\d*[.,]?\d*$', newval) is not None and len(newval) <= 15


#Create window
root = Tk()
root.title("Braking Calculator")
root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)

#   Title box
topframe = Frame(root, borderwidth=5,relief='raised',background='green')
topframe.pack(fill=BOTH)
Label(topframe,text="Braking Calculator",font=("Arial",25)).pack(anchor='center')

#   Left box, for user to input values
inputFrame = Frame(root, borderwidth=5,relief='raised')
inputFrame.pack(side=LEFT,expand=True,fill=BOTH)

#Variables to hold text labels and text box values
values = [["Mass (kg)",StringVar(inputFrame,"500")],
          ["Velocity (m/s)",StringVar(inputFrame,"60")],
          ["F_d (N)",StringVar(inputFrame,"130")], 
          ["L_ratio",StringVar(inputFrame,"7")],
          ["MC_Bore (Inch)",StringVar(inputFrame,"1")],
          ["A_cal_f (m^2)",StringVar(inputFrame,"0.001019353")],
          ["A_cal_r (m^2)",StringVar(inputFrame,"0.00154838")],
          ["CG_f (m)",StringVar(inputFrame,"1.47")],
          ["CG_r (m)",StringVar(inputFrame,"1.47")],
          ["WB (m)",StringVar(inputFrame,"2.94")],
          ["h_cg (m)",StringVar(inputFrame,"0.5775")],
          ["R_eff_f (m)",StringVar(inputFrame,"0.13")],
          ["R_eff_r (m)",StringVar(inputFrame,"0.1651")],
          ["R_t (m)",StringVar(inputFrame,"0.254")],
          ["u_bp",StringVar(inputFrame,"0.4")],
          ["u_peak_f",StringVar(inputFrame,"0.6")],
          ["u_peak_r",StringVar(inputFrame,"0.6")]]



check_num_wrapper = (root.register(check_num), '%P') #Call function to validate if entry is a float
#Text Labels and Text Boxes
for i in range(len(values)):
    Label(inputFrame,text=values[i][0]).grid(column=0,row=i,padx=6,sticky=W)
    Entry(inputFrame,textvariable=values[i][1],validate='key',validatecommand=check_num_wrapper).grid(column=1,row=i,padx=6,sticky=(W,E))

#Calculate/Quit buttons
Label(inputFrame,text="").grid(column=0,row=17) #Spacer
Button(inputFrame,text="Calculate",command=intiate_calc).grid(column=1,row=20,padx=6,pady=6,sticky=E)
Button(inputFrame,text="quit",command=root.destroy).grid(column=0,row=20,padx=6,pady=6,sticky=W)

#   Right box, for calculated values
outputFrame = Frame(root, borderwidth=5,relief='raised')
outputFrame.pack(side=RIGHT,expand=True,fill=BOTH)
intiate_calc()

root.mainloop()