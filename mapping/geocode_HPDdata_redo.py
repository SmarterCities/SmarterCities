import csv
import time
import sys
from pygeocoder import Geocoder

filename = 'ProjectBuilding20140404_geocoded.csv'
with open(filename, 'rb') as input_file:
    info = csv.reader(input_file)
    header = info.next()
    istreet = header.index('StreetName')
    inumber = header.index('HouseNumber')
    iboro = header.index('BoroID')
    ilat = header.index('Lat')
    ilon = header.index('Lon')
    newrows = []
    k = 0
    for row in info:
        #print row[iboro]
        if row[istreet] != 'N/A' and row[ilat] == '':
            if row[iboro] == '1':
                city = 'New York'
            elif row[iboro] == '2':
                city = 'Bronx'
            elif row[iboro] == '3':
                city = 'Brooklyn'
            elif row[iboro] == '4':
                city = 'Queens'
            elif row[iboro] == '5':
                city = 'Staten Island'
            else:
                city = 'NaN'
            address = row[inumber] + ' ' + row[istreet] + ', ' + city + ', NY'
            try:
                result = Geocoder.geocode(address)
                time.sleep(.5)
                if len(result) == 1:
                    row[ilon] = result.coordinates[0]
                    row[ilat] = result.coordinates[1]
                    newrows.append(row)
                else:
                    print 'more than one geolocation found for ' + address
                    #row.append(result[0].coordinates[0])
                    #row.append(result[0].coordinates[1])
                    newrows.append(row)
            except:
                k = k + 1
                row.append(None)
                row.append(None)
                newrows.append(row)
                continue
        else:
            newrows.append(row)
    
nname = filename[:-4] + "_redone.csv" # The filename of the output file

with open(nname, "wb") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)
    writer.writerows(newrows)

#with open('ProjectBuilding20140404_geocoded.csv', 'wb') as output_file:
#    writer = csv.writer(output_file)
#    writer.writerow(header)
#    writer.writerows(rows)