zipgeo
===============================

zipgeo is a super simple geocoding command line program
to quickly and easily get and validate location information
and geocode (add lat/lon) and write the output file

1. zipgeo takes an input csv file of locations in the form:

  "AnyID","address","city","state","zip","country"
  1,"179 SPANISH POINT DR", "BEAUFORT",  "SC", "29902","USA"
  2,"274 BIRCH DR",         "LAUREL BAY","SC", "29902","USA"
  3,"2026 SE ELLIOTT",      "PORTLAND",  "OR", "97214-0001","USA"
  4,"2026 SE ELLIOTT",      "PORTLAND",  "OR", "970",  "USA"
  5,"2026 SE ELLIOTT",      "PORTLAND",  "OR", "97214","USA"

It's best with full data and ZIPs, though attempts are made 
to clean up or trim zips to use in ZIP5 format.

US-ONLY for now.

It is a two step process after cleaning

	1]  get the lat/lon (or average lat/lon) for the zipcode or city/state etc.
	2]  get the refined address-level lat/lon via api from web


Geocode Module returns such information as: 
* country, 
* address,
* zip (postal-code),


zipgeo release history
===============================

2020-08-18  First Release
2020-
2020-
2020-


zipgeo punchlist
===============================

0  Insert the lookup to get the zipcode if it's missing (like "PHILLY" or "PHILADELPHIA")
1  "Handle" Mexico and Canada; first with Mexican State and Canadian Province
2  Add some decent logging options describing the processing and results  (https://realpython.com/python-logging/)
2c Can it be forgiving of fieldnames allow POSTALCODE for 'zip' or default to usual order and don't sweat the names, ok?
3  Make it work from a single string like "179 SPANISH POINT DR, BEAUFORT, SC  29902"
4  Make it work from command line a la:  python zipgeo.py "C:/OPTMODELS/ZIPGEO/data/anydata.csv" "C:/OPTMODELS/ZIPGEO/output/zgeo_anydata.csv" 100
5       where 100 is the timeout
6  Trap errors due to missing API key or other API error
7  remove keys and user_id's to keys.py
8  add reverse geocoding?
9  make it deal with any number of fields in any order, ignoring but keeping extras (see school_bad.csv)
10 make it an option to do both zip-geocoding (at zip5 level) or 'api-geocoding (address level) [SLOW] or both


zipgeo other info
===============================

What to test on:
  IF CANADA RETURN PROVINCE GEO DATA
  IF MEXICO RETURN STATE DATA

  SQL SERVER:	S02ASQLP102
  DB:		BMOS
  TABLE:		tblCAFE_ZipCode

  geocode("380 New York Street, Redlands, CA 92373")
  geocode("380", "New York Street", "Redlands", "CA", "92373")

   geocode("Redlands, CA")
   geocode("Redlands", "CA")
   geocode("38117")
   geocode("29902", "USA")
   geocode("MOSCOW", "USA")
   geocode("PARIS", "USA")
   geocode("PARIS", "TN", "USA")
   geocode(“Jacksonville”)
   geocode(“philllllllllllladelphis”



zipgeo how to use it
===============================
#if cmd line doesn't for you do (from CMD as Administrator, with python path in your %PATH%):
#  python -m pip install pandas
#  python -m pip install uszipcode
#  python -m pip install geopy


more
===============================
    # GeocoderDotUS inactivated for error       # OpenMapQuest  inactivated for error       # GoogleV3
    # Nice example on GitHub here: https://gist.github.com/ericrobskyhuntley/0c293113aa75a254237c143e0cf962fa
    # Another One:  https://gist.github.com/rgdonohue/c4beedd3ca47d29aef01


