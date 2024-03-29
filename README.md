# BVT_Engineering_Methods
Python function libraries for common engineering and construction standards.

Currently we have methods in development for:
- AS/NZS 4600 2018 - comprehensive
- AS/NZS 1170.0 2002 - Reference tables for project level parameters, load combinations and unities
- NZS 1170.5 2004 - Section 3, section 5 (equivalent static method, section 8
- AS 4084 2012 - just started

A quick "how-to":

1. You can pip install all the standard function libraries into python as follows:
```python
!pip install git+https://github.com/BVT-Engineering/BVT_Engineering_Methods.git
```
2. Then import into your routines the standards you want to reference:
```python
from BVT_Engineering_Methods import nzs_1170_5 as NZS_1170_5
```
Finally, in your code, clauses from the standard can be called like this:
```python
CpTp = NZS_1170_5.part_design_response_coefficient(subsoil_type,Z,R,N_TD,C_Hi,CiTp)
```
This provides a readable method, while simplifying the code calculation checks.
