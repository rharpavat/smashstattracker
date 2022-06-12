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
    path("runanalytics/", stattracker.views.run_analytics, name="runanalytics"),
    path("graphs/", stattracker.views.view_graphs, name="viewgraphs"),
    path("totalkills/", stattracker.views.get_total_kills_chart, name="totalkills"),
    path("avgkills/", stattracker.views.get_avg_kills_chart, name="avgkills"),
    path("totaldeaths/", stattracker.views.get_total_deaths_chart, name="totaldeaths"),
    path("avgdeaths/", stattracker.views.get_avg_deaths_chart, name="avgdeaths"),
    path("totalsds/", stattracker.views.get_total_sds_chart, name="totalsds"),
    path("avgsds/", stattracker.views.get_avg_sds_chart, name="avgsds"),
    path("totalwins/", stattracker.views.get_total_wins_chart, name="totalwins"),
    path("latesttotalwins/", stattracker.views.get_latest_total_wins_chart, name="latesttotalwins"),
    path("avgrank/", stattracker.views.get_avg_rank_chart, name="avgrank")
]
