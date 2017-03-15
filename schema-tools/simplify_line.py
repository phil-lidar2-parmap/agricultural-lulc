# Windows
# ArcPy

__version__ = "0.1"

import arcpy
import arcpy.cartography as CA

in_features = arcpy.GetParameterAsText(0)
out_feature_class = arcpy.GetParameterAsText(1)
algorithm = arcpy.GetParameterAsText(2)
tolerance = arcpy.GetParameterAsText(3)
error_checking_option = arcpy.GetParameterAsText(4)
error_resolving_option = arcpy.GetParameterAsText(5)
collapsed_point_option = arcpy.GetParameterAsText(6)

if arcpy.GetParameterAsText(4):
	error_checking_option = 'CHECK'
else:
	error_checking_option = 'NO_CHECK'

if arcpy.GetParameterAsText(5):
	error_resolving_option = 'RESOLVE_ERRORS'
else:
	error_resolving_option = 'FLAG_ERRORS'

if arcpy.GetParameterAsText(6):
	collapsed_point_option  = 'KEEP_COLLAPSED_POINTS'
else:
	collapsed_point_option  = 'NO_KEEP'


CA.SimplifyLine(in_features, out_feature_class, algorithm, tolerance, error_resolving_option,collapsed_point_option,error_checking_option)