from django.contrib import admin

# Register your models here.
# ADDITION: change admin site title and header
# you can change the admin site title (admin.site.site_title) and header (admin.site.site_header)
# and you can also change the admin site index title (admin.site.index_title)
# and you can also change the admin name (admin.site.name)
# and you can also change the admin site site url (admin.site.site_url)
# see the documentation for more information
# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#adminsite-objects


# see https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.Group
# for more information on the Group model and its usecases
# We don't use groups in this project
# therefore to unclutter the admin site, we unregister the Group model (it's registered by default)

from django.contrib.auth.models import Group
# ADDITION: unregister Group model
# you can unregister any model you want by using the admin.site.unregister() method
# see https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#unregistering-models