from home.views import index, people
from django.urls import path

urlpatterns = [
    path("index/", index),
    path("person/", people)
]
