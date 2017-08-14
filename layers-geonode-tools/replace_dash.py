__version__ = "0.1"
import os

input_directory = raw_input("Input directory:")
if os.path.exists(input_directory):
	for path, dirs, files in os.walk(input_directory,topdown=False):
		for f in files:
			if "-" in f:
				try:
					src = file_path = os.path.join(path,f)
					dst = file_path = os.path.join(path,f.replace("-","_"))
					print "SRC :" + src
					print "DST :" + dst
					os.rename(src,dst)
				except Exception, e:
					print "Error in renaming: " + src
else:
	print "Directory does not exist"

raw_input('\nPress ENTER to exit...')
