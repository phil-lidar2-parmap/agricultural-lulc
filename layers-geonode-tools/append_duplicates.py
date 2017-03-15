# Windows
# ArcPy

__version__ = "0.1.1"

import arcpy
import os
import sys
import csv
import time
import argsparse
from datetime import datetime

print sys.version
startTime = time.time()

parser = argparse.ArgumentParser(description='Remove duplicates of Agri Maps')
parser.add_argument('-i','--input_directory')
args = parser.parse_args()

# output CSV file
log_file = "logs_" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ".csv"
csvfile = open(log_file, 'wb')
spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(["Source", "Destination", "Date Created", "Remarks"])

input_directory = args.input_directory()
output_directory = r"F:\PARMap_10K_Shapefiles\10K"

for path, dirs, files in os.walk(input_directory,topdown=False):
	for f in sorted(files):
		if f.endswith(".shp"):
			src_file = os.path.join(path,f)
			dst_file = os.path.join(output_directory,f).replace(".shp","_PARMAP.shp")
			print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]",\
			"SOURCE:", src_file
			print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]",\
			"DESTINATION:", dst_file

			try:
				if os.path.exists(dst_file):
					#append
					print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]",\
					"Appending features"
					arcpy.Append_management(src_file, dst_file, "TEST")
					spamwriter.writerow([src_file, dst_file, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Append"])
					print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]",\
					"Done appending"
				else:
					print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]",\
					"Copying features"
					#copy to new folder
					arcpy.CopyFeatures_management(src_file, dst_file)
					spamwriter.writerow([src_file, dst_file, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Copy"])
					print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]",\
					"Done copying"
			except Exception, err:
					print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]",\
					err
					spamwriter.writerow([src_file, dst_file, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Error"])
			print "\n#####################################################################\n"
csvfile.close()
endTime = time.time()  # End timing
print '\nElapsed Time:', str("{0:.2f}".format(round(endTime - startTime,2))), 'seconds'