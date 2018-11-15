from opencage.geocoder import OpenCageGeocode

key = '51df2f36d3fc4952a3d460f8fa3a1993'

geocoder = OpenCageGeocode(key)

query = 'Julia Bernstein 913, La Reina, Santiago, Chile'
ret = geocoder.geocode(query)
print(ret[0]['geometry']['lat'])
print(ret[0]['geometry']['lng'])




#pa instalar: terminal-> new terminal -> pip install opencage