#!/usr/bin/env python
# coding: utf-8

# # AS 1170.2:2021 method
# 
# This method references the following standard:
# NZS 1170.4:2021, for New Zealand structures.
# 
# Method developed 23 January 2023
# (c) BVT Consulting Ltd
# 
# Developer - Nima Shokrollahi

# In[1]:


import pandas as pd
import numpy as np


# ## Site wind speed

# ![image.png](attachment:image.png)

# ### Regional wind speeds ($V_R$)

# In[2]:



table3_1_b = pd.DataFrame([
['Akaroa','A7',],
['Alexandra','A7',],
['Arrowtown','A7',],
['Arthurs Pass','A7',],
['Ashburton','A7',],
['Auckland','A6',],
['Balclutha','A7',],
['Blenheim','A7',],
['Bluff','A7',],
['Bulls','A7',],
['Cambridge','A6',],
['Cheviot','A7',],
['Christchurch','A7',],
['Cromwell','A7',],
['Dannevirke','A7',],
['Darfield','A7',],
['Dargaville','A6',],
['Dunedin','A7',],
['Eastbourne - Point Howard','A7',],
['Fairlie','A7',],
['Fielding','A7',],
['Fox Glacier','A7',],
['Foxton/Foxton Beach','A7',],
['Franz Josef','A7',],
['Geraldine','A7',],
['Gisborne','A7',],
['Gore','A7',],
['Greymouth','A7',],
['Hamilton','A7',],
['Hanmer Springs','A7',],
['Harihari','A7',],
['Hastings','A7',],
['Hawera','A7',],
['Hokitika','A7',],
['Huntly','A7',],
['Hutt Valley - south of Taita Gorge','A7',],
['Inglewood','A7',],
['Invercargill','A7',],
['Kaikohe','A6',],
['Kaikoura','A7',],
['Kaitaia','A6',],
['Kawerau','A7',],
['Levin','A7',],
['Manukau City','A6',],
['Mangakino','A7',],
['Marton','A7',],
['Masterton','A7',],
['Matamata','A7',],
['Mataura','A7',],
['Milford Sound','A7',],
['Morrinsville','A7',],
['Mosgiel','A7',],
['Motueka','A7',],
['Mount Maunganui','A7',],
['Mt Cook','A7',],
['Murchison','A7',],
['Murupara','A7',],
['Napier','A7',],
['Nelson','A7',],
['New Plymouth','A7',],
['Ngaruawahia','A7',],
['Oamaru','A7',],
['Oban','A7',],
['Ohakune','A7',],
['Opotiki','A7',],
['Opunake','A7',],
['Otaki','A7',],
['Otira','A7',],
['Otorohanga','A7',],
['Paeroa','A6',],
['Pahiatua','A7',],
['Paihia/Russell','A7',],
['Palmerston ','A7',],
['Palmerston North','A7',],
['Paraparaumu','A7',],
['Patea','A7',],
['Picton','A7',],
['Porirua','A7',],
['Pukekohe','A7',],
['Putaruru','A7',],
['Queenstown','A7',],
['Raetihi','A7',],
['Rangiora','A7',],
['Reefton','A7',],
['Riverton','A7',],
['Rotorua','A7',],
['Ruatoria','A7',],
['Seddon','A7',],
['Springs Junction','A7',],
['St Arnaud','A7',],
['Stratford','A7',],
['Taihape','A7',],
['Takaka ','A7',],
['Taumarunui','A7',],
['Taupo','A7',],
['Tauranga','A7',],
['Te Anau','A7',],
['Te Aroha','A6',],
['Te Awamutu','A7',],
['Te Kuiti','A7',],
['Te Puke','A7',],
['Temuka','A7',],
['Thames','A6',],
['Timaru','A7',],
['Tokoroa','A7',],
['Turangi','A7',],
['Twizel','A7',],
['Upper Hutt','A7',],
['Waihi','A6',],
['Waikanae','A7',],
['Waimate','A7',],
['Wainuiomata','A7',],
['Waiouru','A7',],
['Waipawa','A7',],
['Waipukurau','A7',],
['Wairoa','A7',],
['Waitara','A7',],
['Waiuku','A6',],
['Wanaka','A7',],
['Wanganui','A7',],
['Ward','A7',],
['Warkworth','A6',],
['Wellington','W',],
['Wellington CBD','W',],
['Westport','A7',],
['Whakatane','A7',],
['Whangarei','A6',],
['Winton','A7',],
['Woodville','A7',]],
columns = ["Location","Wind Region"]                       
)


#table3_1_b


# ## Wind region speeds

# In[3]:


table3_1 = pd.DataFrame([
['1/25', 37, 37, 43],
['1/50', 39, 39, 45],
['1/100', 41, 41, 47],
['1/200', 43, 43, 49],
['1/250', 43, 43, 49],
['1/500', 45, 45, 51],
['1/1000', 46, 46, 53],
['1/2000', 48, 48, 54],
['1/2500', 48, 48, 55]],
columns = ["V value", "A6", "A7", "W"]
)


# In[4]:


def location_wind_region(location):
    return table3_1_b[table3_1_b["Location"] == location]["Wind Region"].values[0]

def wind_region_speed(p, location):
    location_region = location_wind_region(location)
    return table3_1[table3_1["V value"] == p][location_region].values[0]


# In[5]:


#Vr = wind_region_speed(1/50, "Auckland")
#Vr


# ### Terrain/height Multiplier ($M_zcat$)

# ![image.png](attachment:image.png)

# In[6]:


Table4_1 = pd.DataFrame([
    [3, 0.99, 0.95, 0.91, 0.87, 0.83, 0.75],
    [5, 1.05, 0.98, 0.91, 0.87, 0.83, 0.75],
    [10, 1.12, 1.06, 1, 0.915, 0.83, 0.75],
    [15, 1.16, 1.05, 1.05, 0.97, 0.89, 0.75],
    [20, 1.19, 1.135, 1.08, 1.01, 0.94, 0.75],
    [30, 1.22, 1.17, 1.12, 1.06, 1, 0.8],
    [40, 1.24, 1.2, 1.16, 1.1, 1.04, 0.85],
    [50, 1.25, 1.215, 1.18, 1.125, 1.07, 0.9],
    [75, 1.27, 1.245, 1.22, 1.17, 1.12, 0.98],
    [100, 1.29, 1.265, 1.24, 1.2, 1.16, 1.03],
    [150, 1.31, 1.29, 1.27, 1.24, 1.21, 1.11],
    [200, 1.32, 1.305, 1.29, 1.265, 1.24, 1.16]],
    columns = ["Height", "TC1", "TC1.5", "TC2", "TC2.5", "TC3", "TC4"]
)

#Table4_1
    


# In[7]:


def interpolation(height):
    indices = Table4_1['Height'].searchsorted([height], side='right')
    lower_bound_index = indices[0] - 1
    upper_bound_index = indices[0] if indices[0] != len(Table4_1) else indices[0] - 1
    height_low = Table4_1['Height'][lower_bound_index]
    height_high = Table4_1['Height'][upper_bound_index]
    interpolation_hn = (height - height_low) / (height_high - height_low)
    return interpolation_hn, lower_bound_index, upper_bound_index

def Mz_cat(height, Terrain_category):
    if height <= 3:
        Mz_cat = Table4_1[Terrain_category][0]
    else:
        interpolation_height, lower_bound_index, upper_bound_index = interpolation(height)
        mz_cat_low = Table4_1[Terrain_category][lower_bound_index]
        mz_cat_high = Table4_1[Terrain_category][upper_bound_index]
        Mz_cat = mz_cat_low + interpolation_height * (mz_cat_high - mz_cat_low)
    
    return Mz_cat
    


# ### Calculate site wind

# In[9]:


def site_wind_speed(p, location, height, Terrain_category):
    
    Md = 1.0 #wind_direction_multiplier
    Ms = 1.0 #shielding_multiplier
    Mh = 1.0 #hill_multiplier
    elevation_multiplier = 1.0
    Mlee = 1.0 #lee_multiplier
    Mt = 1.0 #topographic_multiplier
    
    Vr = wind_region_speed(p, location)
    Mz_cat_value = Mz_cat(height, Terrain_category)
    v_site = Vr * Md * (Mz_cat_value * Ms * Mt)
    return v_site


# In[10]:


#v_site = site_wind_speed(1/1000, "Auckland", 20, "TC2")
#print("site_wind:", v_site)


# ### Calculate wind pressure

# In[ ]:


def calc_wind_pressure(v_site):
    
    partition_overall_pressure_factor = 0.4
    #Density of air (kg/m3)
    rho_air = 1.2
    #Partition and building assumed not to be dynamically sensitive
    wind_dynamic_response_factor = 1.0
    
    wind_pressure = 0.5 * rho_air * (v_site**2) * partition_overall_pressure_factor * wind_dynamic_response_factor
    return wind_pressure

