from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
# ADDITION: change admin site title and header
admin.site.name = "Dwitter Admin"
admin.site.site_header = "Dwitter"
admin.site.site_title = "Dwitter Admin Portal"
admin.site.index_title = "Welcome to Dwitter Admin Portal"

# ADDITION: unregister Group model
admin.site.unregister(Group) # <-- We don't use groups in this project
# therefore to unclutter the admin site, we unregister the Group model
# https://stackoverflow.com/questions/13229235/django-admin-page-removing-group
