
#install non-standard dependencies

!pip install -q geopy

# basic utilities
import json
import requests
import pandas as pd

# reverse geocoding utilities
from geopy.geocoders import Nominatim

def location_lookup(search_string):

  geolocator = Nominatim(user_agent="address_details")
  location = geolocator.geocode(search_string)

  try:
    f'Address Match: {location.address}'
    f'Coordinates: {(location.latitude, location.longitude)}'
  except AttributeError:
    print("Sorry, we can't find that address. Please check you have the correct address details.")

  def map_query(longitude:float, latitude:float) -> dict:
    '''Query OpenStreetMap for a long/lat coordinate and return relevant metadata.'''
    url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1&namedetails=1'
    data = json.loads(requests.get(url).text)
    return data

  location_data = map_query(longitude=location.longitude, latitude=location.latitude)

  f'Address:       {location.address}'
  
  try: 
    council = location_data["address"]["county"]
  except KeyError:
    council = location_data["address"]["state"]

  table3_3 = pd.DataFrame([
  ['Akaroa',-43.8052059,172.9671548,0.3,20,'A7'],
  ['Alexandra',-45.2478653,169.3843692,0.21,20,'A7'],
  ['Arrowtown',-44.9424921,168.8283058,0.3,20,'A7'],
  ['Arthurs Pass',-42.9401564,171.5619826,0.6,12,'A7'],
  ['Ashburton',-43.905386,171.7447855,0.2,20,'A7'],
  ['Auckland',-36.8508827,174.7644881,0.13,20,'A7'],
  ['Balclutha',-46.2343847,169.7460167,0.13,20,'A7'],
  ['Blenheim',-41.513552,173.9597954,0.33,0,'A7'],
  ['Bluff',-46.597299,168.3302209,0.15,20,'A7'],
  ['Bulls',-40.1745609,175.3848623,0.31,20,'A7'],
  ['Cambridge',-37.8891864,175.466267,0.18,20,'A7'],
  ['Cheviot',-42.8130026,173.2739445,0.4,20,'A7'],
  ['Christchurch',-43.5320214,172.6305589,0.3,20,'A7'],
  ['Cromwell ',-45.0459401,169.1955689,0.24,20,'A7'],
  ['Dannevirke',-40.2102968,176.0942328,0.42,10,'A7'],
  ['Darfield',-43.4896243,172.1096996,0.3,20,'A7'],
  ['Dargaville',-35.9412883,173.8685647,0.1,20,'A7'],
  ['Dunedin',-45.8795455,170.5005957,0.13,20,'A7'],
  ['Eastbourne - Point Howard',-41.252852,174.9032883,0.4,4,'A7'],
  ['Fairlie',-44.0977299,170.8288521,0.24,20,'A7'],
  ['Fielding',-40.2277695,175.5658723,0.37,20,'A7'],
  ['Fox Glacier',-43.5285361,170.1540226,0.44,2,'A7'],
  ['Foxton/Foxton Beach',-40.4632238,175.2275964,0.36,20,'A7'],
  ['Franz Josef',-43.3873509,170.1833467,0.44,2,'A7'],
  ['Geraldine',-44.092301,171.2446573,0.19,20,'A7'],
  ['Gisborne',-38.6640913,178.0227931,0.36,20,'A7'],
  ['Gore',-46.1040833,168.9421444,0.18,20,'A7'],
  ['Greymouth',-42.4614253,171.1985024,0.37,20,'A7'],
  ['Hamilton',-37.7825893,175.2527624,0.13,20,'A7'],
  ['Hanmer Springs',-42.5255877,172.8289005,0.55,2,'A7'],
  ['Harihari',-43.1482215,170.5515074,0.46,4,'A7'],
  ['Hastings',-39.6302214,176.8304088,0.39,20,'A7'],
  ['Hawera',-39.5891194,174.2826385,0.18,20,'A7'],
  ['Hokitika',-42.7156909,170.9683049,0.45,20,'A7'],
  ['Huntly',-37.561486,175.1583585,0.15,20,'A7'],
  ['Hutt Valley - south of Taita Gorge',-41.1751124,174.9545312,0.4,0,'A7'],
  ['Inglewood',-39.15608,174.207926,0.17,20,'A7'],
  ['Invercargill',-46.4178708,168.3614659,0.18,20,'A7'],
  ['Kaikohe',-35.4059867,173.8032186,0.1,20,'A7'],
  ['Kaikoura',-42.3994483,173.6799111,0.42,12,'A7'],
  ['Kaitaia',-35.1088272,173.258714,0.1,20,'A7'],
  ['Kawerau',-38.086578,176.7036392,0.29,20,'A7'],
  ['Levin',-40.6218489,175.2866444,0.4,20,'A7'],
  ['Manukau City',-36.991461,174.8733999,0.13,20,'A7'],
  ['Mangakino',-38.3750149,175.7625779,0.21,20,'A7'],
  ['Marton',-40.0793203,175.3792768,0.3,20,'A7'],
  ['Masterton',-40.9463736,175.667234,0.42,6,'A7'],
  ['Matamata',-37.8084687,175.7709978,0.19,20,'A7'],
  ['Mataura',-46.1939524,168.8654783,0.17,20,'A7'],
  ['Milford Sound',-44.6414024,167.8973801,0.54,20,'A7'],
  ['Morrinsville',-37.6592693,175.5291308,0.18,20,'A7'],
  ['Mosgiel',-45.8739057,170.3475837,0.13,20,'A7'],
  ['Motueka',-41.1081429,173.0112377,0.26,20,'A7'],
  ['Mount Maunganui',-37.6646852,176.2080948,0.2,20,'A7'],
  ['Mt Cook',-43.5949749,170.1417883,0.38,20,'A7'],
  ['Murchison',-41.8000753,172.3254688,0.34,20,'A7'],
  ['Murupara',-38.4575344,176.7051193,0.3,20,'A7'],
  ['Napier',-39.5108848,176.8764428,0.38,20,'A7'],
  ['Nelson',-41.2985321,173.2443635,0.27,20,'A7'],
  ['New Plymouth',-39.0571533,174.0794082,0.18,20,'A7'],
  ['Ngaruawahia',-37.6674316,175.1467392,0.15,20,'A7'],
  ['Oamaru',-45.0965979,170.9714456,0.13,20,'A7'],
  ['Oban',-46.8978621,168.1284057,0.14,20,'A7'],
  ['Ohakune',-39.4185581,175.3996118,0.27,20,'A7'],
  ['Opotiki',-38.0122705,177.2871025,0.3,20,'A7'],
  ['Opunake',-39.4589862,173.8678942,0.18,20,'A7'],
  ['Otaki',-40.7603422,175.1576886,0.4,20,'A7'],
  ['Otira',-42.8316193,171.5612693,0.6,3,'A7'],
  ['Otorohanga',-38.1887897,175.2099072,0.17,20,'A7'],
  ['Paeroa',-37.375534,175.6678873,0.18,20,'A7'],
  ['Pahiatua',-40.4545624,175.8399893,0.42,8,'A7'],
  ['Paihia/Russell',-35.2821294,174.0910282,0.1,20,'A7'],
  ['Palmerston ',-45.485101,170.7147452,0.13,20,'A7'],
  ['Palmerston North',-40.3544628,175.6097478,0.38,8,'A7'],
  ['Paraparaumu',-40.915496,175.007312,0.4,14,'A7'],
  ['Patea',-39.7572286,174.4752973,0.19,20,'A7'],
  ['Picton',-41.2954812,174.0028153,0.3,16,'A7'],
  ['Porirua',-41.1380517,174.8472141,0.4,8,'A7'],
  ['Pukekohe',-37.2003745,174.9010498,0.13,20,'A7'],
  ['Putaruru',-38.0504692,175.7803993,0.21,20,'A7'],
  ['Queenstown',-45.0301511,168.6615141,0.32,20,'A7'],
  ['Raetihi',-39.4276874,175.2817814,0.26,20,'A7'],
  ['Rangiora',-43.3032326,172.5966281,0.33,20,'A7'],
  ['Reefton',-42.1195039,171.8622754,0.37,20,'A7'],
  ['Riverton',-46.3545151,168.0100598,0.2,20,'A7'],
  ['Rotorua',-38.1445987,176.2377669,0.24,20,'A7'],
  ['Ruatoria',-37.8898127,178.3191491,0.33,20,'A7'],
  ['Seddon',-41.6742775,174.0759237,0.4,6,'A7'],
  ['Springs Junction',-42.3345585,172.1817998,0.45,3,'A7'],
  ['St Arnaud',-41.8012348,172.8477475,0.36,2,'A7'],
  ['Stratford',-39.3379897,174.28411,0.18,20,'A7'],
  ['Taihape',-39.6762843,175.798292,0.33,20,'A7'],
  ['Takaka ',-40.8484812,172.8078325,0.23,20,'A7'],
  ['Taumarunui',-38.8832802,175.2563657,0.21,20,'A7'],
  ['Taupo',-38.6842862,176.0704465,0.28,20,'A7'],
  ['Tauranga',-37.7475768,176.1220183,0.2,20,'A7'],
  ['Te Anau',-45.4144293,167.7180426,0.36,20,'A7'],
  ['Te Aroha',-37.5431901,175.7123003,0.18,20,'A7'],
  ['Te Awamutu',-38.0087105,175.3210648,0.17,20,'A7'],
  ['Te Kuiti',-38.3380941,175.1672536,0.18,20,'A7'],
  ['Te Puke',-37.7841979,176.3264797,0.22,20,'A7'],
  ['Temuka',-44.2453676,171.2763124,0.17,20,'A7'],
  ['Thames',-37.1383356,175.5405213,0.16,20,'A7'],
  ['Timaru',-44.3903881,171.2372756,0.15,20,'A7'],
  ['Tokoroa',-38.220211,175.862693,0.21,20,'A7'],
  ['Turangi',-38.9905117,175.8109105,0.27,20,'A7'],
  ['Twizel',-44.2614837,170.0876398,0.27,20,'A7'],
  ['Upper Hutt',-41.1249326,175.0656426,0.42,2,'A7'],
  ['Waihi',-37.392753,175.841441,0.18,20,'A7'],
  ['Waikanae',-40.8786599,175.0641649,0.4,15,'A7'],
  ['Waimate',-44.732697,171.0480709,0.14,20,'A7'],
  ['Wainuiomata',-41.2625754,174.9471014,0.4,5,'A7'],
  ['Waiouru',-39.4772357,175.6683591,0.29,20,'A7'],
  ['Waipawa',-39.9415369,176.5896168,0.41,20,'A7'],
  ['Waipukurau',-39.9956348,176.5567213,0.41,20,'A7'],
  ['Wairoa',-39.0351747,177.4181452,0.37,20,'A7'],
  ['Waitara',-39.0022823,174.2353003,0.18,20,'A7'],
  ['Waiuku',-37.2576887,174.7336494,0.13,20,'A7'],
  ['Wanaka',-44.6942992,169.1417356,0.3,20,'A7'],
  ['Wanganui',-39.9330715,175.0286083,0.25,20,'A7'],
  ['Ward',-41.8294381,174.1311058,0.4,4,'A7'],
  ['Warkworth',-36.3970407,174.6605976,0.13,20,'A7'],
  ['Wellington ',-41.2923814,174.7787463,0.4,0,'W'],
  ['Wellington CBD (north of Basin Reserve)',-41.3003665,174.7803198,0.4,2,'W'],
  ['Westport',-41.7545797,171.6059512,0.3,20,'A7'],
  ['Whakatane',-37.9585311,176.9822259,0.3,20,'A7'],
  ['Whangarei',-35.7274938,174.3165604,0.1,20,'A7'],
  ['Winton',-46.1397899,168.3258061,0.2,20,'A7'],
  ['Woodville',-40.3370803,175.8667045,0.41,2,'A7']],
  columns = ["Location","Latitude","Longitude","Z","D","Wind Region"]                       
  )

  #Use sum of root squares to find closest town in table 3.3 from NZS1170.5

  lat_closest = abs(table3_3["Latitude"] - location.latitude)
  long_closest = abs(table3_3["Longitude"] - location.longitude)

  closest_srs = (lat_closest*lat_closest + long_closest*long_closest)**0.5
  closest_table3_3 = table3_3.loc[closest_srs.idxmin()]

  location_data['address']

  #Assemble function output
  #address = location_data['address']['house_number']+' '+location_data['address']['road']+', '+location_data['address']['suburb']+', '+location_data['address']['city']+' '+location_data['address']['postcode']
  council = council +' Council'
  Z,D = closest_table3_3.Z, closest_table3_3.D

  return {"Council":council,"Z factor": Z, "Near Fault Factor": D }