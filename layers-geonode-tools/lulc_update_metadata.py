#!/usr/bin/python
# Geonode

from geonode.settings import GEONODE_APPS
import geonode.settings as settings
import os

from datetime import datetime, timedelta
from django.contrib.auth.models import Group
from django.db.models import Q
from geonode.base.models import TopicCategory
from geonode.layers.models import Layer, Style
from geoserver.catalog import Catalog
from guardian.shortcuts import assign_perm, get_anonymous_user
from pprint import pprint
from threading import Thread
import multiprocessing
import subprocess
import traceback
import psycopg2
import psycopg2.extras

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geonode.settings")

def connect_db():
	conn = psycopg2.connect(("host={0} dbname={1} user={2} password={3}".format
							 (settings.DATABASE_HOST,
							  settings.DATABASES['datastore']['NAME'],
							  settings.DATABASE_USER,
							  settings.DATABASE_PASSWORD)))

	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	return conn, cur

def close_db(conn, cur):
	cur.close()
	conn.close()


def select_by_map_no(cur, quad_name):

	# Construct query
	cur.execute('''
SELECT mapno, quadname, city_munic, province,
	   resourcema, completed, muncode, suc_hei
FROM metadata_index
WHERE quadname = %s''', (quad_name,))

	# Return results
	return cur.fetchall()

def update_style(layer, style_template):

	# Get geoserver catalog
	cat = Catalog(settings.OGC_SERVER['default']['LOCATION'] + 'rest',
				  username=settings.OGC_SERVER['default']['USER'],
				  password=settings.OGC_SERVER['default']['PASSWORD'])

	# Get equivalent geoserver layer
	gs_layer = cat.get_layer(layer.name)
	print layer.name, ': gs_layer:', gs_layer.name

	# Get current style

	cur_def_gs_style = gs_layer._get_default_style()

	if cur_def_gs_style is not None:
		print layer.name, ': cur_def_gs_style.name:', cur_def_gs_style.name

	gs_style = cat.get_style(style_template)

	try:
		if gs_style is not None:
			print layer.name, ': gs_style.name:', gs_style.name

			if cur_def_gs_style and cur_def_gs_style.name != gs_style.name:

				print layer.name, ': Setting default style...'
				gs_layer._set_default_style(gs_style)
				cat.save(gs_layer)

				print layer.name, ': Deleting old default style from geoserver...'
				cat.delete(cur_def_gs_style)

				print layer.name, ': Deleting old default style from geonode...'
				gn_style = Style.objects.get(name=layer.name)
				gn_style.delete()

	except Exception:
		print layer.name, ': Error setting style!'
		traceback.print_exc()
		raise

def update_thumb_perms(layer):

	print layer.name, ': Setting thumbnail permissions...'
	thumbnail_str = 'layer-' + str(layer.uuid) + '-thumb.png'
	thumb_url = '/home/geonode/geonode/geonode/uploaded/thumbs/' + thumbnail_str
	subprocess.call(['sudo', '/bin/chown', 'apache:apache', thumb_url])
	subprocess.call(['sudo', '/bin/chmod', '666', thumb_url])


def update_layer_perms(layer):

	try:

		print layer.name, ': Updating layer permissions...'
		# layer.remove_all_permissions()
		anon_group = Group.objects.get(name='anonymous')
		assign_perm('view_resourcebase', anon_group, layer.get_self_resource())
		assign_perm('view_resourcebase', get_anonymous_user(),
					layer.get_self_resource())

	except Exception:
		print layer.name, ': Error updating layer permissions!'
		traceback.print_exc()
		# raise


def update_lulc(layer):

	# Get quad name
	quad_name = layer.name.replace("_parmap","").upper()
	print layer.name, ': quad name:', quad_name

	# Connect to db
	conn, cur = connect_db()
	results = select_by_map_no(cur, quad_name)

	# list
	city_munic_list = []
	province_list = []
	resourcema_list = []
	suc_hei_list = []
	keywords_list = []

	# Iterating through each result
	for r in results:
		# Check if munic is completed
		if r['completed'] == "Yes":
			mapno = r['mapno']
			city_munic_list.append(r['city_munic'].replace("Bulacan", "Bulakan"))
			province_list.append(r['province'])
			resourcema_list.append(r['resourcema'])
			suc_hei_list.append(r['suc_hei'])

	suc_hei = u", ".join(list(set(suc_hei_list))).replace(",", " and")

	# Add city/muni, province and suc to keywords
	keywords_list.extend(city_munic_list)
	keywords_list.extend(list(set(province_list)))
	keywords_list.extend(list(set(suc_hei_list)))

	# Check landcover type
	landcover = "AGRILANDCOVER"
	landcover_title = "Agricultural Land Cover Map"
	if "Agricultural and Coastal" in resourcema_list:
		landcover = "AGRICOASTLANDCOVER"
		landcover_title = "Agricultural And Coastal Land Cover Map"

	layer_title = str(mapno) + " " + landcover_title
	print layer.name, ': layer_title:', layer_title

	# abstract
	if landcover == "AGRICOASTLANDCOVER":
		abstract_landcover = "Land Cover Map of Agricultural Resources integrated with Coastal Resources."
		purpose_landcover = "Integrated Agricultural and Coastal Land Cover Maps"
		resources_landcover = "resources"
		keywords_list.extend(["PARMap", "Agriculture", "CoastMap", "Mangrove", "Aquaculture", \
		"Landcover", "Phil-LiDAR 2"])
	else:
		abstract_landcover= "Land Cover Map of Agricultural Resources."
		purpose_landcover = "Detailed Agricultural Land Cover Maps"
		resources_landcover = "agricultural resources"
		keywords_list.extend(["PARMap", "Agriculture", "Landcover", "Phil-LiDAR 2"])

	# check if processed by UPD
	if len(list(set(suc_hei_list))) == 1 and list(set(suc_hei_list))[0] == "University of the Philippines Diliman":
		layer_abstract = """Maps prepared by University of the Philippines Training Center for Applied Geodesy and Photogrammetry (Phil-LiDAR 2 Program A Project 1). The use of the datasets provided herewith are covered by End Users License Agreement (EULA). Shapefiles include initial {0}

Note: Datasets subject to updating. Maps show land cover on date of data acquisition and may not reflect present land cover.

Major Source of Information: LiDAR Datasets from DREAM/Phil-LiDAR 1 Program

Accuracy and Limitations: The accuracy of the delivered Products/ouputs are dependent on the source datasets, and limitations of the software and algorithms used and implemented procedures. The Products are provided "as is" without any warranty of any kind, expressed or implied. Phil-LiDAR 2 Program does not warrant that the Products will meet the needs or expectations of the end users, or that the operations or use of the Products will be error free.""".format(abstract_landcover)
	
	else:
		layer_abstract = """Maps prepared by {0} (Phil-LiDAR 2 Program B) and reviewed by University of the Philippines Training Center for Applied Geodesy and Photogrammetry (Phil-LiDAR 2 Program A Project 1). The use of the datasets provided herewith are covered by End Users License Agreement (EULA). Shapefiles include initial {1}

Note: Datasets subject to updating. Maps show land cover on date of data acquisition and may not reflect present land cover.

Major Source of Information: LiDAR Datasets from DREAM/Phil-LiDAR 1 Program

Accuracy and Limitations: The accuracy of the delivered Products/ouputs are dependent on the source datasets, and limitations of the software and algorithms used and implemented procedures. The Products are provided "as is" without any warranty of any kind, expressed or implied. Phil-LiDAR 2 Program does not warrant that the Products will meet the needs or expectations of the end users, or that the operations or use of the Products will be error free.""".format(suc_hei, abstract_landcover)

	print layer.name, ': layer_abstract:', layer_abstract

	# purpose
	layer_purpose = "{0} are needed by Government Agencies and Local Government Units for planning and decision making. This complements on-going programs of the Department of Agriculture by utilizing LiDAR data for the mapping of {1} and vulnerability assessment.".format(purpose_landcover, resources_landcover)

	print layer.name, ': layer_purpose:', layer_purpose

	# Check if there are changes
	has_layer_changes = False
	if layer.title != layer_title:
		print layer.name, ': Setting layer.title...'
		has_layer_changes = True
		layer.title = layer_title
	if layer.abstract != layer_abstract:
		print layer.name, ': Setting layer.abstract...'
		has_layer_changes = True
		layer.abstract = layer_abstract
	if layer.purpose != layer_purpose:
		print layer.name, ': Setting layer.purpose...'
		has_layer_changes = True
		layer.purpose = layer_purpose

	if len(layer.keywords.values_list()) == 0:
		print layer.name, ': Adding keyword...'
		has_layer_changes = True
		for keyword in keywords_list:
			print keyword
			layer.keywords.add(keyword)
		
	if layer.category != TopicCategory.objects.get(identifier="imageryBaseMapsEarthCover"):
		print layer.name, ': Setting layer.category...'
		has_layer_changes = True
		layer.category = TopicCategory.objects.get(
			identifier="imageryBaseMapsEarthCover")

	# Update style
	update_style(layer, 'agricoast_lulc')

	# Update thumbnail permissions
	update_thumb_perms(layer)

	# Update layer permissions
	update_layer_perms(layer)

	# Close db
	# close_db(conn, cur)
	has_layer_changes = True
	return has_layer_changes

def save_layer(layer):
	print layer.name, ': Saving layer...'
	layer.save()


def update_metadata(layer):

	print 'layer.name:', layer.name

	try:
		has_layer_changes = False
		if 'Parmap' in layer.title:
			has_layer_changes = update_lulc(layer)

		# Save layer if there are changes
		if has_layer_changes:
			print layer.name, ': Saving layer...'
			layer.save()

		else:
			print layer.name, ': No changes to layer. Skipping...'

	except Exception:
		print layer.name, ': Error updating metadata!'
		traceback.print_exc()

	return has_layer_changes


if __name__ == "__main__":

	# Get layers with "_parmap" keyword

	layers = Layer.objects.filter(name__icontains='_parmap')

	total = len(layers)
	print 'Updating', total, 'layers!'

	# Update metadata
	counter = 0
	start_time = datetime.now()
	for layer in layers:
		print '#' * 40

		update_metadata(layer)

		counter += 1
		duration = datetime.now() - start_time
		total_time = duration.total_seconds() * total / float(counter)
		print counter, '/', total, 'ETA:', start_time + timedelta(seconds=total_time)