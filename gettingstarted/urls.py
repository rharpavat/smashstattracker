from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import stattracker.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", stattracker.views.index, name="index"),
    path("admin/", admin.site.urls),
    path("importdata/", stattracker.views.importdata, name="importdata"),
    path("runanalytics/", stattracker.views.run_analytics, name="runanalytics")
]
