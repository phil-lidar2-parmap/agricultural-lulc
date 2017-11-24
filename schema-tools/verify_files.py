__version__ = "0.3.2"

import os
import csv
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_directory")
parser.parse_args()
args = parser.parse_args()

def verify_vector(shp):
    cmd = "ogrinfo -al " + shp + " | grep POLYGON"
    try:
        proc = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception:
        return 1

def verify_raster(ds):
    cmd = "gdalinfo -checksum " + ds
    try:
        proc = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception:
        return 1

cwd = args.input_directory
if cwd.endswith("/"):
    bname = cwd.split("/")[-2]
else:
    bname = cwd.split("/")[-1]

csv_name = "verify_{0}.csv".format(bname)
csv_file = open(csv_name, 'wb')
spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Path', 'File', 'File Extension', "Is Corrupted"])

for path, dirs, files in os.walk(cwd,topdown=True):
    for f in sorted(files):
        file_path = os.path.join(path,f)

        if f.endswith(".shp"):
            print file_path
            file_extn = f.split(".",1)[1]
            return_code = verify_vector(file_path)
            spamwriter.writerow([path, f, file_extn, return_code])

        elif f.__contains__(".tif") or f.__contains__('.jpg'):
            print file_path
            file_extn = f.split(".",1)[1]
            return_code = verify_raster(file_path)
            spamwriter.writerow([path, f, file_extn, return_code])

        else:
            pass
csv_file.close()
