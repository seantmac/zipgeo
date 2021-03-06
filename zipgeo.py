# Sean MacDermant   Python 3.8   2020-08-18 - 2020-09-01       #
# zipgeo.py takes a .csv file with 6 fields and geocodes it
# *by zipcode* first; then via api and address.
# ("AnyID","address","city","state","zip","country")

import pandas as pd
from uszipcode import SearchEngine
import os
import sys
from keys import n_user, bing_key, oc_key
# import geocoding services / # NOMINATIM requires no key
from geopy.geocoders import ArcGIS, Bing, Nominatim, OpenCage

# initialize everything
arcgis = ArcGIS(timeout=100)
bing = Bing(bing_key,timeout=100)
nominatim = Nominatim(user_agent=n_user, timeout=100)
opencage = OpenCage(oc_key, timeout=100)

# choose and order your geocoders in preference order
geocoders = [bing, nominatim, arcgis]
search = SearchEngine(simple_zipcode=True)

# set input directory and filename
currentdir = os.getcwd()
filename = 'fibrtest.csv'
if len(sys.argv) - 1 >= 1:
    filename = str(sys.argv[1])
in_file = currentdir + '/data/' + filename
timeout = 100


def zipgeo():
    anydata = pd.io.parsers.read_csv(in_file, dtype={'zip': 'str'})
    # trim spaces
    anydata = anydata.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # left 5-char
    anydata['newzip'] = anydata['zip'].str[:5]    #this is left(x,5)
    # if it's a Zip3 add '01'
    anydata['newzip'] = anydata['newzip'].str.pad(width=4, side='right', fillchar='0')
    anydata['newzip'] = anydata['newzip'].str.pad(width=5, side='right', fillchar='1')
    # fill missing address with 123 MAIN ST.
    anydata.fillna(value={'address': '123 MAIN ST.'}, inplace = True)

    clnzipcol = anydata['newzip'].values.tolist()

    latitudes = []
    longitudes = []
    cities = []
    statuses = []
    geozips = []

    for datapoint in clnzipcol:
         #this is the search for the location using the zipcode
         result = search.by_zipcode(datapoint)

         if result:
             longitude = result.lng
             latitude = result.lat
             city = result.city
             status = "ZIP5_USZC"
             geozip = result.zipcode
         else:
             longitude = ""
             latitude = ""
             city = ""
             status = ""
             geozip = ""

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

    out_file = currentdir + '/output/' + 'zgeo_' + filename
    clndata.to_csv(out_file)

    apidata = clndata
    apidata = apidata.merge(apidata.apply(lambda add: gc(add), axis=1), left_index=True, right_index=True)

    # load columns from dataframe
    lat = apidata['lat']
    lon = apidata['lon']

    # define latitude/longitude for function *AND* # add new column with generated zip-code
    azipdf = pd.DataFrame({'lat': lat, 'lon': lon})

    # debug: 'get_zipcode can choke on nulls
    #         Springfield, MO, the birthplace of Route 66 and population centroid of USA
    #         lat=37.210388 lon=-93.297256 zip='63001'
    azipdf.fillna(value={'lat': ' 37.210388'}, inplace = True)  #SPRINGFIELD MO
    azipdf.fillna(value={'lon': '-93.297256'}, inplace = True)  #SPRINGFIELD MO

    #print(azipdf)

    # get zipcode from lat/lon
    azipdf['zipcode'] = azipdf.apply(lambda x: get_zipcode(x.lat, x.lon), axis=1)
    apidata['azip'] = azipdf['zipcode'].values
    apidata['newzip'].fillna(apidata['azip'])   #missing newZips get API ZIPCODE Lkp

    # delete unneeded columns
    del apidata['time']
    del apidata['zgeozip']
    del apidata['zip_status']   # # zip_geo_city too?

    # write the output file
    out_file = currentdir + '/output/' + 'apig_' + filename
    apidata.to_csv(out_file, encoding='utf-8', index=False)


#define get_zipcode search function
def get_zipcode(lat, lon):
    if lat is not None and lon is not None:
        result = search.by_coordinates(lat, lon, radius=2, returns=3)
        if result:
            return result[0].zipcode
        else:
            return '63001'
    else:
        return '63001'


#define gc, the api geocoding function
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
    zipgeo()


if __name__ == '__main__':
    run()
    sys.exit(0)
