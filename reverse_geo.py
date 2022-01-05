# Sean MacDermant   Python 3.8   2020-11-18 - 2020-11-18       #
# reverse_geo.py takes a .csv file with 3 fields and reverse_geocodes it
# ("AnyID","lat","lon")

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
filename = 'RgeoCMWY.CSV' #'RgeoFVE.CSV'
if len(sys.argv) - 1 >= 1:
    filename = str(sys.argv[1])
in_file = currentdir + '/data/' + filename
timeout = 100


def reverse_geo():
    anydata = pd.io.parsers.read_csv(in_file, dtype={'zip': 'str'})
    # trim spaces
    anydata = anydata.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # load columns from dataframe
    lat = anydata['lat']
    lon = anydata['lon']

    # define latitude/longitude for function *AND* # add new column with generated zip-code
    azipdf = pd.DataFrame({'lat': lat, 'lon': lon})
    azipdf['zipcode'] = azipdf.apply(lambda x: get_zipcode(x.lat, x.lon), axis=1)

    # write the output file
    out_file = currentdir + '/output/' + 'rgeo_' + filename
    azipdf.to_csv(out_file, encoding='utf-8', index=False)


#define get_zipcode search function
def get_zipcode(lat, lon):
    if lat is not None and lon is not None:
        result = search.by_coordinates(lat, lon, radius=9, returns=5)
        if result:
            return result[0].zipcode
        else:
            return '99999'
    else:
        return '99999'


def run():
    reverse_geo()


if __name__ == '__main__':
    run()
    sys.exit(0)



