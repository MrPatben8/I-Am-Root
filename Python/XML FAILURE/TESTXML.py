#TEST FILE XML

from xml.dom import minidom

mydoc = minidom.parse ("temperatura2014-xml.xml")

lugar = mydoc.getElementsByTagName("precipitacion")

print("Lugar #2 attribute: ")
print(lugar[1].attributes["ap"].value)

 