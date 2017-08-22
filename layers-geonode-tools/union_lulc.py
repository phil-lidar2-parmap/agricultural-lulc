__version__ = "0.3.2"
__authors__ = "Jok Laurente"
__email__ = ["jmelaurente@gmail.com"]
__description__ = 'Union of LULC shapefiles'

import arcpy
import os
import logging
import time
import argparse
import csv

startTime = time.time()

# Parse arguments
parser = argparse.ArgumentParser(description='Union of LULC shapefiles')
parser.add_argument('-i','--input_directory')
parser.add_argument('-o','--output_directory')
args = parser.parse_args()

LOG_FILENAME = "union_lulc.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.ERROR, format='%(asctime)s: %(levelname)s: %(message)s')

logger = logging.getLogger("union_lulc.log")
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

input_directory = args.input_directory
output_directory = args.output_directory

csv_file = open("union_lulc.csv", 'wb')
spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Quad', 'Path', 'Remarks'])

codeblock_union = """def getDominantValue(code1, code2):
	# create a list for lulc types
	coastal = ["46","47","49","52"]
	agri = ["08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26", "27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","51","55"]
	non_agri = ["01","02","03","04","05","06","07","44","45","48","50","53","54"]
	utype = code1
	if code1 <> code2:
		# objects that are in the same group will return 'SAME' value
		if code1 in coastal and code2 in coastal:
			# get nearest feature
			utype = "SAME"
		elif code1 in agri and code2 in agri:
			# get nearest feautre
			utype = "SAME"
		elif code1 in non_agri and code2 in non_agri:
			# get neartest feature
			utype = "SAME"
		# objects that differ from each other will get the dominant type
		elif code1 in coastal:
			utype = code1
		elif code2 in coastal:
			utype = code2
		elif code1 in agri:
			utype = code1
		elif code2 in agri:
			utype = code2
		elif code1 in non_agri:
			utype = code1
		elif code2 in non_agri:
			utype = code2
		else:
			utype = "00"
	return utype"""

codeblock_type = """def checkType(field1, field2, type1, type2, utype):
	ufield = field1
	if utype == type2:
		ufield = field2
	return ufield"""

def calculateOtherFields(layer):
	# calculate other fields
	arcpy.CalculateField_management(layer, "CLASSIFICA", "checkType(!CLASSIFICA!, !CLASSIFI_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "RESOURCE_T", "checkType(!RESOURCE_T!, !RESOURCE_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "ID_CLASS", "checkType(!ID_CLASS!, !ID_CLASS_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "MAIN_CLASS", "checkType(!MAIN_CLASS!, !MAIN_CLA_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "OTHER_CLAS", "checkType(!OTHER_CLAS!, !OTHER_CL_2!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "OTHER_CL_1", "checkType(!OTHER_CL_1!, !OTHER_CL_3!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "CLASS_DESC", "checkType(!CLASS_DESC!, !CLASS_DE_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "ID_TYPE", "checkType(!ID_TYPE!, !ID_TYPE_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "OTHER_TYPE", "checkType(!OTHER_TYPE!, !OTHER_TY_2!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "OTHER_TY_1", "checkType(!OTHER_TY_1!, !OTHER_TY_3!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "TYPE_DESCR", "checkType(!TYPE_DESCR!, !TYPE_DES_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "DATA_SOURC", "checkType(!DATA_SOURC!, !DATA_SOU_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "DATASET_AC", "checkType(!DATASET_AC!, !DATASET__1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "FARMING_SY", "checkType(!FARMING_SY!, !FARMING__1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "CROP_PLANT", "checkType(!CROP_PLANT!, !CROP_PLA_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "JAN", "checkType(!JAN!, !JAN_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "FEB", "checkType(!FEB!, !FEB_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "MAR", "checkType(!MAR!, !MAR_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "APR", "checkType(!APR!, !APR_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "MAY", "checkType(!MAY!, !MAY_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "JUN", "checkType(!JUN!, !JUN_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "JUL", "checkType(!JUL!, !JUL_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "AUG", "checkType(!AUG!, !AUG_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "SEP", "checkType(!SEP!, !SEP_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "OCT", "checkType(!OCT!, !OCT_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "NOV", "checkType(!NOV!, !NOV_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "DEC", "checkType(!DEC!, !DEC_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "REGION", "checkType(!REGION!, !REGION_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "PROVINCE", "checkType(!PROVINCE!, !PROVINCE_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "CITYMUNI", "checkType(!CITYMUNI!, !CITYMUNI_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "BARANGAY", "checkType(!BARANGAY!, !BARANGAY_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "REMARKS", "checkType(!REMARKS!, !REMARKS_1!, !MAIN_TYPE!, !MAIN_TYP_1!, !UTYPE!)", "PYTHON_9.3", codeblock_type)
	arcpy.CalculateField_management(layer, "MAIN_TYPE", "!UTYPE!", "PYTHON_9.3")
	arcpy.DeleteField_management(layer, ["CLASSIFI_1", "RESOURCE_1", "ID_CLASS_1", "MAIN_CLA_1", "OTHER_CL_2", "OTHER_CL_3", "CLASS_DE_1", "ID_TYPE_1", "MAIN_TYP_1", "OTHER_TY_2", "OTHER_TY_3", "TYPE_DES_1", "DATA_SOU_1", "DATASET__1", "FARMING__1", "CROP_PLA_1","JAN_1", "FEB_1", "MAR_1",
	"APR_1", "MAY_1", "JUN_1", "JUL_1", "AUG_1", "SEP_1", "OCT_1", "NOV_1", "DEC_1", "REGION_1", "PROVINCE_1", "CITYMUNI_1", "BARANGAY_1", "REMARKS_1", "AREA_1", "SHAPE_Leng", "SHAPE_Area", "SHAPE_Le_1", "SHAPE_Ar_1"])

def calculateJoinedFields(layer):
	# calculate other fields
	arcpy.CalculateField_management(layer,"MAIN_TYPE","!MAIN_TYP_1!","PYTHON_9.3")
	arcpy.CalculateField_management(layer, "CLASSIFICA", "!CLASSIFI_1!","PYTHON_9.3")
	arcpy.CalculateField_management(layer, "RESOURCE_T", "!RESOURCE_1!","PYTHON_9.3")
	arcpy.CalculateField_management(layer, "ID_CLASS", "!ID_CLASS_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "MAIN_CLASS", "!MAIN_CLA_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "OTHER_CLAS", "!OTHER_CL_2!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "OTHER_CL_1", "!OTHER_CL_3!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "CLASS_DESC", "!CLASS_DE_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "ID_TYPE", "!ID_TYPE_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "OTHER_TYPE", "!OTHER_TY_2!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "OTHER_TY_1", "!OTHER_TY_3!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "TYPE_DESCR", "!TYPE_DES_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "DATA_SOURC", "!DATA_SOU_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "DATASET_AC", "!DATASET__1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "FARMING_SY", "!FARMING__1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "CROP_PLANT", "!CROP_PLA_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "JAN", "!JAN_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "FEB", "!FEB_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "MAR", "!MAR_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "APR", "!APR_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "MAY", "!MAY_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "JUN", "!JUN_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "JUL", "!JUL_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "AUG", "!AUG_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "SEP", "!SEP_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "OCT", "!OCT_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "NOV", "!NOV_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "DEC", "!DEC_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "REGION", "!REGION_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "PROVINCE", "!PROVINCE_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "CITYMUNI", "!CITYMUNI_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "BARANGAY", "!BARANGAY_1!", "PYTHON_9.3")
	arcpy.CalculateField_management(layer, "REMARKS", "!REMARKS_1!", "PYTHON_9.3")

	arcpy.DeleteField_management(layer, ["UTYPE", "NEAR_FID", "NEAR_DIST","CLASSIFI_1", "RESOURCE_1", "ID_CLASS_1", "MAIN_CLA_1", "OTHER_CL_2", "OTHER_CL_3", "CLASS_DE_1", "ID_TYPE_1", "MAIN_TYP_1", "OTHER_TY_2", "OTHER_TY_3", "TYPE_DES_1", "DATA_SOU_1", "DATASET__1", "FARMING__1", "CROP_PLA_1","JAN_1", "FEB_1", "MAR_1",
	"APR_1", "MAY_1", "JUN_1", "JUL_1", "AUG_1", "SEP_1", "OCT_1", "NOV_1", "DEC_1", "REGION_1", "PROVINCE_1", "CITYMUNI_1", "BARANGAY_1", "REMARKS_1"])

if __name__ == "__main__":
	# loop thru the shapefiles in input directory
	for path, dirs, files in os.walk(input_directory,topdown=False):
		for f in files:
			if f.endswith(".shp"):
				try:
					quad = f.replace(".shp","")
					src = os.path.join(path,f)
					dst = os.path.join(output_directory,f.replace(".shp","_LULC.shp"))
					temp_union = os.path.join(output_directory,f.replace(".shp","_union.shp"))
					logger.info("%s: Checking if shapefile exists in output directory", quad)
					# if exists, union the duplicate shapefiles
					if os.path.exists(dst):
						logger.info("%s: Already exists! Executing union of duplicate shapefiles", quad)
						arcpy.Union_analysis([src,dst], temp_union, "NO_FID")

						logger.info("%s: Adding UTYPE temporary field", quad)
						arcpy.AddField_management(temp_union, "UTYPE", "TEXT")

						logger.info("%s: Calculating dominant value by comparing the two objects", quad)
						arcpy.CalculateField_management(temp_union, "UTYPE", "getDominantValue(!MAIN_TYPE!,!MAIN_TYP_1!)", "PYTHON_9.3", codeblock_union)

						logger.info("%s: Creating a layer for objects that have dominant value", quad)
						# create a layer for objects that have dominant value
						arcpy.MakeFeatureLayer_management(temp_union, "union_true", "UTYPE <> 'SAME'")

						logger.info("%s: Creating a layer for objects that don't have dominant value", quad)
						# create a layer for objects that don't have dominant value
						arcpy.MakeFeatureLayer_management(temp_union, "union_false", "UTYPE = 'SAME'")

						logger.info("%s: Calculating the other fields of the dominant value", quad)
						calculateOtherFields("union_true")

						logger.info("%s: Calculating the nearest feature of objects that don't have dominant value", quad)
						arcpy.Near_analysis("union_false", "union_true")

						logger.info("%s: Joining the fields union-true and union-false to identify what values would be assigned", quad)
						arcpy.JoinField_management("union_false", "NEAR_FID", "union_true", "FID", ["CLASSIFICA", "RESOURCE_T", "ID_CLASS", "MAIN_CLASS", "OTHER_CLAS", "OTHER_CL_1", "CLASS_DESC", "ID_TYPE", "OTHER_TYPE", "OTHER_TY_1", "TYPE_DESCR", "DATA_SOURC", "DATASET_AC", "FARMING_SY", "CROP_PLANT",
						"JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "REGION", "PROVINCE", "CITYMUNI", "BARANGAY", "REMARKS", "MAIN_TYPE" ])

						logger.info("%s: Calculating the other fields of the joined value", quad)
						calculateJoinedFields("union_false")

						logger.info("%s: Calculating area for each geometry", quad)
						arcpy.CalculateField_management(temp_union, "AREA", "!shape.area@squaremeters!", "PYTHON_9.3")

						logger.info("%s: Deleting intermediate data", quad)
						arcpy.Delete_management("union_false")
						arcpy.Delete_management("union_true")
						arcpy.Delete_management(dst)
						arcpy.Rename_management(temp_union,dst)
						arcpy.Delete_management(src)
						spamwriter.writerow([quad, src, 'Union'])
					# if does not exists, rename the the shapefile
					else:
						logger.info("%s: Does not exists. Renaming the shapefile", quad)
						arcpy.Copy_management(src, dst)
						arcpy.Delete_management(src)
						spamwriter.writerow([quad, src, 'Rename'])
				except Exception:
					logger.exception("%s: Failed to union", quad)
					spamwriter.writerow([quad, src, 'Error'])
					arcpy.Delete_management("union_false")
					arcpy.Delete_management("union_true")
					arcpy.Delete_management(temp_union)
csv_file.close()
endTime = time.time()  # End timing
print '\nElapsed Time:', str("{0:.2f}".format(round(endTime - startTime,2))), 'seconds'
