#!/usr/bin/python
import os
import subprocess

cwd = os.getcwd()
raster_formats = ['jpg','tif','png']

for path, dirs, files in os.walk(cwd,topdown=False):
	for f in files:
		if f.endswith(".py"):
			pass
		else:
			inRaster = os.path.join(path,f)
			gdal_translate = r"gdal_translate -of JPEG -outsize 2339 3311"
			outputDir = os.path.join(path,"resampled")
			filename = os.path.splitext(os.path.basename(f))[0] + ".jpg"
			print "orig", f
			print "basename", filename
			if os.path.exists(outputDir):
				pass
			else:
				os.mkdir(outputDir)
			
			outRaster = os.path.join(path,"resampled",filename)

			cmd = " ".join([gdal_translate, inRaster, outRaster])
			print cmd
			#print "input", inRaster
			#print "output", outRaster
			subprocess.call(cmd, shell=True)

for x in os.listdir(outputDir):
	if x.endswith(".jpg"):
		pass
	else:
		os.remove(os.path.join(outputDir,x))

#gdal_translate -of JPEG -co COMPRESS=JPEG -outsize 2339 3311