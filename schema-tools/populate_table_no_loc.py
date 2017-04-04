# Windows
# ArcPy

__version__ = "0.1"
__description__ = 'Automation of PARMap schema (location not included)'

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
# nso_brgy = os.path.join(current_gdb, "NSO_Brgy")

# define field lists
fields = ['MAIN_TYPE', 'MAIN_CLASS', 'RESOURCE_TYPE', 'CLASSIFICATION', 'ID_CLASS','ID_TYPE', 'SHAPE@']

# open excel file
book = open_workbook(excel_file,on_demand=True)

# get the sheets
sheet_classes = book.sheet_by_name("Classes")
sheet_dynamic = book.sheet_by_name("Dynamic")

# get the number of features
result = arcpy.GetCount_management(fc)
feature_count = int(result.getOutput(0))

try:
	# loop through features of LULC
	cursor = arcpy.da.UpdateCursor(fc,fields)
	ctr = 0
	for row in cursor:
		null_field = False

		ctr += 1

		# loop through fields
		for i in range(6):
			if not row[i]:
				null_field = True

		message_update = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]: Updating feature "\
		 + str(ctr) + " of " + str(feature_count)
		arcpy.AddMessage(message_update)

		# check if attribute fields have values
		if null_field is True:
			fc_main_type = row[0]
			geom_fc = row[6]
			lulc_type_code = ""

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

except Exception:
	arcpy.AddError((traceback.format_exc()))
	arcpy.AddError((sys.exc_info()[0]))
