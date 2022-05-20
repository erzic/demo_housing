from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/text/", views.table_view, name="table_view")
]