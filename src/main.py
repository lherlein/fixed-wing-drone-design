import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data from CSV file
file_path = 'xf-naca4412-il-1e6.csv'  # Replace with your actual file path
data = pd.read_csv(file_path, skiprows=10)

## Constants

rho = 1.225  # Air density (kg/m^3)
b = 0.762  # Wing span (m)
c = 0.1016  # Chord length (m)
S = b * c  # Wing area (m^2)
AR = b**2 / S  # Aspect ratio

W_est = 7 # Estimated weight of the aircraft (N)

cl = np.array(data['Cl'])
cd = np.array(data['Cd'])
alpha = np.array(data['Alpha'])

## Calculations 

#######################################################################################################
################################# Main Wing Body Calculations #########################################
#######################################################################################################

# for 1 to 20 m/s
velocity = np.arange(1, 41, 1)
trim_alpha = np.arange(-5, 6, .25)
lift_arr = []
drag_arr = []
L_D_arr = []

# Loop over trim_alpha and velocity to calculate lift and drag
for a in trim_alpha:
  lift_values = []
  drag_values = []
  L_D_values = []
  if a in alpha:
    index_a = np.where(alpha == a)[0][0]
    for v in velocity:
      # Calculate Lift and Drag at this velocity and angle of attack
      lift = 0.5 * rho * v**2 * S * cl[index_a]
      drag = 0.5 * rho * v**2 * S * cd[index_a]
      # Append lift and drag values to the respective lists
      lift_values.append(lift)
      drag_values.append(drag)
      L_D_values.append(lift / drag)
  else:
    # If the angle of attack is not in alpha, append zeros or handle appropriately
    lift_values = [0] * len(velocity)
    drag_values = [0] * len(velocity)
    L_D_values = [0] * len(velocity)
  # Append the list of lift and drag values for this trim_alpha to the main lists
  lift_arr.append(lift_values)
  drag_arr.append(drag_values)
  L_D_arr.append(L_D_values)

# Convert lists to numpy arrays for easier manipulation and analysis
lift_arr = np.array(lift_arr)
drag_arr = np.array(drag_arr)
L_D_arr = np.array(L_D_arr)



#######################################################################################################
########################################## Plotting Data #############################################
#######################################################################################################

# Plotting Cl vs Alpha
plt.figure(figsize=(10, 6))
plt.plot(alpha, cl, marker='o', linestyle='-', color='b', label='Cl')
plt.title('Lift Coefficient (Cl) vs Angle of Attack (Alpha)')
plt.xlabel('Alpha (degrees)')
plt.ylabel('Cl')
plt.grid(True)
plt.legend()
plt.savefig('plots/Cl_vs_Alpha.png')
plt.close()

# Plotting Cd vs Alpha
plt.figure(figsize=(10, 6))
plt.plot(alpha, cd, marker='o', linestyle='-', color='r', label='Cd')
plt.title('Drag Coefficient (Cd) vs Angle of Attack (Alpha)')
plt.xlabel('Alpha (degrees)')
plt.ylabel('Cd') 
plt.grid(True)
plt.legend()
plt.savefig('plots/Cd_vs_Alpha.png')
plt.close()

# Plot L/D vs trim alpha for 10 m/s
plt.figure(figsize=(10, 6))
plt.plot(trim_alpha, L_D_arr, marker='o', linestyle='-', color='g')
plt.title('Lift-to-Drag Ratio (L/D) vs Trim Angle of Attack for 10 m/s')
plt.xlabel('Trim Alpha (degrees)')
plt.ylabel('L/D')
plt.grid(True)
plt.savefig('plots/L_D_vs_TrimAlpha_10ms.png')
plt.close()

# Plot Lift vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, lift_arr[20], marker='o', linestyle='-', color='b')
plt.plot(velocity, [W_est]*len(velocity), marker='o', linestyle='-', color='r', label='Weight Estimate')
plt.title('Lift vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Lift (N)')
plt.grid(True)
plt.legend()
plt.savefig('plots/Lift_vs_Velocity_5deg.png')
plt.close()

# Plot Drag vs velocity for trim alpha = 5 degrees
plt.figure(figsize=(10, 6))
plt.plot(velocity, drag_arr[20], marker='o', linestyle='-', color='b')
plt.title('Drag vs Velocity for Trim Alpha = 5 degrees')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Drag (N)')
plt.grid(True)
plt.savefig('plots/Drag_vs_Velocity_5deg.png')
plt.close()
