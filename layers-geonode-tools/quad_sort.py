__version__ = "0.2."

import shutil
import os
import time

startTime = time.time()

# parameters
input_directory = '<input_directory>'
output_directory = '<input_directory>'
text_file = '<text_file>'

f = open(text_file,'r')
dst_folder = ""

instring = f.read()
quad_list =str(instring).split("\n")

for q in quad_list:
	for f in os.listdir(input_directory):
		if "*" in q:
			dst_folder = os.path.join(output_directory,q.replace("*",""))
		else:
			src_file = os.path.join(input_directory,f)
			dst_file = os.path.join(dst_folder,f)
			quad_name = f.split(".",1)[0]
			file_extension = f.split(".",1)[1]

			if quad_name == q:
				if not os.path.exists(dst_folder):
					os.makedirs(dst_folder)
				try:
					print "Copying:", src_file
					shutil.copy(src_file,dst_file)
					print "Successfully copied:", src_file
				except:
					print "Error in copying:", src_file

endTime = time.time()  # End timing
print '\nElapsed Time:', str("{0:.2f}".format(round(endTime - startTime,2))), 'seconds'
