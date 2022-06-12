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
    path("manage/", stattracker.views.manage, name="manage"),
    path("importdata/", stattracker.views.importdata, name="importdata"),
    path("runanalytics/", stattracker.views.run_analytics, name="runanalytics"),
    path("generateleaderboard/", stattracker.views.generate_leaderboard, name="generateleaderboard"),
    path("totalkills/", stattracker.views.get_total_kills_chart, name="totalkills"),
    path("avgkills/", stattracker.views.get_avg_kills_chart, name="avgkills"),
    path("totaldeaths/", stattracker.views.get_total_deaths_chart, name="totaldeaths"),
    path("avgdeaths/", stattracker.views.get_avg_deaths_chart, name="avgdeaths"),
    path("totalsds/", stattracker.views.get_total_sds_chart, name="totalsds"),
    path("avgsds/", stattracker.views.get_avg_sds_chart, name="avgsds"),
    path("totalwins/", stattracker.views.get_total_wins_chart, name="totalwins"),
    path("avgrank/", stattracker.views.get_avg_rank_chart, name="avgrank"),
    path("totaldmggiven/", stattracker.views.get_total_dmggiven_chart, name="totaldmggiven"),
    path("avgdmggiven/", stattracker.views.get_avg_dmggiven_chart, name="avgdmggiven"),
    path("totaldmgtaken/", stattracker.views.get_total_dmgtaken_chart, name="totaldmgtaken"),
    path("avgdmgtaken/", stattracker.views.get_avg_dmgtaken_chart, name="avgdmgtaken"),
    path("kdratio/", stattracker.views.get_kdratio_chart, name="kdratio"),
    path("latesttotalwins/", stattracker.views.get_latest_total_wins_chart, name="latesttotalwins"),
    path("latesttotalkills/", stattracker.views.get_latest_total_kills_chart, name="latesttotalkills"),
    path("latesttotaldeaths/", stattracker.views.get_latest_total_deaths_chart, name="latesttotaldeaths"),
    path("latesttotalsds/", stattracker.views.get_latest_total_sds_chart, name="latesttotalsds"),
    path("latesttotaldmggiven/", stattracker.views.get_latest_total_dmggiven_chart, name="latesttotaldmggiven"),
    path("latesttotaldmgtaken/", stattracker.views.get_latest_total_dmgtaken_chart, name="latesttotaldmgtaken")
]
