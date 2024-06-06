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
i_t = 0  # Incidence angle of the tail (degrees)

W_est = 7 # Estimated weight of the aircraft (N)

cl = np.array(data['Cl'])
cd = np.array(data['Cd'])
alpha = np.array(data['Alpha'])

## Calculations 

#######################################################################################################
################################# Main Wing Body Calculations #########################################
#######################################################################################################

# for 1 to 40 m/s
velocity = np.arange(1, 41, 1)
trim_alpha = np.arange(-5, 6, .25)
lift_w_arr = []
drag_w_arr = []
L_D_w_arr = []

# Loop over trim_alpha and velocity to calculate lift_w and drag_w
for a in trim_alpha:
  lift_w_values = []
  drag_w_values = []
  L_D_w_values = []
  if a in alpha:
    index_a = np.where(alpha == a)[0][0]
    for v in velocity:
      # Calculate lift_w and drag_w at this velocity and angle of attack
      lift_w = 0.5 * rho * v**2 * S_w * cl[index_a]
      drag_w = 0.5 * rho * v**2 * S_w * cd[index_a]
      # Append lift_w and drag_w values to the respective lists
      lift_w_values.append(lift_w)
      drag_w_values.append(drag_w)
      L_D_w_values.append(lift_w / drag_w)
  else:
    # If the angle of attack is not in alpha, append zeros or handle appropriately
    lift_w_values = [0] * len(velocity)
    drag_w_values = [0] * len(velocity)
    L_D_w_values = [0] * len(velocity)
  # Append the list of lift_w and drag_w values for this trim_alpha to the main lists
  lift_w_arr.append(lift_w_values)
  drag_w_arr.append(drag_w_values)
  L_D_w_arr.append(L_D_w_values)

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
  L_D_t_values = []
  if a in alpha:
    index_a = np.where(alpha == a)[0][0]
    for v in velocity:
      # Calculate lift_w and drag_w at this velocity and angle of attack
      lift_t = 0.5 * rho * v**2 * S_t * cl[index_a]
      drag_t = 0.5 * rho * v**2 * S_t * cd[index_a]
      # Append lift_w and drag_w values to the respective lists
      lift_t_values.append(lift_t)
      drag_t_values.append(drag_t)
      L_D_t_values.append(lift_t / drag_t)
  else:
    # If the angle of attack is not in alpha, append zeros or handle appropriately
    lift_t_values = [0] * len(velocity)
    drag_t_values = [0] * len(velocity)
    L_D_t_values = [0] * len(velocity)
  # Append the list of lift_w and drag_w values for this trim_alpha to the main lists
  lift_t_arr.append(lift_t_values)
  drag_t_arr.append(drag_t_values)
  L_D_t_arr.append(L_D_t_values)

# Convert lists to numpy arrays for easier manipulation and analysis
lift_t_arr = np.array(lift_t_arr)
drag_t_arr = np.array(drag_t_arr)
L_D_t_arr = np.array(L_D_t_arr)

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

# Plot L/D vs trim alpha for 10 m/s
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
plt.plot(velocity, lift_w_arr[20], marker='o', linestyle='-', color='b')
plt.plot(velocity, [W_est]*len(velocity), marker='o', linestyle='-', color='r', label='Weight Estimate')
plt.title('lift_w vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('lift_w (N)')
plt.grid(True)
plt.legend()
plt.savefig('plots/lift_w_vs_Velocity_5deg.png')
plt.close()

# Plot drag_w vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, drag_w_arr[20], marker='o', linestyle='-', color='b')
plt.title('drag_w vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('drag_w (N)')
plt.grid(True)
plt.savefig('plots/drag_w_vs_Velocity_5deg.png')
plt.close()

###### TAIL DATA ######

# Plot L/D vs trim alpha for 10 m/s
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
plt.plot(velocity, lift_t_arr[20], marker='o', linestyle='-', color='b')
plt.title('lift_t vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('lift_t (N)')
plt.grid(True)
plt.savefig('plots/lift_t_vs_Velocity_5deg.png')
plt.close()

# Plot drag_t vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, drag_t_arr[20], marker='o', linestyle='-', color='b')
plt.title('drag_t vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('drag_t (N)')
plt.grid(True)
plt.savefig('plots/drag_t_vs_Velocity_5deg.png')
plt.close()

