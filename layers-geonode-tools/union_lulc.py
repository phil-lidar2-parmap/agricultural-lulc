__version__ = "0.1"
__authors__ = "Jok Laurente"
__email__ = ["jmelaurente@gmail.com"]
__description__ = 'Union of LULC shapefiles'

import arcpy
import os

arcpy.env.overwriteOutput = True

input_directory = r"D:\union_lulc\input"
output_directory = r"D:\union_lulc\output"

codeblock_union = """def getDominantValue(code1, code2):
	# create a list for lulc types
	coastal = ["46","47","49","52"]
	agri = ["08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26", "27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","51","55"]
	non_agri = ["01","02","03","04","05","06","07","44","45","48","50","53","54"]

	utype = ""
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
	ufield = ""
	if utype == type1:
		ufield = field1
	elif utype == type2:
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
	arcpy.DeleteField_management(layer, ["CLASSIFI_1", "RESOURCE_1", "ID_CLASS_1", "MAIN_CLA_1", "OTHER_CL_2", "OTHER_CL_3", "CLASS_DE_1", "ID_TYPE_1", "MAIN_TYP_1" "OTHER_TY_2", "OTHER_TY_3", "TYPE_DES_1", "DATA_SOU_1", "DATASET__1", "FARMING__1", "CROP_PLA_1","JAN_1", "FEB_1", "MAR_1",
	"APR_1", "MAY_1", "JUN_1", "JUL_1", "AUG_1", "SEP_1", "OCT_1", "NOV_1", "DEC_1", "REGION_1", "PROVINCE_1", "CITYMUNI_1", "BARANGAY_1", "REMARKS_1", "AREA_1"])

if __name__ == "__main__":
	# loop thru the shapefiles in input directory
	for path, dirs, files in os.walk(input_directory,topdown=False):
		for f in files:
			if f.endswith(".shp"):
				src = os.path.join(path,f)
				print src
				dst = os.path.join(output_directory,f.replace(".shp","_LULC.shp"))
				temp_union = os.path.join(output_directory,f.replace(".shp","_union.shp"))
				# if exists, union the duplicate shapefiles
				if os.path.exists(dst):
					print "Union duplicate values"
					arcpy.Union_analysis([src,dst], temp_union, "NO_FID")
					# add temporary field "UTYPE"
					arcpy.AddField_management(temp_union, "UTYPE", "TEXT")
					# get the dominant value by comparing the two objects
					arcpy.CalculateField_management(temp_union, "UTYPE", "getDominantValue(!MAIN_TYPE!,!MAIN_TYP_1!)", "PYTHON_9.3", codeblock_union)
					# create a layer for objects that have dominant value
					arcpy.MakeFeatureLayer_management(temp_union, "union_true", "UTYPE <> 'SAME'")
					# create a layer for objects that don't have dominant value
					arcpy.MakeFeatureLayer_management(temp_union, "union_false", "UTYPE = 'SAME'")

					# calculate other fields
					calculateOtherFields("union_true")

					# get the nearest feature of union-false layer
					arcpy.Near_analysis("union_false", "union_true")
					# join the fields union-true and union-false to identify what values would be assigned
					# arcpy.JoinField_management("union_false", "NEAR_FID", "union_true", "FID", ["UTYPE","CLASSIFICA", "CLASSIFI_1", "RESOURCE_T", "RESOURCE_1", "MAIN_CLASS", "MAIN_CLA_1"])
					arcpy.JoinField_management("union_false", "NEAR_FID", "union_true", "FID", ["UTYPE"])
					# get the dominant value from the joined fields
					arcpy.CalculateField_management("union_false","UTYPE","!UTYPE_1!","PYTHON_9.3")
				# if does not exists, rename the the shapefile
				else:
					print "Renaming lulc layers"
					arcpy.Copy_management(src, dst)

#### integration of other fields
#### check if geometries are the same
