import csv
import time
import sys
from pygeocoder import Geocoder

filename = '..\data\LocalLaw4420140404\ProjectBuilding20140404.txt'
with open(filename, 'rb') as input_file:
    first_line = input_file.readline()
    header = first_line.strip('\r\n').split('|')

    rows = []
    for line in input_file:
        rows.append(line.strip('\r\n').split('|'))

with open('ProjectBuilding20140404.csv', 'wb') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)
    writer.writerows(rows)