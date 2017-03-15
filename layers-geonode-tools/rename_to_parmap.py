# Windows

__version__ = "0.1"

import os
import shutil
from datetime import datetime

input_dir = r"F:\PARMap_10K_Shapefiles\SUC\UPMIN"
output_dir = r"F:\PARMap_10K_Shapefiles\10K"

for path, dirs, files in os.walk(input_dir):
	for f in files:
		src_file = os.path.join(path,f)
		quad_name = f.split(".",1)[0]
		file_extension = f.split(".",1)[1]
		# print "file", f
		# print "quad name", quad_name
		# print "extension", file_extension
		print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]"\
		"src:", src_file
		dst_file = os.path.join(output_dir, quad_name + "_PARMAP." + file_extension)
		print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]"\
		"dst:", dst_file
		shutil.copy(src_file,dst_file)
