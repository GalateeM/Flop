from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from . import views


app_name = "importation"

urlpatterns = [
    re_path(r'^$', views.importation_dispo, name="importation_dispo"),
    re_path(r'^get_dispo_file/(?P<period>[a-zA-Z0-9]+)/$', views.get_dispo_file, name="get_dispo_file"),
]
