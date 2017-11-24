__version__ = "0.2.1"

import os
import csv
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_directory")
parser.parse_args()
args = parser.parse_args()

cwd = args.input_directory
if cwd.endswith("/"):
    bname = cwd.split("/")[-2]
else:
    bname = cwd.split("/")[-1]

csv_name = "list_{0}.csv".format(bname)
csv_file = open(csv_name, 'wb')
spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Path', 'File', 'File Extension'])

for path, dirs, files in os.walk(cwd,topdown=True):
    for f in sorted(files):
        file_path = os.path.join(path,f)
        print file_path

        if path.endswith("gdb"):
            gdb_file = os.path.basename(path)
            gdb_path = os.path.dirname(path)
            spamwriter.writerow([gdb_path, gdb_file, "gdb"])
            break

        else:
            try:
                file_extn = f.split(".",1)[1]
            except Exception:
                file_extn = ""
            spamwriter.writerow([path, f, file_extn])

csv_file.close()
