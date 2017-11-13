import os
import shutil
import time
import logging
import argparse
import csv

# Parse arguments
parser = argparse.ArgumentParser(description='Renaming LULC shapefiles')
parser.add_argument('-i','--input_directory')
parser.add_argument('-o','--output_directory')
args = parser.parse_args()
startTime = time.time()

LOG_FILENAME = "rename_lulc.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.ERROR, format='%(asctime)s: %(levelname)s: %(message)s')

logger = logging.getLogger("rename_lulc.log")
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

csv_file = open("rename_lulc.csv", 'wb')
spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Source', 'Destination', 'Remarks'])

input_directory = args.input_directory
output_directory = args.output_directory

file_count = sum([len(files) for r, d, files in os.walk(input_directory)])

logger.info("Total number of files: %s" % file_count)
file_count_ctr = 0

for path, dirs, files in os.walk(input_directory,topdown=False):
    for f in sorted(files):
        if f.__contains__('.'):
            try:
                ctr = 0
                file_count_ctr += 1
                src = os.path.join(path,f)
                logger.info("SRC: %s" %src)
                quad_name = f.split(".",1)[0].lower()
                file_extension = f.split(".",1)[1].lower()
                new_quad_name = quad_name + "_lulc"
                dst = os.path.join(output_directory, new_quad_name + "." + file_extension)

                # Check if output filename is already exists
                while os.path.exists(dst):
                    ctr += 1
                    new_quad_name = quad_name + "_lulc_" + str(ctr)
                    dst = os.path.join(output_directory, new_quad_name + "." + file_extension)

                logger.info("DST: %s" %dst)
                logger.info("Renaming file: {0}.{1} ({2}/{3})".format(quad_name, file_extension, file_count_ctr, file_count))
                shutil.copy(src,dst)
                spamwriter.writerow([src, dst])
            except Exception, e:
                spamwriter.writerow([src, dst, "Error"])
                logger.exception("Error in renaming %s" % quad_name)

csv_file.close()
endTime = time.time()  # End timing
print '\nElapsed Time:', str("{0:.2f}".format(round(endTime - startTime,2))), 'seconds'

