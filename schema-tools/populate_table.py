# Windows
# ArcPy

__version__ = "0.5.4"
__description__ = 'Automation of PARMap schema'

# import modules
import arcpy
import os
import xlrd
import traceback
import sys
from xlrd import open_workbook
from datetime import datetime

# set environment to overwrite output
arcpy.env.overwriteOutput=True

# print python version
arcpy.AddMessage(sys.version)

# set parameters
excel_file = arcpy.GetParameterAsText(0)
current_gdb = arcpy.GetParameterAsText(1)

# define variables
fc = os.path.join(current_gdb, "AgriCoast_LULC")
nso_brgy = os.path.join(current_gdb, "NSO_Brgy")

# define field lists
fields = ['MAIN_TYPE', 'MAIN_CLASS', 'RESOURCE_TYPE', 'CLASSIFICATION', 'ID_CLASS','ID_TYPE',\
'BARANGAY', 'CITYMUNI', 'PROVINCE', 'REGION', 'SHAPE@']
fields_sort = ['OBJECTID', 'NAMEJN2002', 'CITYMUNI', 'PROVINCE', 'REGION_NO']
fields_near = ['NEAR_FID']
fields_nso = ['OBJECTID_1', 'NAMEJN2002', 'CITYMUNI', 'PROVINCE', 'REGION_NO']
fields_identity = ['NAMEJN2002', 'CITYMUNI_1', 'PROVINCE_1', 'REGION_NO']

# intermediate data
temp_point = os.path.join(current_gdb, "temp_point")
temp_near = os.path.join(current_gdb, "temp_near")
temp_identity = os.path.join(current_gdb, "temp_identity")

# open excel file
book = open_workbook(excel_file,on_demand=True)

# get the sheets
sheet_classes = book.sheet_by_name("Classes")
sheet_dynamic = book.sheet_by_name("Dynamic")

# get the number of features
result = arcpy.GetCount_management(fc)
feature_count = int(result.getOutput(0))
message_get_location = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
"]: Updating the location attributes of LULC"
arcpy.AddMessage(message_get_location)

try:
	# Update the location attributes
	# Limited to features intersected with brgy boundary
	arcpy.AddMessage("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
		"]: Converting feature to point")
	arcpy.FeatureToPoint_management(fc, temp_point, "CENTROID")

	arcpy.AddMessage("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
		"]: Calculating intersection")
	arcpy.Identity_analysis(temp_point, nso_brgy, temp_identity, "ALL")

	arcpy.AddMessage("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
		"]: Joining tables")
	arcpy.JoinField_management(fc, "OBJECTID", temp_identity, "ORIG_FID", fields_identity)

	arcpy.AddMessage("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
		"]: Calculating fields")
	arcpy.CalculateField_management(fc, "BARANGAY", '!NAMEJN2002!', "PYTHON_9.3")
	arcpy.CalculateField_management(fc, "CITYMUNI", '!CITYMUNI_1!', "PYTHON_9.3")
	arcpy.CalculateField_management(fc, "PROVINCE", '!PROVINCE_1!', "PYTHON_9.3")
	arcpy.CalculateField_management(fc, "REGION", '!REGION_NO!', "PYTHON_9.3")

	arcpy.AddMessage("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
		"]: Deleting intermediate fields")
	arcpy.DeleteField_management(fc, fields_identity)

	message_done_location = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
	"]: Done updating! Starting to iterate through features"
	arcpy.AddMessage(message_done_location)
except Exception:
	arcpy.AddError((traceback.format_exc()))
	arcpy.AddError((sys.exc_info()[0]))
	sys.exit()

try:
	# loop through features of LULC
	cursor = arcpy.da.UpdateCursor(fc,fields)
	ctr = 0
	for row in cursor:
		null_field = False
		location_attribute = True

		ctr += 1

		# loop through fields
		for i in range(9):
			if not row[i]:
				null_field = True

		message_update = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]: Updating feature "\
		 + str(ctr) + " of " + str(feature_count)
		arcpy.AddMessage(message_update)

		# check if attribute fields have values
		if null_field is True:
			fc_main_type = row[0]
			geom_fc = row[10]
			lulc_type_code = ""

			# check if barangay field is null
			if not row[6]:
				arcpy.AddMessage("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]: Calculating nearest feature")

				# get the nearest barangay from feature
				arcpy.GenerateNearTable_analysis(geom_fc, nso_brgy, temp_near, "", "NO_LOCATION", \
					"NO_ANGLE", "CLOSEST")

				# get the FID of the nearest barangay
				near_cursor = arcpy.da.SearchCursor(temp_near, fields_near)
				for near_row in near_cursor:
					near_fid = near_row[0]

				# get the barangay, muni, province and region name from boundary
				brgy_cursor = arcpy.da.SearchCursor(nso_brgy, fields_nso)
				for brgy_row in brgy_cursor:
					if brgy_row[0] == near_fid:
						brgy_name = brgy_row[1]
						muni_name = brgy_row[2]
						province_name = brgy_row[3]
						region_no = brgy_row[4]
						break

				location_attribute = False

			# loop through the rows in dynamic sheet
			# get the values set by SUCs
			for x in range(sheet_dynamic.nrows):

				# get the dynamic id
				id_dynamic = sheet_dynamic.row(x)[0].value

				# get the dynamic value
				value_dynamic = sheet_dynamic.row(x)[1].value

				# check if dynamic value and feature's type is the same
				if fc_main_type == value_dynamic:

					# loop through rows in classes sheet
					for y in range(sheet_classes.nrows):

						# get the values to be uploaded in the schema
						lulc_type_code = sheet_classes.row(y)[0].value
						lulc_class_code = sheet_classes.row(y)[2].value
						resource_type = sheet_classes.row(y)[4].value
						classification_code = sheet_classes.row(y)[5].value
						id_class = sheet_classes.row(y)[7].value
						id_type = sheet_classes.row(y)[8].value

						# check if dynamic id and lulc_type_code is the same
						if id_dynamic == lulc_type_code:

							# assign the values for each field
							row[0] = lulc_type_code
							row[1] = lulc_class_code
							row[2] = resource_type
							row[3] = classification_code
							row[4] = id_class
							row[5] = id_type

							# update fields if location attributes have null values
							if not location_attribute:
								row[6] = brgy_name
								row[7] = muni_name
								row[8] = province_name
								row[9] = region_no

			# update current row
			cursor.updateRow(row)

			# check if current feature was updated
			if lulc_type_code == "":
				message_result = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
				"]: WARNING! Feature was not updated"
			else:
				message_result = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
				"]: Feature was successfully updated"
			arcpy.AddMessage(message_result)

		else:
			message_result = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
				"]: Feature's attribute already exists. Skipping!"
			arcpy.AddMessage(message_result)

# delete intermediate data
	arcpy.Delete_management(temp_near)
	arcpy.Delete_management(temp_point)
	arcpy.Delete_management(temp_identity)

except Exception:
	arcpy.AddError((traceback.format_exc()))
	arcpy.AddError((sys.exc_info()[0]))
