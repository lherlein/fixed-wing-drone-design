import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data from CSV file
file_path = 'xf-naca4412-il-1e6.csv'  # Replace with your actual file path
data = pd.read_csv(file_path, skiprows=10)

## Constants

rho = 1.225  # Air density (kg/m^3)
c = 0.1016  # Chord length (m)

b_w = 0.762  # Wing span (m)
S_w = b_w * c  # Wing area (m^2)
AR_w = b_w**2 / S_w  # Aspect ratio

b_t = 0.303  # Wing span (m) UP FOR VARIATION
S_t = b_t * c  # Wing area (m^2)
AR_t = b_t**2 / S_t  # Aspect ratio

W_est = 7 # Estimated weight of the aircraft (N)

cl = np.array(data['Cl'])
cd = np.array(data['Cd'])
alpha = np.array(data['Alpha'])

## Calculations 

## Calculate the center of gravity of the aircraft

# Define points of mass
# Treat the "fuselage" tubes as massless

m_prop = 47 + 24 # mass of motor and mount, grams
x_prop = 0

m_wing = 18 + 16*4 + 31 # mass of servos and wing pla, grams
x_wing = np.linspace(0.05, 0.25, 100) # distance from propeller to wing, meters

m_tail = 18 + 16*2 + 31# mass of servos and tail pla, grams
x_tail = np.linspace(0.75, 1.5, 100) # distance from propeller to tail, meters

x_cm = np.zeros((len(x_wing), len(x_tail)))

for i, xw in enumerate(x_wing):
  for j, xt in enumerate(x_tail):
    cm = (m_prop*x_prop + m_wing*x_wing[i] + m_tail*x_tail[j]) / (m_prop + m_wing + m_tail) # center of mass
    x_cm[i, j] = cm

m_total = m_prop + m_wing + m_tail

W_min = (m_total/1000) * 9.81 # minimum weight of the aircraft (N)

#######################################################################################################
################################# Main Wing Body Calculations #########################################
#######################################################################################################

# for 1 to 40 m/s
velocity = np.arange(1, 45, 1)
trim_alpha = np.arange(-5, 6, .25)
# print(trim_alpha)
# print(np.where(trim_alpha == 5)[0])
lift_w_arr = []
drag_w_arr = []
L_D_w_arr = []

# Loop over trim_alpha and velocity to calculate lift_w and drag_w
for a in trim_alpha:
  lift_w_values = []
  drag_w_values = []
  if a in alpha:
    index_a = np.where(alpha == a)[0][0]
    for v in velocity:
      # Calculate lift_w and drag_w at this velocity and angle of attack
      lift_w = 0.5 * rho * v**2 * S_w * cl[index_a]
      drag_w = 0.5 * rho * v**2 * S_w * cd[index_a]
      # Append lift_w and drag_w values to the respective lists
      lift_w_values.append(lift_w)
      drag_w_values.append(drag_w)
      L_D_w_value = (lift_w / drag_w)
  else:
    # If the angle of attack is not in alpha, append zeros or handle appropriately
    lift_w_values = [0] * len(velocity)
    drag_w_values = [0] * len(velocity)
    L_D_w_value = 0
  # Append the list of lift_w and drag_w values for this trim_alpha to the main lists
  lift_w_arr.append(lift_w_values)
  drag_w_arr.append(drag_w_values)
  L_D_w_arr.append(L_D_w_value)

# Convert lists to numpy arrays for easier manipulation and analysis
lift_w_arr = np.array(lift_w_arr)
drag_w_arr = np.array(drag_w_arr)
L_D_w_arr = np.array(L_D_w_arr)


#######################################################################################################
######################################### Tail Calculations ###########################################
#######################################################################################################

lift_t_arr = []
drag_t_arr = []
L_D_t_arr = []

# Loop over trim_alpha and velocity to calculate lift_w and drag_w
for a in trim_alpha:
  lift_t_values = []
  drag_t_values = []
  if a in alpha:
    index_a = np.where(alpha == a)[0][0]
    for v in velocity:
      # Calculate lift_w and drag_w at this velocity and angle of attack
      lift_t = 0.5 * rho * v**2 * S_t * cl[index_a]
      drag_t = 0.5 * rho * v**2 * S_t * cd[index_a]
      # Append lift_w and drag_w values to the respective lists
      lift_t_values.append(lift_t)
      drag_t_values.append(drag_t)
      L_D_t_value = (lift_t / drag_t)
  else:
    # If the angle of attack is not in alpha, append zeros or handle appropriately
    lift_t_values = [0] * len(velocity)
    drag_t_values = [0] * len(velocity)
    L_D_t_value = 0
  # Append the list of lift_w and drag_w values for this trim_alpha to the main lists
  lift_t_arr.append(lift_t_values)
  drag_t_arr.append(drag_t_values)
  L_D_t_arr.append(L_D_t_value)

# Convert lists to numpy arrays for easier manipulation and analysis
lift_t_arr = np.array(lift_t_arr)
drag_t_arr = np.array(drag_t_arr)
L_D_t_arr = np.array(L_D_t_arr)


#######################################################################################################
###################################### Stability Calculations #########################################
#######################################################################################################

## Constants

# lw ==> distance from cg to wing aerodynamic center
# lt ==> distance from cg to tail aerodynamic center
lw = np.zeros((len(x_wing), len(x_tail)))
lt = np.zeros((len(x_wing), len(x_tail)))

for i in range(len(x_wing)):
  xw = x_wing[i]
  for j in range(len(x_tail)):
    ltval = x_tail[j] - x_cm[i,j] - ((c/4)*.0254) # distance from cg to tail aerodynamic center (meters)
    lt[i,j] = ltval

    if xw > x_cm[i,j]:
      lwval = xw - x_cm[i,j] + ((c/4)*.0254)
    elif xw < x_cm[i,j]:
      lwval = x_cm[i,j] - xw - ((c/4)*.0254)
    else:
      lwval = 0
    lw[i,j] = lwval

trim_alpha_w = 5  # Trim angle of attack for the wing (degrees)

# Calculations

## Physical restraint: i_t = 0 - can't mount precise enough
# so find l_w and l_t that give the stability when i_t is close to zero

# Loop over lw and lt to calculate the stability at 10 m/s

M = np.zeros((len(x_wing), len(x_tail)))

for i in range(len(x_wing)):
  for j in range(len(x_tail)):
    lwval = lw[i,j]
    ltval = lt[i,j]
    # Calculate the moment about the center of gravity

    if x_wing[i] > x_cm[i,j]:
      M_w = lwval * lift_w_arr[np.where(trim_alpha == trim_alpha_w)[0][0], np.where(velocity == 10)[0][0]] * -1
    elif x_wing[i] < x_cm[i,j]:
      M_w = lwval * lift_w_arr[np.where(trim_alpha == trim_alpha_w)[0][0], np.where(velocity == 10)[0][0]]
    else:
      M_w = 0; 

    M_t = ltval * lift_t_arr[np.where(trim_alpha == trim_alpha_w)[0][0], np.where(velocity == 10)[0][0]] * -1

    # Append the moment to the main list
    M[i,j] = M_w + M_t

# Find the lw and lt values that give the stability when i_t is close to zero
for i, momentarr in enumerate(M):
  wingpos = x_wing[i]
  for j, moment in enumerate(momentarr):
    tailpos = x_tail[j]
    if -0.0001 < moment < 0.0001:
      print(f"xw: {wingpos}, xt: {tailpos}, M: {moment}")
    
    
#######################################################################################################
########################################## Plotting Data ##############################################
#######################################################################################################

###### AIRFOIL DATA ######

# Plotting Cl vs Alpha
plt.figure(figsize=(10, 6))
plt.plot(alpha, cl, marker='o', linestyle='-', color='b', label='Cl')
plt.title('lift_w Coefficient (Cl) vs Angle of Attack (Alpha)')
plt.xlabel('Alpha (degrees)')
plt.ylabel('Cl')
plt.grid(True)
plt.legend()
plt.savefig('plots/Cl_vs_Alpha.png')
plt.close()

# Plotting Cd vs Alpha
plt.figure(figsize=(10, 6))
plt.plot(alpha, cd, marker='o', linestyle='-', color='r', label='Cd')
plt.title('drag_w Coefficient (Cd) vs Angle of Attack (Alpha)')
plt.xlabel('Alpha (degrees)')
plt.ylabel('Cd') 
plt.grid(True)
plt.legend()
plt.savefig('plots/Cd_vs_Alpha.png')
plt.close()

###### MAIN WING DATA ######

# Plot L/D vs trim alpha for 20 m/s
plt.figure(figsize=(10, 6))
plt.plot(trim_alpha, L_D_w_arr, marker='o', linestyle='-', color='g')
plt.title('lift_w-to-drag_w Ratio (L/D) vs Trim Angle of Attack for 10 m/s')
plt.xlabel('Trim Alpha (degrees)')
plt.ylabel('L/D')
plt.grid(True)
plt.savefig('plots/L_D_w_vs_TrimAlpha_10ms.png')
plt.close()

# Plot lift_w vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, lift_w_arr[np.where(trim_alpha == 5)[0][0]], marker='o', linestyle='-', color='b')
plt.plot(velocity, [W_min]*len(velocity), marker='o', linestyle='-', color='r', label='Weight Estimate')
plt.title('lift_w vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('lift_w (N)')
plt.grid(True)
plt.legend()
plt.savefig('plots/lift_w_vs_Velocity_5deg.png')
plt.close()

# Plot drag_w vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, drag_w_arr[np.where(trim_alpha == 5)[0][0]], marker='o', linestyle='-', color='b')
plt.title('drag_w vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('drag_w (N)')
plt.grid(True)
plt.savefig('plots/drag_w_vs_Velocity_5deg.png')
plt.close()

###### TAIL DATA ######

# Plot L/D vs trim alpha for 20 m/s
plt.figure(figsize=(10, 6))
plt.plot(trim_alpha, L_D_t_arr, marker='o', linestyle='-', color='g')
plt.title('lift_t-to-drag_t Ratio (L/D) vs Trim Angle of Attack for 10 m/s')
plt.xlabel('Trim Alpha (degrees)')
plt.ylabel('L/D')
plt.grid(True)
plt.savefig('plots/L_D_t_vs_TrimAlpha_10ms.png')
plt.close()

# Plot lift_t vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, lift_t_arr[np.where(trim_alpha == 5)[0][0]], marker='o', linestyle='-', color='b')
plt.title('lift_t vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('lift_t (N)')
plt.grid(True)
plt.savefig('plots/lift_t_vs_Velocity_5deg.png')
plt.close()

# Plot drag_t vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, drag_t_arr[np.where(trim_alpha == 5)[0][0]], marker='o', linestyle='-', color='b')
plt.title('drag_t vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('drag_t (N)')
plt.grid(True)
plt.savefig('plots/drag_t_vs_Velocity_5deg.png')
plt.close()

###### STABILITY DATA ######

# Plot M vs x_wing and x_tail for 10m/s as a heatmap
plt.figure(figsize=(10, 6))
plt.imshow(M, cmap='coolwarm', interpolation='nearest')
plt.colorbar()
locsx, labelsx = plt.xticks()
print(labelsx)
locsy, labelsy = plt.yticks()
plt.yticks(locsx, [0, round(x_tail[0], 2), round(x_tail[19], 2), round(x_tail[39], 2), round(x_tail[59], 2), round(x_tail[79], 2), round(x_tail[99], 2)])
plt.xticks(locsy, [0, round(x_wing[0], 2), round(x_wing[19], 2), round(x_wing[39], 2), round(x_wing[59], 2), round(x_wing[79], 2), round(x_wing[99], 2)])
plt.title('Moment (M) vs x_wing and x_tail for 10 m/s')
plt.xlabel('x_wing')
plt.ylabel('x_tao;')
plt.grid(True)
plt.savefig('plots/M_vs_x_wing_x_tail_10ms.png')
plt.close()