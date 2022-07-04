# -*- coding: utf-8 -*-
"""BRANZ_Seismic_Design_of_High_Level_Storage_Racking_Systems_in_Areas_with_Public_Access_2006.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S2MhYhmKqOaxXM5rOSAdRnlMHyTDLBoj

This method references the following design guide: BRANZ Seismic Design og High Level Storage Racking Systems with Public Access

Method developed 05 July 2022 (c) BVT Consulting Ltd

Developed - SB

Reviewed -

05.07.2022 - SB - DRAFT Sections 3.1.3 added

# Section 3 Rack Design

## 3.1 Applicable design standards

### 3.1.3 Gravity load from shelf contents

This section specifies the load combination factors to be applied to the live load ($Q$) when it is used in seismic load combinations.

For the cross-aisle direction, racking systems must be designed using a $\psi_c$ of 1.0 and for the down-aisle drirection, a figure of 0.6 may be used
"""

# define psi_c combination factors
Section_3_1_3_psi_c_across = 1.0
Section_3_1_3_psi_c_down = 0.6

"""#### 3.1.4 Seismic weight

The equation given here to calculate seismic weight is used.

The area reduction factor, $\psi_E$, is taken as 1.0 for across-aisle and 0.8 for down-aisle.

The rigid mass factor, $\psi_M$, is taken as 0.67. An option is also provided to not use the rigid mass factor.
"""

def Section_3_1_4_seismic_weight(Gi,Qi,direction, use_rigid_mass_factor):
  # assign psi_E based on direction
  if direction == 'across':
    psi_E = 1.0
  elif direction == 'down':
    psi_E = 0.8
  else:
    print('ERROR - direction must be "across" or "down"')
    psi_E = 'ERROR - direction must be "across" or "down"'
  
  # assign psi_M based on whether use_rigid_mass_factor input is True
  if use_rigid_mass_factor == True:
    psi_M = 0.67
  elif use_rigid_mass_factor == False:
    psi_M = 1
  else:
    print('ERROR - use_rigid_mass_factor must be True or False')
    psi_M = 'ERROR - use_rigid_mass_factor must be True or False'

  # calculate seismic weight
  Wi = Gi + psi_E*psi_M*Qi

  return Wi