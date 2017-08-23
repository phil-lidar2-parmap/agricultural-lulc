__version__ = "0.4"

import os
import sys
import csv
import time
import shutil
import argparse
import logging
import arcpy

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
lulc_gdb = r"E:\PARMAP_10K\10K LULC Layers.gdb\LULC_Database"

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
			logger.exception("%s: Error encountered", f)
			spamwriter.writerow([f, path, file_extension, "Duplicate"])

# calculate for area and delete unnecessary fields
for shp in os.listdir(output_directory):
	if shp.endswith(".shp"):
		drop_fields = ["SHAPE_Leng", "SHAPE_Area"]
		shp_path = os.path.join(output_directory, shp)
		quad = shp.split("_LULC",1)[0]
		try:
			logger.info("%s: Calculating area for each geometry", quad)
			arcpy.CalculateField_management(shp_path, "AREA", "!shape.area@squaremeters!", "PYTHON_9.3")

			logger.info("%s: Deleting unnecessary fields", quad)
			arcpy.DeleteField_management(shp_path,drop_fields)

			logger.info("%s: Updating LULC Database", quad)
			expression = "quadname = '{0}'".format(quad)
			arcpy.MakeFeatureLayer_management(lulc_gdb, "lulc_gdb_layer", expression)
			arcpy.CalculateField_management("lulc_gdb_layer", "is_renamed", '"Y"', "PYTHON_9.3")
			arcpy.Delete_management("lulc_gdb_layer")
			
		except Exception:
			logger.exception("%s: Error encountered", shp)

endTime = time.time()  # End timing
print '\nElapsed Time:', str("{0:.2f}".format(round(endTime - startTime,2))), 'seconds'
