# import the geocoding services you'd like to try
from geopy.geocoders import ArcGIS, Bing, Nominatim, OpenCage, GoogleV3, OpenMapQuest
import csv, sys
import pandas as pd
import keys

in_file = 'C:/OPTMODELS/ZIPGEO/data/data.csv'    #str(sys.argv[1])
out_file = 'C:/OPTMODELS/ZIPGEO/output/gctester_data.csv' #str(sys.argv[2])
timeout = 100       #int(sys.argv[3])

print('creating geocoding objects.')

arcgis = ArcGIS(timeout=timeout)
bing = Bing(api_key=keys.bing_key,timeout=100)
nominatim = Nominatim(user_agent=keys.n_user, timeout=timeout)
#opencage = OpenCage(api_key=keys.oc_api,timeout=timeout)
#googlev3 = GoogleV3(api_key=keys.g3_api, domain='maps.googleapis.com', timeout=timeout)
#openmapquest = OpenMapQuest(api_key=keys.omq_api, timeout=timeout)

# choose and order your preference for geocoders here
geocoders = [bing, nominatim, arcgis]

def gc(address):
    street = str(address['address'])
    city = str(address['city'])
    state = str(address['state'])
    zip = str(address['zip'])
    country = str(address['country'])
    add_concat = street + ", " + city + ", " + state + " " + zip + " " + country
    for gcoder in geocoders:
        location = gcoder.geocode(add_concat)
        if location != None:
            print(f'geocoded record {address.name}: {street}')
            located = pd.Series({
                'lat': location.latitude,
                'lng': location.longitude,
                'time': pd.to_datetime('now')
            })
        else:
            print(f'failed to geolocate record {address.name}: {street}')
            located = pd.Series({
                'lat': 'null',
                'lng': 'null',
                'time': pd.to_datetime('now')
            })
        return located

print('opening input.')
reader = pd.read_csv(in_file, header=0)
print('geocoding addresses.')
reader = reader.merge(reader.apply(lambda add: gc(add), axis=1), left_index=True, right_index=True)
print(f'writing to {out_file}.')
reader.to_csv(out_file, encoding='utf-8', index=False)
print('done.')