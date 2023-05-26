from django.urls import re_path
from . import views

app_name="configuration"

urlpatterns = [
    re_path(r'^$', views.configuration, name="configuration"),
    re_path(r'^upload_config/$', views.import_config_file, name="ul_config"),
    re_path(r'^upload_planif/$', views.import_planif_file, name="ul_planif"),
    re_path(r'^download_config/$', views.get_config_file, name="dl_config"),
    re_path(r'^download_planif/$', views.get_planif_file, name="dl_planif"),
    re_path(r'^mk_and_dl_blank_planif/$', views.mk_and_dl_planif, {'with_courses': False}, name="mk_and_dl_blank_planif"),
    re_path(r'^mk_and_dl_fullfilled_planif/$', views.mk_and_dl_planif, {'with_courses': True}, name="mk_and_dl_fullfilled_planif"),
    re_path(r'^mk_and_dl_fullfilled_database_file/$', views.mk_and_dl_database_file, name="mk_and_dl_fullfilled_database_file"),
]
