#!/usr/bin/python
# Geonode

##sudo geonode shell
##execfile("upload_reports.py")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geonode.settings")
from django.contrib.auth.models import Group
from geonode.people.models import Profile
from geonode.settings import GEONODE_APPS
import geonode.settings as settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from geonode.documents.models import Document
from geonode.base.models import ResourceBase
from guardian.shortcuts import assign_perm, get_anonymous_user

print "Starting..."

#delete existing documents
queryset = Document.objects.all()    
for d in queryset:
        rb = ResourceBase.objects.get(id=d.resourcebase_ptr_id)
        d.delete()
        rb.delete()

abstract_text = """Maps prepared by Phil-LiDAR 2 Program B and reviewed by University of the Philippines Training Center for Applied Geodesy and Photogrammetry (Phil-LiDAR 2 Program A Project 1). The use of the datasets provided herewith are covered by End Users License Agreement (EULA). Shapefiles include initial Land Cover Map of Agricultural Resources integrated with Coastal Resources.

Note: Datasets subject to updating. Maps show land cover on date of data acquisition and may not reflect present land cover.

Major Source of Information: LiDAR Datasets from DREAM/Phil-LiDAR 1 Program

Accuracy and Limitations: The accuracy of the delivered Products/ouputs are dependent on the source datasets, and limitations of the software and algorithms used and implemented procedures. The Products are provided "as is" without any warranty of any kind, expressed or implied. Phil-LiDAR 2 Program does not warrant that the Products will meet the needs or expectations of the end users, or that the operations or use of the Products will be error free."""

path, dirs, files = os.walk("/home/geonode/Data/Documents/").next()
file_count = len(files)
print "Total number of jpeg files: ", file_count
ctr = 1

for file in os.listdir("/home/geonode/Data/Documents/"):
        
        print "Uploading ", str(ctr), " of ", file_count, ":", file
        #SULTAN_NAGA_DIMAPORO__LANAO_DEL_NORTE__AGRICOASTLANDCOVER
        name = file.replace(".jpg","")
        name1 = name.replace("__AGRICOASTLANDCOVER", " Agricultural and Coastal Land Cover Map").replace("__AGRILANDCOVER", " Agricultural Land Cover Map")
        name2 = name1.replace("__",", ").replace("_", " ").title()        
        t =  open('/home/geonode/Data/Documents/' + file, 'r')
        f = SimpleUploadedFile(file, t.read(), 'application/jpeg')
        superuser = Profile.objects.get(id=1)
        if len(name) >= 100: name = name[:99]
        c = Document.objects.create(doc_file=f,owner=superuser, title=name2, abstract=abstract_text)
        #c.set_default_permissions()
        
        anon_group = Group.objects.get(name='anonymous')
        assign_perm('view_resourcebase', anon_group, c.get_self_resource())
        assign_perm('view_resourcebase', get_anonymous_user(),
                    c.get_self_resource())
        ctr+=1    
print "Finished"
