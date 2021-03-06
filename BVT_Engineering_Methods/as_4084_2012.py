# -*- coding: utf-8 -*-
"""AS_4084:2012.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PtShxcSmikA2D3reW-M33Esrv-1JsiuT

#AS_4084:2012.py function library

This method references the following standard: AS 4084:2012, for Steel storage racking

Method developed 23 June 2022 (c) BVT Consulting Ltd

Developed - SB

Reviewed -

05.07.2022 - v 1.0 - Released for use in BVT Selective/Pallet Racking Performance Function. Sections 4.2.2.2(a), 4.2.2.4(a),(b),(c), 4.2.2.5(a) added

# Section 4 Design Procedures

## 4.2 Design Criteria

###4.2.2 Design based on linear or global nonlinear structural analysis

#### 4.2.2.2 Design based on global nonlinear structural analysis considering the down-aisle direction

Alternative method (a) is used:
> $l_e = L$

where $L$ is the height between beam levels

Eq. 4.2.2.2 and alternative method (b) are not currently covered.
"""

def Clause_4_2_2_2a_post_le_down_aisle_GNA(L, down_aisle_bracing):
  # le = L whether rack is unbraced or braced in down aisle
  if down_aisle_bracing is 'unbraced' or down_aisle_bracing is 'braced':
    le = L
  else:
    le = 'Error: "down_aisle_bracing" input should be either "unbraced" or "braced"'

  return le

"""####4.2.2.4 Design based on global nonlinear structural analysis considering the cross aisle direction

Alternative methods a,b,c are covered:

(a) For the bottom length of an upright in a braced upright frame, $l_e = 0.9L$, where $L$ is the height from the floor to the second node point, provided that -
>(i) the bracing members of the upright frame are connected to both flanges of the upright;

>(ii) the bracing eccentricities satisfy the requirements of Clause 3.3.2.6 (this assumption is met if each brace meets the next at a node, or if braces are spaced by maximum $1.5*post depth$) ;

>(iii) a baseplate is fitted to the upright; and

>(iv) the floor is concrete

otherwise $l_e=L$

(b) For all other parts of the upright, $l_e=L$, where $l$ is the distance between brace nodes.

(c) For horizontal and dioagonal bracing members in an upright frame, provided the bracing member is welded with a minimum fillet length of 20 mm to both flanges of the uprights, for in plane buckling, $le=0.9L$. For all opther cases, $l_e=L$.

"""

def Clause_4_2_2_4ab_post_le_across_aisle_GNA(bottom_brace_height, brace_spacing, is_below_second_brace_node, is_bracing_eccentricity_low, is_floor_concrete, is_baseplate_fitted):
  if is_floor_concrete is True and is_baseplate_fitted is True and is_bracing_eccentricity_low is True:
    # alternative (a) applies
    if is_below_second_brace_node is True:
      le = 0.9*(bottom_brace_height+brace_spacing)
    else: 
      le = brace_spacing
  
  else:
    # alternative (b) applies
    le = brace_spacing

  return le

def Clause_4_2_2_4c_brace_le_across_aisle_GNA(brace_welds_longer_than_20mm, brace_length):
  # alternative (c) for brace effective length
  if brace_welds_longer_than_20mm == True:
    le = 0.9*brace_length
  else:
    le = brace_length
  
  return le

"""#### 4.2.2.5 Effective length for torsional buckling of uprights

Only alternative (a) is considered. 

Alternative (b) allows for the torsional buckling length of posts to be halved where braces provide full torsional and warping restraint. This condition does not apply to most racks with bolted braces, but will apply to some racks with welded braces. This is disregarded for conservativeness and simplicity.

The input, brace sapcing, is the distance between brace nodes for the part of the post in question.
"""

def Clause_4_2_2_5a_post_le_torsional(brace_spacing):
  le = brace_spacing
  return le
