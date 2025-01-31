from tkinter import *
import math

def calculate(retrieved_values,outputFrame):
    ## === Requirements ===
    # As per ASC2022 10.5.C:
    # Solar cars must be able to repeatedly stop from speeds of 
    # 50 km/h (31 mph) or greater, with an average deceleration, on 
    # level wetted pavement, exceeding 4.72 m/s^2.
    #
    # For buffer velocity = 60km/h and deceleration = 6 m/s^2.
    ASC_Requirement = 4.72     #Average deceleration (m/s^2)

    # -- Constants ---
    g = 9.8        #Gravity (N/kg)

    calculated_values = [["V_t (N)",StringVar(outputFrame)],
                        ["A_mc (m^2)",StringVar(outputFrame)],
                        ["F_bp (N)",StringVar()],
                        ["P_mc (Pa)",StringVar()],
                        ["P_cal (Pa)",StringVar()],
                        ["F_cal_f (N)",StringVar()],
                        ["F_cal_r (N)",StringVar()],
                        ["F_cl_f (N)",StringVar()],
                        ["F_cl_r (N)",StringVar()],
                        ["F_friction_f (N)",StringVar()],
                        ["F_friction_r (N)",StringVar()],
                        ["T_r_f (N*m)",StringVar()],
                        ["T_r_r (N*m)",StringVar()],
                        ["F_tire_f (N)",StringVar()],
                        ["F_tire_r (N)",StringVar()],
                        ["F_total (N)",StringVar()],
                        ["KE (J)",StringVar()],
                        ["d_s (m)",StringVar()],
                        ["a_v (m/s^2)",StringVar()],
                        ["V_f (N)",StringVar()],
                        ["V_r (N)",StringVar()],
                        ["WT (N)",StringVar()],
                        ["V_f_d (N)",StringVar()],
                        ["V_r_d (N)",StringVar()],
                        ["F_tire_f_wt (N)",StringVar()],
                        ["F_tire_r_wt (N)",StringVar()],
                        ["F_tire_f_bf (N)",StringVar()],
                        ["F_tire_r_bf (N)",StringVar()],
                        ["n - Braking Efficiency, Total",StringVar()],
                        ["n_f - Braking Efficiency, Front",StringVar()],
                        ["n_r - Braking Efficiency, Rear",StringVar()],
                        ["Theoretical Deceleration",StringVar()],
                        ["Difference",StringVar()],
                        ["Safety Factor",StringVar()]]
    
    try:
        ## === Calculations ===
        calculated_values[0][1].set(retrieved_values[0]*g) #V_t - Weight of the vehicle (N)

        # --- Master Cylinder ---
        calculated_values[1][1].set(math.pi*math.pow((retrieved_values[4]/39.37),2)/4) #A_mc - Effective area of the master cylinder (m^2)

        # --- Brake Pedal Force --- 
        calculated_values[2][1].set(retrieved_values[2] * retrieved_values[3]) #F_bp - Force output of the brake pedal assembly (N)

        # --- Master Cylinder Pressure --- 
        calculated_values[3][1].set(float(calculated_values[2][1].get()) / float(calculated_values[1][1].get())) #P_mc - Hydraulic pressure generated by the master cylinder (Pa)

        # --- Force generated by caliper piston --- 
        calculated_values[4][1].set(calculated_values[3][1].get()) #P_cal - Hydraulic pressure transmitted to the calliper (Pa)
        calculated_values[5][1].set(float(calculated_values[4][1].get()) * retrieved_values[5]) #F_cal_f - One sided linear mechanical force generated by the caliper (N)
        calculated_values[6][1].set(float(calculated_values[4][1].get()) * retrieved_values[6]) #F_cal_r

        # --- Caliper Clamp Load --- 
        calculated_values[7][1].set(float(calculated_values[5][1].get()) * 2) #F_cl_f - Clamp force generated by the caliper (N)
        calculated_values[8][1].set(float(calculated_values[6][1].get())) #F_cl_r

        # --- Force on disc by brake pads --- 
        calculated_values[9][1].set(float(calculated_values[7][1].get()) * retrieved_values[14]) #F_friction_f - Frictional force generated by the brake pads opposing the rotation of the rotor (N)
        calculated_values[10][1].set(float(calculated_values[8][1].get()) * retrieved_values[14]) #F_friction_r

        # --- Torque of rotor --- 
        calculated_values[11][1].set(float(calculated_values[9][1].get()) * retrieved_values[11]) #T_r_f - Torque generated by the rotor (N*m)
        calculated_values[12][1].set(float(calculated_values[10][1].get()) * retrieved_values[12]) #T_r_r

        # --- Force on a tire --- 
        calculated_values[13][1].set(float(calculated_values[11][1].get()) / retrieved_values[13]) #F_tire_f - Force reacted between the tire and the ground (assuming friction exists to support the force) (N)
        calculated_values[14][1].set(float(calculated_values[12][1].get()) / retrieved_values[13]) #F_tire_r
        calculated_values[15][1].set(float(calculated_values[13][1].get()) * 2 + float(calculated_values[14][1].get()) * 2)  #F_total - Total braking force reacted between the vehicle and the ground (assuming adequate traction exists) (N)

        # --- Kinetic energy of the vehicle --- 
        retrieved_values[1] /= 3.6 #Velocity - km/h to m/s
        calculated_values[16][1].set(0.5*retrieved_values[0]*math.pow(retrieved_values[1],2)) #KE - (J)

        # --- Stopping Distance --- 
        calculated_values[17][1].set(float(calculated_values[16][1].get()) / (retrieved_values[15] * retrieved_values[0] * g)) #d_s - Stopping distance of the vehicle (m)

        # --- Deceleration --- 
        calculated_values[18][1].set((0 - math.pow(retrieved_values[1],2)) / (2 * float(calculated_values[17][1].get()))) #a_v - Deceleration of the vehicle (m/s^2)

        # --- Front axle vertical force --- 
        calculated_values[19][1].set((retrieved_values[7] * float(calculated_values[0][1].get())) / retrieved_values[9]) #V_f - (N)

        # --- Rear axle vertical force --- 
        calculated_values[20][1].set((retrieved_values[8] * float(calculated_values[0][1].get())) / retrieved_values[9]) #V_r - (N)

        # --- Dynamic absolute weight transferred --- 
        calculated_values[21][1].set(abs((float(calculated_values[18][1].get()) / g) * (retrieved_values[10] / retrieved_values[9]) * float(calculated_values[0][1].get())))  #WT - Absolute weight transferred from the rear axle to the front axle (N) 

        # --- Dynamic Vertical Force --- 
        calculated_values[22][1].set(float(calculated_values[19][1].get()) + float(calculated_values[21][1].get())) #V_f_d - Front axle dynamic vertical force for a given deceleration (N)
        calculated_values[23][1].set(float(calculated_values[20][1].get()) - float(calculated_values[21][1].get())) #V_r_d - Rear axle dynamic vertical force for a given deceleration (N)

        # --- Effect of weight transfer on Tire Output --- 
        calculated_values[24][1].set(retrieved_values[15] * float(calculated_values[19][1].get())) #F_tire_f_wt - (N)
        calculated_values[25][1].set(retrieved_values[16] * float(calculated_values[20][1].get())) #F_tire_r_wt

        # --- Maximum Braking Force Produced By axle --- 
        calculated_values[26][1].set(retrieved_values[15] * float(calculated_values[22][1].get())) #F_tire_f_bf - (N)
        calculated_values[27][1].set(retrieved_values[16] * float(calculated_values[23][1].get())) #F_tire_r_bf

        # --- Braking Efficiency --- 
        calculated_values[28][1].set((float(calculated_values[15][1].get()) / float(calculated_values[0][1].get())) * 100) #n - Total Braking Efficiency
        calculated_values[29][1].set(((2 * float(calculated_values[13][1].get()) / float(calculated_values[0][1].get()) * 100) / float(calculated_values[28][1].get())) * 100) #n_f - Front
        calculated_values[30][1].set(((2 * float(calculated_values[14][1].get()) / float(calculated_values[0][1].get()) * 100) / float(calculated_values[28][1].get())) * 100) #n_r - Rear

        # --- Theoretical Deceleration ---
        calculated_values[31][1].set(float(calculated_values[15][1].get()) / retrieved_values[0]) #Theoretical Deceleration
        calculated_values[32][1].set(float(calculated_values[31][1].get()) - ASC_Requirement) #Difference
        calculated_values[33][1].set(float(calculated_values[31][1].get()) / ASC_Requirement) #Safety_Factor
    except:
        print("Missing or Invalid Values")
        return calculated_values
    return calculated_values

