__version__ = "0.2.1"

import os
import sys
import csv
import time
import shutil
import argparse
import logging

# Parse arguments
parser = argparse.ArgumentParser(description='Renaming distinct LULC shapefiles')
parser.add_argument('-i','--input_directory')
parser.add_argument('-o','--output_directory')
args = parser.parse_args()
startTime = time.time()

LOG_FILENAME = "rename_distinct.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.ERROR, format='%(asctime)s: %(levelname)s: %(message)s')

logger = logging.getLogger("rename_distinct.log")
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

list_quads = []

# output CSV file
log_file = "rename_distinct.csv"
csvfile = open(log_file, 'wb')
spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(["Filename", "Path", "FileExt", "Remarks"])

input_directory = args.input_directory
output_directory = args.output_directory

for path, dirs, files in os.walk(input_directory,topdown=False):
	for f in sorted(files):
		list_quads.append(f)

for path, dirs, files in os.walk(input_directory,topdown=False):
	for f in sorted(files):
		quad_name = f.split(".",1)[0]
		file_extension = f.split(".",1)[1]
		logger.info("%s: Counting the number of occurrences", f)
		try:
			if list_quads.count(f) == 1:
				logger.info("%s: Renaming the shapefile", f)
				src = os.path.join(path,f)
				dst = os.path.join(output_directory, quad_name + "_LULC." + file_extension)
				shutil.move(src,dst)
				spamwriter.writerow([f, path, file_extension, "Distinct"])
			else:
				logger.info("%s: Found duplicate values", f)
				spamwriter.writerow([f, path, file_extension, "Duplicate"])

		except Exception:
			logger.exception("Error encountered")
			spamwriter.writerow([f, path, file_extension, "Duplicate"])

endTime = time.time()  # End timing
print '\nElapsed Time:', str("{0:.2f}".format(round(endTime - startTime,2))), 'seconds'
