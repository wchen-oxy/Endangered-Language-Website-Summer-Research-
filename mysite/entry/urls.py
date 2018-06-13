from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url("entry/", views.search, name="entry"),

]