# Windows

__version__ = "0.1.1"

import os
import sys
import csv
import time
import argparse
from datetime import datetime

print sys.version
startTime = time.time()

list_quads = []

# output CSV file
log_file = "logs_duplicates" + ".csv"
csvfile = open(log_file, 'wb')
spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(["Filename", "Path", "Remarks"])

input_directory = r"F:\PARMap_10K_Shapefiles\SUC"
output_directory = r"F:\PARMap_10K_Shapefiles\10K"

for path, dirs, files in os.walk(input_directory,topdown=False):
	for f in sorted(files):
		if f.endswith(".shp"):
			list_quads.append(f)

for path, dirs, files in os.walk(input_directory,topdown=False):
	for f in sorted(files):
		if f.endswith(".shp"):
			if list_quads.count(f) == 1:
				print list_quads.count(f)
				spamwriter.writerow([f,path,"Distinct"])		
			else:
				print list_quads.count(f)
				spamwriter.writerow([f,path,"Duplicate"])
endTime = time.time()  # End timing
print '\nElapsed Time:', str("{0:.2f}".format(round(endTime - startTime,2))), 'seconds'