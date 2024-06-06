# Personal Drone Calculations and Notes

## Drone Design

<img src="media/plane-render.png" alt="Rendering of Drone" width="400" height="240">

### Wing Body/Tail Design

- `b_w` = 2.5ft = .762m
- `c_bar` = 4in = .1016m
- `S_w` = .0774 m^2

**Airfoil**: NACA 4412 - plots at Re = 1e6

<p style="margin: 0;">
  <img src="plots/Cl_vs_Alpha.png" alt="Cl vs Alpha" width="400" height="240">
  <img src="plots/Cd_vs_Alpha.png" alt="Cd vs Alpha" width="400" height="240">
  <img src="plots/L_D_w_vs_TrimAlpha_10ms.png" alt="L/D for 10m/s vs trim alpha" width="400" height="240">
</p>

**Wing Body Plots**

<p style="margin: 0">
  <img src="plots/lift_w_vs_Velocity_5deg.png" alt="Wing lift vs Velocity at 5deg trim" width="400" height="240">
  <img src="plots/drag_w_vs_Velocity_5deg.png" alt="Drag lift vs Velocity at 5deg trim" width="400" height="240">
</p>

**Tail Plots**

<p style="margin: 0">
  <img src="plots/lift_t_vs_Velocity_5deg.png" alt="Wing lift vs Velocity at 5deg trim" width="400" height="240">
  <img src="plots/drag_t_vs_Velocity_5deg.png" alt="Drag lift vs Velocity at 5deg trim" width="400" height="240">
</p>


### 3d Printing and Design

<p style="margin: 0;">
  <img src="media/wing-block-ss.png" alt="wing-block" width="300" height="100">
  <img src="media/wing-body-connector-ss.png" alt="wing-body-connector" width="300" height="400">
</p>

## Dev Env Activation

`source env/bin/activate` - use local env

`deactivate` - use global env# fixed-wing-drone-design

## Process

Collecting my design process into one place

1. Pick wing body airfoil (NACA 4412)
2. Pick wing body aspect ratio (7.5)
3. Pick wing body chord length (`c_bar` = .1016m) (limited by 3d printer size and practical assembly restraints)
4. Calculate `b`, `S` from the two above values
5. Calculate L, D, L/D for V=[1,20] and trim_alpha=[-5,5.5]
6. Choose optimal trim_alpha from above calculations
7. Calculate Lift at trim from main wing body
8. Pick Tail airfoil (NACA 4412)
9. Pick Tail chord length/span length
10. Calculate lift from tail at trim - i_t