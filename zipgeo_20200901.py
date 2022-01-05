#!/usr/bin/python

"""
Sean MacDermant   Python 3.8   2020-08-18
zipgeo takes a .csv file ("AnyID","address","city","state","zip","country")  and adds some additional fields
it geocodes at a high level first (by zip5) then continues on to use API's to geocode at the street address level
"""

import pandas as pd
from uszipcode import SearchEngine
import os, sys
from keys import n_user, bing_key, oc_key
from geopy.geocoders import ArcGIS, Bing, Nominatim, OpenCage  # import geocoding services / # NOMINATIM requires no key
#if cmd line doesn't for you do (from CMD as Administrator, with python path in your %PATH%):
#  python -m pip install pandas
#  python -m pip install uszipcode
#  python -m pip install geopy
arcgis = ArcGIS(timeout=100)
bing = Bing(bing_key,timeout=100)
nominatim = Nominatim(user_agent=n_user, timeout=100)
opencage = OpenCage(oc_key, timeout=100)
#geocoderDotUS = GeocoderDotUS(timeout=100) #googlev3 = GoogleV3(timeout=100) #openmapquest = OpenMapQuest(timeout=100)

# choose and order your preference for geocoders here
geocoders = [bing, nominatim, arcgis]

# set up your search on uszipcode library
search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database

# set input / # set current working directory
currentdir = os.getcwd()  # 'C:/OPTMODELS/zipgeo'
print(currentdir)


filename = 'iploc.csv'  # 'anydata.csv'
if len(sys.argv) - 1 >= 1:
    filename = str(sys.argv[1])  # 'iploc.csv'

# str(sys.argv[1])   #'anydata.csv'  'big.csv'  'data1.csv'
in_file = currentdir + '/data/' + filename  # e.g. 'kents_fiber_facs.csv'
timeout = 100

def zipgeoandapigeo():

    #The right way to load a dataset with ZIP codes into a DataFrame
    #df_zip_proper = pandas.io.parsers.read_csv('zip/sample.csv', dtype={'zip': 'str'})
#
    anydata = pd.io.parsers.read_csv(in_file, dtype={'zip': 'str'})
    anydata = anydata.applymap(lambda x: x.strip() if isinstance(x, str) else x)     #strips leading and trailing spaces
    anydata['newzip'] = anydata['zip'].str[:5]    #this is left(x,5)
    anydata['newzip'] = anydata['newzip'].str.pad(width=4, side='right', fillchar='0')    #put '01' on end if needed
    anydata['newzip'] = anydata['newzip'].str.pad(width=5, side='right', fillchar='1')    #put '01' on end if needed

    #Replace all NaN elements in column ‘A’, ‘B’, ‘C’, and ‘D’, with 0, 1, 2, and 3 respectively.
    #>>>values = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    #>>> df.fillna(value=values)

    values = {'address': '123 MAIN ST.'}
    anydata.fillna(value=values)
    ##anydata.fillna(value=values)

    print(anydata.head(7))

    clnzipcol = anydata['newzip'].values.tolist()

    latitudes = []
    longitudes = []
    cities = []
    statuses = []
    geozips = []

    for datapoint in clnzipcol:
         result = search.by_zipcode(datapoint)

         if result:                         #and len(result) removed
             longitude = result.lng         #result[0]['geometry']['lng']
             latitude = result.lat         #result[0]['geometry']['lat']
             city = result.city
             status = "ZIP5_uszipcode"
             geozip = result.zipcode

         else:
             longitude = "NaN"
             latitude = "NaN"
             city = "NaN"
             status = "NaN"
             geozip = "NaN"

         latitudes.append(latitude)
         longitudes.append(longitude)
         cities.append(city)
         statuses.append(status)
         geozips.append(geozip)

    clndata = anydata

    clndata["ziplat"] = latitudes
    clndata["ziplon"] = longitudes
    clndata["zip_geo_city"] = cities
    clndata["zip_status"] = statuses
    clndata["zgeozip"] = geozips

    out_file = currentdir + '/output/' + 'zgeo_' + filename  # e.g. 'zgeo_kents_fiber_facs.csv'
    clndata.to_csv(out_file)

    apidata = clndata

    apidata = apidata.merge(apidata.apply(lambda add: gc(add), axis=1), left_index=True, right_index=True)

    out_file = currentdir + '/output/' + 'apig_' + filename     #e.g. 'apig_kents_fiber_facs.csv'
    apidata.to_csv(out_file, encoding='utf-8', index=False)
    print(apidata.head(7))




def gc(address):
    street = str(address['address'])
    city = str(address['city'])
    state = str(address['state'])
    zip = str(address['zip'])
    #country = str(address['country'])
    add_concat = street + ", " + city + ", " + state + " " + zip #+ " " + country
    for gcoder in geocoders:
        location = gcoder.geocode(add_concat)
        if location != None:
            #print(f'geocoded record {address.name}: {street}')
            located = pd.Series({
                'lat': location.latitude,
                'lon': location.longitude,
                'time': pd.to_datetime('now')
            })
        else:
            #print(f'failed to geolocate record {address.name}: {street}')
            located = pd.Series({
                'lat': 'null',
                'lon': 'null',
                'time': pd.to_datetime('now')
            })
        return located



def run():
    ### DEBUG STUFF       ### Looking for Chicago and IL,  and PHILLY, PA but entered wrong spelling.
    res = search.by_city_and_state("cicago", "il")
    print("cicago, il  --> " + res[0].major_city + ", " + res[0].state_abbr + "  " + res[0].zipcode)
    res = search.by_city_and_state("PHILLY", "PA")
    print("PHILLY, PA  --> " + res[0].major_city + ", " + res[0].state_abbr + "  " + res[0].zipcode)
    res = search.by_city_and_state("ILLADELPHIA", "PA")
    print("ILLADELPHIA, PA  --> " + res[0].major_city + ", " + res[0].state_abbr + "  " + res[0].zipcode)
    ###
    print("This script has the name %s" % (sys.argv[0]))

    zipgeoandapigeo()


if __name__ == '__main__':
    run()
    sys.exit(0)
