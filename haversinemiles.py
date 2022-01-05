from math import radians, sin, cos, sqrt, asin


def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8  # Earth radius in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c

## haversine(36.12, -86.67, 33.94, -118.40)
## 2887.2599506071106

d=haversine(32.23, -80.86, 35.1, -90.00)    #kilometers
havmiles = round(d / 1.609344, 1)                  #miles
hhgmiles = 605.0
havfactor= round(hhgmiles / havemiles,4)

print("Haversine Distance in miles is ", havmiles, " miles.")
print("HavFactor                   is ", havfactor)

# "Haversine Distance in miles is "; Format(d, "#.######"); " km ("; Format(d / 1.609344, "#.######"); " miles)."

#Zip3MilesID	Zip3MilesCode	FromZip3	ToZip3	Miles	Note	FromLat	FromLon	Expr1	ToLat	ToLon	Country
#100299381	299_381	299	381	605		32.23	-80.86	US	35.1	-90	US